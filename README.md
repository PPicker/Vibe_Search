# Vibe Searching Prototype

https://prototype.p-picker.com/


이 서비스는 **텍스트 입력을 통해 원하는 스타일의 옷을 제안하는 Vibe Searching Prototype**입니다.  
Fastapi + React + Postrgresql 기반으로 구현되어 있으며, 유저 로그인 등의 인터랙션 없이 기능은 제외한 프로토타입입니다.
현재는 top - 3 related items를 제안합니다.

##  System Architecture Overview
![구조도](./readme_images/struct.png)


## 데모 화면 및 설명

### 1. 메인 화면

텍스트 입력창에 원하는 스타일을 간단히 작성합니다.
![화면](./readme_images/readme1.png)




### 2. 추천 결과 (예시)

입력: **"스트라이프 패턴의 미니멀한 무드의 셔츠"**

![예시 1](./readme_images/readme3.png)

위와 같이 Top-3 관련 상품이 카드 형태로 표시됩니다.

### 3. 상품 디테일 페이지

클릭 시 상세 정보(이미지, 가격, 설명, 구매 링크 등)를 제공합니다.

![디테일](./readme_images/readme4.png)



