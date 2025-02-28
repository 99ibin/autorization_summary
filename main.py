from openai import OpenAI
import requests
import json
from typing import List, Dict
from dataclasses import dataclass


# API 키를 입력받는 방식으로 변경
UNSPLASH_ACCESS_KEY = input("")

client = OpenAI(api_key=())
OPENAI_API_KEY =
@dataclass
class BlogContent:
    title: str
    keywords: List[str]
    main_points: List[str]
    content: str
    images: List[str]

class BlogGenerator:
    def __init__(self, openai_api_key: str, unsplash_access_key: str):
        self.openai_api_key = openai_api_key
        self.client = OpenAI(api_key=openai_api_key)
        self.unsplash_access_key = unsplash_access_key

    def generate_keywords(self, main_topic: str) -> Dict:
        prompt = f"""
        주제: {main_topic}
        
        1. 위 주제와 관련된 키워드 30개를 생성해주세요.
        2. 각 키워드에 대해 다음 정보를 제공해주세요:
           - 검색 난이도 (1-10)
           - 예상 월간 검색량
           - 경쟁강도
        3. 위 정보를 바탕으로 가장 최적화된 키워드를 하나 추천해주세요.
        
        JSON 형식으로 응답해주세요.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return json.loads(response.choices[0].message.content)

    def generate_blog_content(self, keyword: str) -> BlogContent:
        prompt = f"""
        키워드: {keyword}
        
        다음 조건에 맞는 블로그 글을 작성해주세요:
        1. 제목에 숫자를 포함할 것
        2. 1000자 내외
        3. SEO 최적화된 내용
        4. 핵심 키워드 10개 추출
        5. 중점요인 2가지 도출
        
        JSON 형식으로 응답해주세요.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        blog_data = json.loads(response.choices[0].message.content)
        
        # Unsplash에서 이미지 검색
        images = self.get_unsplash_images(keyword)
        
        return BlogContent(
            title=blog_data['title'],
            keywords=blog_data['keywords'],
            main_points=blog_data['main_points'],
            content=blog_data['content'],
            images=images
        )

    def get_unsplash_images(self, keyword: str, count: int = 2) -> List[str]:
        url = f"https://api.unsplash.com/search/photos?query={keyword}&per_page={count}&client_id={self.unsplash_access_key}"
        response = requests.get(url)
        data = response.json()
        
        return [photo["urls"]["regular"] for photo in data["results"]]

def main():
    # 블로그 생성기 초기화
    generator = BlogGenerator(OPENAI_API_KEY, UNSPLASH_ACCESS_KEY)
    
    # 메인 주제 입력
    main_topic = input("📌 블로그의 메인 주제를 입력하세요: ")
    
    # 키워드 생성 및 최적화된 키워드 선택
    keywords_data = generator.generate_keywords(main_topic)
    selected_keyword = keywords_data['recommended_keyword']
    
    # 블로그 콘텐츠 생성
    blog_content = generator.generate_blog_content(selected_keyword)
    
    # 결과 출력
    print(f"\n📢 제목: {blog_content.title}")
    print(f"\n🔑 키워드: {', '.join(blog_content.keywords)}")
    print(f"\n⭐ 중점요인:")
    for point in blog_content.main_points:
        print(f"- {point}")
    print(f"\n📝 본문:\n{blog_content.content}")
    print(f"\n🖼️ 이미지 URL:")
    for url in blog_content.images:
        print(url)

if __name__ == "__main__":
    main()