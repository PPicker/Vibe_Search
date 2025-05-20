from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Request 모델
class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

# Response 모델
class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    link: str
    brand: str 
    image_url: Optional[str] = None

class DetailResponse(BaseModel):
    name: str
    price: int
    link: str
    brand : str
    description: Optional[Any] = None
    image_urls: List[str]



# DB 상품 조회 결과 모델
class ProductSearchResult(BaseModel):
    id: int
    name: str
    price: int
    link: str
    brand: str
    thumbnail_key: Optional[str] = None
    image_url: Optional[str] = None

# DB 상품 상세 결과 모델
class ProductDetail(BaseModel):
    name: str
    price: int
    link: str
    brand : str
    thumbnail_key: Optional[str] = None
    description: Optional[Any] = None
    image_keys: List[str] = []
    image_urls: List[str] = []