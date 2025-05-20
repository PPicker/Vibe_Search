from typing import Optional
from database import get_product_detail_by_id
from models import DetailResponse

class ProductService:
    """상품 관련 비즈니스 로직을 담당하는 서비스 클래스"""
    
    def get_product_detail(self, product_id: int) -> Optional[DetailResponse]:
        """
        상품 ID로 상세 정보 조회
        
        Args:
            product_id: 상품 ID
            
        Returns:
            상품 상세 정보 또는 None (상품 없을 경우)
        """
        # 데이터베이스에서 상품 상세 정보 조회
        product = get_product_detail_by_id(product_id)
        
        if not product:
            return None
        
        # DB 모델을 API 응답 모델로 변환
        response = DetailResponse(
            name=product.name,
            price=product.price,
            link=product.link,
            brand = product.brand,
            description=product.description,
            image_urls=product.image_urls
        )
        
        return response