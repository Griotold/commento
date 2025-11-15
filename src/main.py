from fastapi import FastAPI, Request 
from src.app.schemas.comment import (
    CommentRequest,
    CommentReviewResponse,
    CommentCorrectResponse,
    CommentFeedbackResponse,
)
from src.app.services.comment_service import CommentService
from src.app.core.middlewares.cors import setup_cors
from src.app.core.middlewares.rate_limit import setup_rate_limit, limiter

app = FastAPI(
    title="Commento API",
    description="""
    한국어 혐오 표현 분류 및 댓글 개선 API
    
    ## 기능
    - **글 검토**: 혐오 표현 포함 여부 즉시 판정
    - **글 수정**: 부적절한 표현을 적절한 표현으로 수정
    - **피드백**: 문제 유형, 심각도, AI 설명 제공
    
    ## 분류 카테고리
    - 혐오 (hate)
    - 성차별 (bias_gender)
    - 기타 차별 (bias_others)
    - 욕설/모욕 (offensive)
    """,
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

setup_cors(app)
setup_rate_limit(app)

@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post(
    "/api/review",
    response_model=CommentReviewResponse,
    summary="댓글 검토 (빠른 검증)",
    description="댓글에 혐오 표현이 포함되어 있는지 빠르게 검증합니다.",
    responses={
        200: {
            "description": "검증 성공",
            "content": {
                "application/json": {
                    "example": {"is_problematic": True}
                }
            }
        },
        422: {
            "description": "유효성 검사 실패",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_type",
                                "loc": ["body", "comment"],
                                "msg": "Input should be a valid string",
                                "input": 123
                            }
                        ]
                    }
                }
            }
        },
        429: {
            "description": "요청 한도 초과",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Too Many Requests",
                        "message": "분당 요청 한도(100개)를 초과했습니다. 잠시 후 다시 시도해주세요."
                    }
                }
            }
        }
    }
)
@limiter.limit("100/minute")
async def review_comment(request: Request, body:CommentRequest):
    """빠른 검증"""
    result = CommentService.classify(body.comment)
    return CommentReviewResponse(is_problematic=result["is_problematic"])

@app.post(
    "/api/correct",
    response_model=CommentCorrectResponse,
    summary="댓글 수정",
    description="혐오 표현을 포함한 댓글을 적절한 표현으로 수정합니다.",
    responses={
        200: {
            "description": "수정 성공",
            "content": {
                "application/json": {
                    "example": {"corrected_comment": "수정된 댓글 텍스트"}
                }
            }
        },
        422: {
            "description": "유효성 검사 실패",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_type",
                                "loc": ["body", "comment"],
                                "msg": "Input should be a valid string",
                                "input": 123
                            }
                        ]
                    }
                }
            }
        },
        429: {
            "description": "요청 한도 초과",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Too Many Requests",
                        "message": "분당 요청 한도(100개)를 초과했습니다. 잠시 후 다시 시도해주세요."
                    }
                }
            }
        }
    }
)
@limiter.limit("100/minute")
async def correct_comment(request: Request,body: CommentRequest):
    """댓글 수정"""
    result = await CommentService.correct(body.comment)
    return CommentCorrectResponse(corrected_comment=result["corrected_comment"])

@app.post(
    "/api/feedback",
    response_model=CommentFeedbackResponse,
    summary="상세 피드백",
    description="댓글에 대한 상세한 분석과 개선 사항을 제공합니다.",
    responses={
        200: {
            "description": "피드백 성공",
            "content": {
                "application/json": {
                    "example": {
                        "is_problematic": True,
                        "severity": "높음",
                        "problem_types": ["고정관념", "부적절한 언어"],
                        "confidence": 0.92,
                        "issue_count": 2,
                        "reason": "여성을 특정 직업으로만 한정하는 고정관념이 포함되어 있습니다."
                    }
                }
            }
        },
        422: {
            "description": "유효성 검사 실패",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "string_type",
                                "loc": ["body", "comment"],
                                "msg": "Input should be a valid string",
                                "input": 123
                            }
                        ]
                    }
                }
            }
        },
        429: {
            "description": "요청 한도 초과",
            "content": {
                "application/json": {
                    "example": {
                        "error": "Too Many Requests",
                        "message": "분당 요청 한도(100개)를 초과했습니다. 잠시 후 다시 시도해주세요."
                    }
                }
            }
        }
    }
)
@limiter.limit("100/minute")
async def feedback_comment(request: Request, body: CommentRequest):
    """상세 피드백"""
    return await CommentService.get_feedback(body.comment)