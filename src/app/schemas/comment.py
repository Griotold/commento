from pydantic import BaseModel, Field

class CommentRequest(BaseModel):
    """모든 엔드포인트에서 사용하는 공통 요청"""
    comment: str = Field(..., min_length=1, max_length=1000)

class CommentReviewResponse(BaseModel):
    """POST /api/review 응답"""
    is_problematic: bool

class CommentCorrectResponse(BaseModel):
    """POST /api/correct 응답"""
    corrected_comment: str

class CommentFeedbackResponse(BaseModel):
    """POST /api/feedback 응답"""
    is_problematic: bool
    severity: str  # "높음", "중간", "낮음"
    problem_types: list[str]  # 한글: ["혐오", "성차별"] 형태
    confidence: float
    issue_count: int
    reason: str

# 라벨 매핑 (별도 파일에서 관리 추천)
LABEL_MAPPING = {
    "hate": "혐오",
    "bias_others": "기타 차별",
    "bias_gender": "성차별",
    "offensive": "욕설/모욕"
}