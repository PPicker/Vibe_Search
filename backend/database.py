import os
import psycopg2
import numpy as np
from typing import List, Dict, Optional, Tuple,Any
from pgvector.psycopg2 import register_vector
from aws import get_s3_client
from models import ProductSearchResult, ProductDetail
from psycopg2.extras import RealDictCursor


# 상수
TOP_K = 3

# 데이터베이스 연결 설정
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options="-c search_path=public",
    )
    conn.autocommit = True
    register_vector(conn)
    return conn

# S3 연결
def get_s3_connection():
    s3 = get_s3_client()
    bucket = os.getenv("AWS_S3_BUCKET_NAME")
    return s3, bucket

# 싱글톤 패턴으로 커넥션 관리
class DatabaseManager:
    _instance = None
    _conn = None
    _s3 = None
    _bucket = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._conn = get_db_connection()
            cls._s3, cls._bucket = get_s3_connection()
        return cls._instance

    @property
    def conn(self):
        return self._conn

    @property
    def s3(self):
        return self._s3

    @property
    def bucket(self):
        return self._bucket

    def close(self):
        if self._conn:
            self._conn.close()
            self._conn = None



def search_products_by_hybrid(q_emb: np.ndarray, query_json: Dict[str, Any], category: str, k: int = TOP_K) -> List[ProductSearchResult]:
    """
    카테고리 백오프와 벡터 유사도를 결합한 하이브리드 검색
    
    Args:
        q_emb: 쿼리 임베딩 벡터
        query_json: 구조화된 패션 쿼리 정보
        category: 카테고리 (query_categorizer 결과)
        k: 반환할 상품 수
    
    Returns:
        List[ProductSearchResult]: 검색된 상품 목록 (presigned URL 포함)
    """
    db_manager = DatabaseManager()
    conn = db_manager.conn
    s3 = db_manager.s3
    bucket = db_manager.bucket

    # 1. 쿼리 정보 추출 및 전처리
    genre = query_json.get("장르", None)

    # 장르를 배열로 변환
    genre_list = None
    if genre:
        if isinstance(genre, str):
            genre_list = [g.strip() for g in genre.split(",")]
        else:
            genre_list = genre

    print(f"🔍 검색 시작: category={category}, genre={genre_list}")

    # with conn.cursor() as cur:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # 2. 카테고리 백오프 검색 실행
        results = search_with_category_backoff_and_filters(
            cur=cur,
            category=category,
            genre_list=genre_list,
            q_emb=q_emb,
            k=k
        )

    # 3. presigned URL 생성
    final_results = []
    for r in results:
        product = ProductSearchResult(**r)
        key = product.thumbnail_key
        if key:
            try:
                product.image_url = s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket, "Key": key},
                    ExpiresIn=3600,
                )
            except Exception as e:
                print(f"⚠️ presigned URL 생성 실패: {key}, {e}")
                product.image_url = None
        final_results.append(product)

    print(f"✅ 최종 반환: {len(final_results)}개 상품")
    return final_results


def search_with_category_backoff_and_filters(cur, category: str, genre_list: list, 
                                           q_emb: np.ndarray, k: int):
    """
    카테고리 백오프와 모든 필터를 적용한 검색
    """
    # 1. 카테고리 경로와 depth 가져오기
    if category != "None":
        path_text, depth = get_category(cur, category)
    
    else : 
        print(f"⚠️ 카테고리 '{category}'를 찾을 수 없음. 전체 검색으로 대체")
        return search_without_category_filter(cur, genre_list, q_emb, k)
    
    results = []
    parts = path_text.split(".")

    print(f"🎯 카테고리 '{category}' 검색: path={path_text}, depth={depth}")
    
    # 2. 해당 카테고리와 그 하위 모든 항목을 한 번에 검색
    where_conditions = ["p.category_path <@ %s::ltree"]  # 해당 경로 + 하위 모두
    params = [path_text]
    if genre_list:
        where_conditions.append("p.genre && %s")
        params.append(genre_list)
    params.extend([q_emb, k])
    # 4. SQL 쿼리 실행
    sql = f"""
        SELECT  p.id, p.name, p.original_price AS price,
                p.url AS link, p.brand, p.thumbnail_key,
                p.category_path
        FROM    products AS p
        WHERE   {' AND '.join(where_conditions)}
        ORDER BY p.embedding <#> %s                     -- 벡터 유사도 정렬
        LIMIT   %s
    """

    cur.execute(sql, params)
    results.extend(cur.fetchall()) # 바로 List[Dict] 형태
            
    return results

        

