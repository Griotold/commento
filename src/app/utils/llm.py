from openai import AsyncOpenAI
import os
from dotenv import load_dotenv  # ✅ 추가
from src.app.utils.constants import LABEL_MAPPING

load_dotenv()  # ✅ .env 파일 로드
# 새 방식 (OpenAI 1.0+)
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