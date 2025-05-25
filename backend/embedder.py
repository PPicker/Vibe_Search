from google import genai
from google.genai import types
import os
import numpy as np
import time
from typing import Dict, Any




def build_embedding_query(item: dict, use_prefix: bool = False) -> str:
    """
    item: 상품 메타데이터 dict
    use_prefix=True  -> 'vibe: … silhouette: …'
    use_prefix=False -> '… … …'
    """
    mapping = {
        "분위기 및 지향점": "vibe",
        "실루엣": "silhouette",
        "디테일": "detail",
    }

    parts = []
    for ko_field, en_prefix in mapping.items():
        val = item.get(ko_field)
        if not val:
            continue
        parts.append(
            f"{en_prefix}: {val}" if use_prefix else val
        )

    return " ".join(parts).strip()

class Embedder():
    def __init__(self):
        self.tmp = 0
        self.api_keys = [
                    os.getenv("GEMINI_API_KEY"),
                    os.getenv("GEMINI_API_KEY2"),
                    os.getenv("GEMINI_API_KEY3"),
                    os.getenv("GEMINI_API_KEY4"),
                    os.getenv("GEMINI_API_KEY5"),
                    os.getenv("GEMINI_API_KEY6"),
                    os.getenv("GEMINI_API_KEY7"),
                    os.getenv("GEMINI_API_KEY8"),
                    os.getenv("GEMINI_API_KEY9"),
                    os.getenv("GEMINI_API_KEY10"),
                    os.getenv("GEMINI_API_KEY11")
                    ]
        self.client = genai.Client(
                api_key=self.api_keys[self.tmp],
            )
    def embed(self, json_query):
        max_retries = 3
        retry_count = 0
        text_query =build_embedding_query(json_query, use_prefix=True)
        while retry_count < max_retries:
            try:
                result = self.client.models.embed_content(
                        model="gemini-embedding-exp-03-07",
                        contents=text_query,
                        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
                )
                embedding_np = np.array(result.embeddings[0].values, dtype=np.float32)
                emb_normalized = embedding_np / np.linalg.norm(embedding_np)
                return emb_normalized
                
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise Exception(f"Failed after {max_retries} attempts: {str(e)}")
                
                self.tmp = (self.tmp+1) % 5
                self.client = genai.Client(
                    api_key=self.api_keys[self.tmp],
                )
        return None


# import asyncio
# import os
# import json
# import numpy as np
# from typing import Dict, Any
# from google import genai
# from google.genai import types
# import threading

# class AsyncGeminiClient:
#     def __init__(self):
#         self.api_keys = [
#             os.getenv("GEMINI_API_KEY"),
#             os.getenv("GEMINI_API_KEY2"),
#             os.getenv("GEMINI_API_KEY3"),
#             os.getenv("GEMINI_API_KEY4"),
#             os.getenv("GEMINI_API_KEY5"),
#             os.getenv("GEMINI_API_KEY6"),
#             os.getenv("GEMINI_API_KEY7"),
#             os.getenv("GEMINI_API_KEY8"),
#             os.getenv("GEMINI_API_KEY9"),
#             os.getenv("GEMINI_API_KEY10"),
#             os.getenv("GEMINI_API_KEY11"),
#             os.getenv("GEMINI_API_KEY12"),
#         ]
#         # 각 API 키별로 별도의 인덱스 관리 (thread-safe)
#         self._key_index = 0
#         self._lock = threading.Lock()
        
#     def _get_next_api_key(self):
#         """Thread-safe하게 다음 API 키를 가져옵니다."""
#         with self._lock:
#             current_key = self.api_keys[self._key_index]
#             self._key_index = (self._key_index + 1) % len(self.api_keys)
#             return current_key
    
#     async def _retry_with_rotation(self, operation_func, max_retries=3):
#         """API 키 로테이션과 함께 재시도를 수행합니다."""
#         retry_count = 0
#         last_exception = None
        
#         while retry_count < max_retries:
#             try:
#                 api_key = self._get_next_api_key()
#                 client = genai.Client(api_key=api_key)
#                 return await operation_func(client)
                
#             except Exception as e:
#                 last_exception = e
#                 retry_count += 1
#                 if retry_count >= max_retries:
#                     break
#                 # 짧은 대기 후 재시도
#                 await asyncio.sleep(0.1 * retry_count)
        
#         raise Exception(f"Failed after {max_retries} attempts: {str(last_exception)}")

