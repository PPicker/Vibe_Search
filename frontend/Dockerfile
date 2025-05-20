FROM node:18-alpine AS build

WORKDIR /app

# package.json만 복사
COPY package.json ./
RUN npm install

# 소스 코드 복사 및 빌드
COPY . .
RUN npm run build

# 실행 단계
FROM nginx:1.23-alpine

# Nginx 설정 복사
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# 빌드 결과물 복사
COPY --from=build /app/build /usr/share/nginx/html

# 포트 노출 (80에서 3000으로 변경)
EXPOSE 3000
# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]