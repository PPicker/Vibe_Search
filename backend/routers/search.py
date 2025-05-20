from fastapi import APIRouter, HTTPException, Depends
from typing import List
from embedder import Embedder
from services.search_service import SearchService
from models import SearchRequest, ProductResponse

# 접두사에서 마지막 슬래시 제거
router = APIRouter(prefix="/search", tags=["search"])

# 임베더 인스턴스
embedder = Embedder()

# 의존성 주입을 위한 함수
def get_embedder():
    return embedder

def get_search_service():
    return SearchService()

# 여기서 경로를 "" (빈 문자열)로 변경
@router.post("", response_model=List[ProductResponse])
def search_products(
    req: SearchRequest, 
    embedder: Embedder = Depends(get_embedder),
    search_service: SearchService = Depends(get_search_service)
):
    q = req.query.strip()
    if not q:
        raise HTTPException(status_code=400, detail="검색어를 입력해주세요")
    
    # 여기서 필요하다면 추가 처리 가능
    # - translate 함수로 영어 번역
    # - categorize 함수로 카테고리 분류
    
    # 쿼리 임베딩 생성
    q_emb = embedder.embed(q)
    
    # 서비스 계층을 통해 상품 검색
    results = search_service.search_products_by_embedding(q_emb, req.top_k)
    
    return results