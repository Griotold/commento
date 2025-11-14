from openai import AsyncOpenAI
import os
from dotenv import load_dotenv  
from src.app.utils.constants import LABEL_MAPPING

load_dotenv()  

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_reason(text: str, problem_types: list, all_labels: list) -> str:
    """OpenAI API로 이유 생성"""
    
    top_labels = all_labels[:3]
    labels_info = ", ".join([
        f"{LABEL_MAPPING.get(l['label'], l['label'])} ({l['score']:.1%})"
        for l in top_labels
    ])
    
    prompt = f"""다음 댓글이 왜 혐오 표현으로 분류되었는지 한국어로 간단히 설명해줘. 1-2문장 정도로 작성해.

        댓글: "{text}"

        감지된 문제: {labels_info}

        설명:"""
    
    # 새 방식
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "너는 혐오 표현 분석 전문가야."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

async def correct_comment_text(text: str) -> str:
    """댓글 수정"""
    
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "너는 한국어 댓글 수정 전문가야. 혐오 표현, 욕설, 차별적 표현을 적절한 표현으로 수정해줘. 의미는 유지하면서 부적절한 언어만 수정해. 반드시 수정된 댓글 텍스트만 출력하고, 어떠한 설명이나 부가 설명도 포함하지 마."
            },
            {
                "role": "user", 
                "content": f"다음 댓글을 수정해줘. 수정된 댓글 텍스트만 출력해:\n\n{text}"
            }
        ],
        max_tokens=3000,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()