from fastapi import APIRouter, HTTPException, Depends
from services.product_service import ProductService
from models import DetailResponse

router = APIRouter(prefix="/product", tags=["product"])

# 의존성 주입을 위한 함수
def get_product_service():
    return ProductService()

@router.get("/{product_id}", response_model=DetailResponse)
def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service)
):
    product = product_service.get_product_detail(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    
    return product