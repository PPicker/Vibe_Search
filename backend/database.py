import os
import psycopg2
import numpy as np
from typing import List, Dict, Optional, Tuple
from pgvector.psycopg2 import register_vector
from aws import get_s3_client
from models import ProductSearchResult, ProductDetail



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