#     def embed(self, json_query: Dict[str, Any]) -> np.ndarray:
#         """동기로 임베딩을 생성합니다."""
#         text_query = build_embedding_query(json_query, use_prefix=True)
#         max_retries = 3
#         retry_count = 0
#         last_exception = None
        
#         while retry_count < max_retries:
#             try:
#                 api_key = self._get_next_api_key()
#                 client = genai.Client(api_key=api_key)
                
#                 result = client.models.embed_content(
#                     model="gemini-embedding-exp-03-07",
#                     contents=text_query,
#                     config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
#                 )
#                 embedding_np = np.array(result.embeddings[0].values, dtype=np.float32)
#                 emb_normalized = embedding_np / np.linalg.norm(embedding_np)
#                 return emb_normalized
                
#             except Exception as e:
#                 last_exception = e
#                 retry_count += 1
#                 if retry_count >= max_retries:
#                     break
        
#         raise Exception(f"Failed after {max_retries} attempts: {str(last_exception)}")

#     async def parse_fashion_query(self, text_query: str) -> Dict[str, Any]:
#         """비동기로 패션 쿼리를 파싱합니다."""
        
#         async def _parse_operation(client):
#             model = "gemini-2.5-flash-preview-05-20"
#             contents = [
#                 # 기존 contents 내용 그대로...
#                 types.Content(
#                     role="user",
#                     parts=[
#                         types.Part.from_text(text="""도쿄의 빈티지 숍에서 찾을 것 같은 워크웨어 자켓"""),
#                     ],
#                 ),
#                 types.Content(
#                     role="model",
#                     parts=[
#                         types.Part.from_text(text="""**Analyzing Query Structure**

# I'm currently focused on extracting key elements from the user's text query and structuring them into a JSON format. My primary objective is to accurately map the provided information to the specific JSON fields: material, genre, category, silhouette, color and pattern, sub-category, atmosphere, and direction. Right now, I'm working to identify the specific requirements for each category.


# **Mapping User Queries**

# I'm now focusing on mapping the user's query into the JSON format, considering the constraints for each field. I've successfully mapped the example query \"도쿄의 빈티지 숍에서 찾을 것 같은 워크웨어 자켓\" to the JSON fields. The genre is identified as \"워크웨어\", the category as \"outer\", and the sub-category as \"자켓\".  Null values are assigned to fields lacking information, like material, silhouette, and color/pattern. The goal is to retain the original query's essence as much as possible.


# **Formulating JSON Data**

# I'm now structuring user queries into a JSON format, considering each field's specific constraints. I'm focusing on \"도쿄의 빈티지 숍에서 찾을 것 같은 워크웨어 자켓,\" successfully mapping: material (null), genre (\"워크웨어\"), category (\"outer\"), silhouette (null), color/pattern (null), sub-category (\"자켓\"), and atmosphere/direction (\"도쿄 빈티지\"). My focus is to preserve the user's intent.


# """),
#                         types.Part.from_text(text="""```json
# {
#   \"소재\": null,
#   \"장르\": \"워크웨어\",
#   \"카테고리\": \"outer\",
#   \"실루엣\": null,
#   \"색상 및 패턴\": null,
#   \"세부 카테고리\": \"자켓\",
#   \"분위기 및 지향점\": \"도쿄 빈티지 숍 느낌\"
# }
# ```"""),
#                     ],
#                 ),
#                 # ... 나머지 examples
#                 types.Content(
#                     role="user",
#                     parts=[
#                         types.Part.from_text(text=text_query),
#                     ],
#                 ),
#             ]
            
#             generate_content_config = types.GenerateContentConfig(
#                 response_mime_type="text/plain",
#                 system_instruction=[
#                     types.Part.from_text(text="""너는 패션 전문가로써 사용자의 질문을 구조화해줘
# 사용자는 자기가 원하는 느낌의 옷을 text query로 제공해줬어 
# 이걸 구조화하는게 필요해 text query를 json 형식으로 뱉어줘 
# 이때 json의 항목은 
# 소재, 장르, 카테고리,  실루엣, 색상 및 패턴, 세부 카테고리,  분위기 및 지향점이야 

# 카테고리는 top accessory bottom outer 중 하나로 뱉어줘

# 세부 카테고리는 정말 옷의 세부 카테고리를 분리해서 넣어줘

# 장르는 다음 중 하나로 뱉어줘 만약에 이중에 해당하지 않으면 null을 내보내고 복수로 해당되면 복수를 ,로 구분해서 저장하는데, 가장 근사한 애의 순서대로 나열해 가령 아메리칸 캐주얼과 아메카지 둘다 해당되는 것 같을땐 그 중 더 확실한애를 앞에 둬
# - 캐주얼
# - 아메리칸 캐주얼
# - 아메카지
# - 스트릿
# - 댄디
# - 미니멀리즘
# - 클래식 
# - 워크웨어 
# - 프레피 
# - 락시크
# - 아웃도어