def search_without_category_filter(cur, genre_list: list, q_emb: np.ndarray, k: int):
    """
    카테고리 필터 없이 다른 필터들과 벡터 유사도로만 검색
    """
    where_conditions = []
    params = []
    
    # 장르 필터
    if genre_list:
        where_conditions.append("p.genre && %s")
        params.append(genre_list)
    
    # WHERE 절 구성
    where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""
    
    # 임베딩 벡터와 k 추가
    params.extend([q_emb, k])
    
    sql = f"""
        SELECT  p.id, p.name, p.original_price AS price,
                p.url AS link, p.brand, p.thumbnail_key,
                p.category_path
        FROM    products AS p
        {where_clause}
        ORDER BY p.embedding <#> %s              -- 벡터 유사도 정렬
        LIMIT   %s
    """
    
    cur.execute(sql, params)
    
    cur.execute(sql, params)
    results = cur.fetchall()  # 바로 List[Dict] 형태

    return results[:k]


def get_category(cur, slug: str):
    """
    slug 로 category 레코드 찾기.
    Return (path_text, depth_int)  depth = 1(root)|2(mid)|3(leaf)
    """
    cur.execute(
        "SELECT path::text AS path, nlevel(path) AS depth "
        "FROM   category WHERE name = %s",
        (slug,)
    )
    rec = cur.fetchone()
    if not rec:
        raise ValueError(f"category '{slug}' not found in DB")
    print(rec)
    return rec["path"], rec["depth"]

# 벡터 검색 함수
def search_products_by_embedding(q_emb: np.ndarray, k: int = TOP_K) -> List[ProductSearchResult]:
    """
    1) pgvector의 inner-product (<#>)로 top-k id 검색
    2) 곧바로 name, price, link, thumbnail_key 가져오기
    3) presigned URL 생성
    """
    db_manager = DatabaseManager()
    conn = db_manager.conn
    s3 = db_manager.s3
    bucket = db_manager.bucket

    # 1) Tensor → Python 리스트 & 검색
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                p.id,
                p.name,
                p.original_price AS price,
                p.url AS link,
                p.brand,
                p.thumbnail_key
            FROM products AS p
            ORDER BY p.embedding <#> %s
            LIMIT %s;
            """,
            (q_emb, k),
        )
        cols = [c.name for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]

    # 2) presigned URL 생성
    results = []
    for r in rows:
        product = ProductSearchResult(**r)
        key = product.thumbnail_key
        if key:
            product.image_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=3600,
            )
        results.append(product)

    return results

# 상품 상세 정보 조회
def get_product_detail_by_id(prod_id: int) -> Optional[ProductDetail]:
    """
    1) products 메타 정보 가져오기
    2) product_images 에서 이미지 키 가져오기
    3) S3 presigned URL 생성
    """
    db_manager = DatabaseManager()
    conn = db_manager.conn
    s3 = db_manager.s3
    bucket = db_manager.bucket

    # 1) products 메타
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT name,
                   original_price AS price,
                   url as link,
                   brand,
                   description,
                   thumbnail_key
              FROM products
             WHERE id = %s
            """,
            (prod_id,),
        )
        result = cur.fetchone()
        if not result:
            return None
        
        name, price, link,brand, description,thumb_key = result
        product = ProductDetail(
            name=name,
            price=price,
            link=link,
            brand = brand,
            description = description,
            thumbnail_key=thumb_key,
            image_keys=[],
            image_urls=[]
        )

    # 2) products_images 에서 모든 key (order_index 순)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT key
              FROM product_images
             WHERE product_id = %s
             ORDER BY order_index
            """,
            (prod_id,),
        )
        product.image_keys = [row[0] for row in cur.fetchall()]

    # 3) presigned URL 리스트 생성
    if product.thumbnail_key:
        product.image_urls.append(
            s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": product.thumbnail_key},
                ExpiresIn=3600,
            )
        )
    
    for key in product.image_keys:
        product.image_urls.append(
            s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=3600,
            )
        )

    return product