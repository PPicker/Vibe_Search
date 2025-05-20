from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search, product

# FastAPI 앱 초기화
app = FastAPI(
    title="상품 벡터 검색 API",
    description="벡터 임베딩 기반 상품 검색 API",
    version="1.0.0",
    redirect_slashes=False  # 슬래시 리다이렉션 비활성화
)

# CORS 설정 - 프론트엔드에서 API 호출 가능하도록
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://prototype.p-picker.com"],  # 실제 도메인으로 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 라우터 등록
app.include_router(search.router)
app.include_router(product.router)

@app.get("/")
def read_root():
    return {
        "message": "벡터 검색 상품 추천 API",
        "docs_url": "/docs",
        "routes": {
            "search": "/search",
            "product_detail": "/product/{product_id}"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)