import numpy as np
from typing import List,Any,Dict
from database import search_products_by_embedding,search_products_by_hybrid
from models import ProductResponse

class SearchService:
    """검색 관련 비즈니스 로직을 담당하는 서비스 클래스"""

    def search_products_by_hybrid(self, q_emb: np.ndarray, query_json : Dict[str, Any],category:str, top_k: int = 3) -> List[ProductResponse]:
        """
        벡터 임베딩을 기반으로 상품 검색
        
        Args:
            q_emb: 검색 쿼리의 벡터 임베딩
            top_k: 반환할 결과 수
            
        Returns:
            검색된 상품 목록
        """
        # 데이터베이스에서 상품 검색
        db_results = search_products_by_hybrid(q_emb, query_json,category,top_k)
        
        # DB 모델을 API 응답 모델로 변환
        response_products = [
            ProductResponse(
                id=p.id,
                name=p.name,
                price=p.price,
                brand=p.brand,
                link=p.link,
                image_url=p.image_url
            ) for p in db_results
        ]
        
        return response_products



    def search_products_by_embedding(self, q_emb: np.ndarray,top_k: int = 3) -> List[ProductResponse]:
        """
        벡터 임베딩을 기반으로 상품 검색
        
        Args:
            q_emb: 검색 쿼리의 벡터 임베딩
            top_k: 반환할 결과 수
            
        Returns:
            검색된 상품 목록
        """
        # 데이터베이스에서 상품 검색
        db_results = search_products_by_embedding(q_emb, top_k)
        
        # DB 모델을 API 응답 모델로 변환
        response_products = [
            ProductResponse(
                id=p.id,
                name=p.name,
                price=p.price,
                brand=p.brand,
                link=p.link,
                image_url=p.image_url
            ) for p in db_results
        ]
        
        return response_products