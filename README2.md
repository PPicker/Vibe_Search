# Vibe Searching

## 📦 프로젝트 구조

```text
backend/
├── Dockerfile
├── app.py
├── aws.py
├── database.py
├── embedder.py
├── models.py
├── routers/
│   ├── __init__.py
│   ├── product.py
│   └── search.py
└── services/
    ├── __init__.py
    ├── product_service.py
    └── search_service.py

database/
├── README.md
├── init/        # 초기 스키마 및 사용자 생성 스크립트
│   ├── 01-create_user.sh
│   └── 02-init_schema.sql
├── pgdata_prod  # 프로덕션 데이터 저장소
└── pgdata_test  # 테스트 데이터 저장소

docker-compose.yml
frontend/
├── Dockerfile
├── nginx/nginx.conf
├── package.json
└── src/         # React 소스 코드
```

* **`app.py`**: FastAPI 애플리케이션의 진입점으로, 앱 초기화, CORS 설정, 라우터 등록을 담당합니다.
* **`aws.py`**: 환경 변수에 저장된 자격 증명을 사용해 AWS S3 클라이언트를 생성하는 팩토리 함수를 제공합니다.
* **`database.py`**: PostgreSQL + pgvector 데이터베이스 연결과 AWS S3 통합을 싱글톤 `DatabaseManager`로 관리하며, 검색 및 상세 조회용 핵심 데이터 액세스 함수를 구현합니다.
* **`embedder.py`**: Google Gemini 임베딩 API를 래핑한 `Embedder` 클래스를 구현하며, 재시도 로직과 키 순환(Key Rotation)을 포함합니다.
* **`models.py`**: Pydantic 스키마를 정의하여 요청/응답 유효성 검사와 내부 데이터베이스 결과 매핑을 담당합니다.
* **`routers/`**: FastAPI 엔드포인트 정의

  * **`search.py`**: `/search` POST 엔드포인트로 텍스트 쿼리를 받아 임베딩 생성 후 검색 결과를 반환합니다.
  * **`product.py`**: `/product/{id}` GET 엔드포인트로 제품 상세 정보를 조회합니다.
* **`services/`**: 비즈니스 로직 캡슐화

  * **`SearchService`**: 임베딩 기반 검색을 조율하고 Pydantic 모델로 매핑합니다.
  * **`ProductService`**: 제품 상세 데이터를 조회하고 변환합니다.

---

## 계층화 아키텍처 & 의존성

```
클라이언트 요청
    ↓
API 계층 (routers/search.py, routers/product.py)
    ↓
서비스 계층 (SearchService, ProductService)
    ↓
데이터 계층 (database.search_products_by_embedding, database.get_product_detail_by_id)
    ↓         ↖️
AWS S3 (aws.get_s3_client)   Embedder (embedder.embed)
```

1. **API 계층**: HTTP 인터페이스 정의, 요청/응답 유효성 검사, 의존성 주입(`Depends`).
2. **서비스 계층**: 비즈니스 규칙, 입력 정제, Pydantic 모델을 활용한 응답 조립.
3. **데이터 계층**:

   * **PostgreSQL + pgvector**: 벡터 유사도 검색 최적화.
   * **AWS S3**: 제품 썸네일 및 이미지를 presigned URL로 저장·제공.
4. **임베딩**:

   * Google Gemini 임베딩 모델(`gemini-embedding-exp-03-07`) 사용.
   * 벡터 정규화와 키 순환을 통한 오류 복구.

---

## 🚀 디자인 패턴 & 베스트 프랙티스

* **싱글톤 패턴**: `DatabaseManager`로 PostgreSQL과 S3 연결 풀을 단일 인스턴스로 유지.
* **의존성 주입**: FastAPI `Depends`로 테스트 용이성 및 컴포넌트 분리.
* **계층 분리**: 라우팅, 비즈니스 로직, 데이터 액세스 책임 분리.
* **재시도 로직**: 임베더 실패 시 API 키 순환으로 안정성 강화.
* **환경 변수 구성**: 자격 증명, 데이터베이스 설정, AWS 정보 `.env`로 관리.
* **도커라이즈 배포**: `backend/Dockerfile`로 프로덕션 컨테이너 정의.

---

## 🐳 Docker Compose 설정

```yaml
version: '3.8'

services:
  # PostgreSQL + pgvector 데이터베이스
  database:
    image: pgvector/pgvector:0.8.0-pg15
    container_name: vibe_db
    restart: always
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./database/pgdata_prod:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # FastAPI 백엔드 서비스
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: vibe_backend
    restart: on-failure
    env_file:
      - .env
    depends_on:
      - database
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app

  # React 프론트엔드 서비스 + Nginx
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: vibe_frontend
    restart: on-failure
    depends_on:
      - backend
    ports:
      - "3000:80"   # Nginx가 80 포트로 서비스
    volumes:
      - ./frontend:/usr/share/nginx/html:ro

networks:
  default:
    driver: bridge
```

* `database`: PostgreSQL + pgvector 컨테이너로 데이터 영속성 보장.
* `backend`: FastAPI 앱 컨테이너화, 코드 마운트로 개발 중 실시간 반영.
* `frontend`: React 빌드 후 Nginx로 서빙, 호스트 3000번 포트 노출.
* 브리지 네트워크로 서비스 간 통신 구성.

---

## 📈 확장성 및 향후 개선 방향

* **배치 임베딩(Batch Embedding)**: 쿼리 묶음 처리로 API 호출 횟수 및 비용 절감.
* **캐싱 레이어**: Redis/Memcached 도입으로 자주 요청되는 데이터 캐싱.
* **레이트 리밋팅(Rate Limiting)**: 과부하 시 임베딩 API와 DB 보호.
* **모니터링 & 로깅**: 구조화된 로그와 Prometheus 메트릭 추가.

---