# 만약에 json 항목에 해당하는 내용이 없다면 해당 항목은 null로 뱉어줘 

# 최대한 사용자의 질문에서 내용을 수정하지 말고 mapping해주는 역할만 수행해
# """),
#                 ],
#             )

#             response_text = ""
#             async for chunk in client.models.generate_content_stream(
#                 model=model,
#                 contents=contents,
#                 config=generate_content_config,
#             ):
#                 response_text += chunk.text

#             # JSON 부분만 추출
#             json_start = response_text.find('```json')
#             json_end = response_text.find('```', json_start + 7)
            
#             if json_start != -1 and json_end != -1:
#                 json_str = response_text[json_start + 7:json_end].strip()
#                 return json.loads(json_str)
#             else:
#                 try:
#                     return json.loads(response_text.strip())
#                 except json.JSONDecodeError:
#                     raise Exception("응답에서 유효한 JSON을 찾을 수 없습니다.")
        
#         return await self._retry_with_rotation(_parse_operation)

#     async def query_categorizer(self, text_query: str) -> str:
#         """비동기로 쿼리를 카테고리로 분류합니다."""
        
#         async def _categorize_operation(client):
#             model = "gemini-2.5-flash-preview-05-20"
#             contents = [
#                 # 기존 contents 내용 그대로...
#                 types.Content(
#                     role="user",
#                     parts=[
#                         types.Part.from_text(text=text_query),
#                     ],
#                 ),
#             ]
            
#             generate_content_config = types.GenerateContentConfig(
#                 response_mime_type="text/plain",
#                 system_instruction=[
#                     types.Part.from_text(text="""You are a fashion expert.
# Your task is to analyze the user's query and determine whether it contains any specific keywords.
# Based on those keywords, you must select the most appropriate category from the following structure:
# {
#     \"top\": {
#         \"tshirt\":      [\"short_sleeve_tshirt\", \"long_sleeve_tshirt\",
#                         \"sleeveless_tshirt\", \"ringer_tshirt\"],
#         \"shirt\":       [\"short_sleeve_shirt\", \"denim_shirt\",
#                         \"chambray_shirt\", \"polo_shirt\"],
#         \"knit\":        [\"knit\", \"henley_knit\", \"sweatshirt\"],
#         \"cardigan\":    [\"cardigan\"],
#         \"hoodie\":      [\"hoodie\"],
#         \"vest\":        [\"vest\"],
#     },
#     \"bottom\": {
#         \"pants\":         [\"pants\", \"slacks\", \"wide_pants\"],
#         \"chino_pants\":   [\"chino_pants\"],
#         \"denim_pants\":   [\"denim_pants\"],
#         \"cargo_pants\":   [\"cargo_pants\"],
#         \"fatigue_pants\": [\"fatigue_pants\"],
#         \"shorts\":        [\"shorts\", \"cargo_shorts\", \"denim_shorts\"],
#     },
#     \"outer\": {
#         \"jacket\":   [\"jacket\", \"souvenir_jacket\", \"liner_jacket\",
#                      \"trucker_jacket\", \"harrington_jacket\",
#                      \"hooded_jacket\", \"field_jacket\", \"zip_up_jacket\"],
#         \"blouson\":  [\"blouson\"],
#         \"blazer\":   [\"blazer\"],
#     },
#     \"accessory\": {
#         \"belt\":      [\"belt\"],
#         \"hat\":       [\"ball_cap\"],
#         \"neckwear\":  [\"necktie\"],
#         \"bag\":       [\"tote_bag\", \"shopper_bag\"],
#     },
# }

# This structure has 3 levels:

# The first level is the top category: top, bottom, outer, or accessory.

# The second level is the middle category.

# The third level is the most specific category.

# You must analyze the user's query and return the most appropriate category.
# If the query contains a match at the most specific level, return that specific category.
# If the query is less detailed, return the broader matching category.

# If the user's query does not provide enough information to determine a category, return None."""),
#                 ],
#             )

#             response_text = ""
#             async for chunk in client.models.generate_content_stream(
#                 model=model,
#                 contents=contents,
#                 config=generate_content_config,
#             ):
#                 response_text += chunk.text
            
#             return response_text.strip()
        
#         return await self._retry_with_rotation(_categorize_operation)
