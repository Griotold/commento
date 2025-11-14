from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 레이트 리미터 생성
limiter = Limiter(key_func=get_remote_address)

def setup_rate_limit(app: FastAPI) -> None:
    """
    레이트 리미팅 설정
    """
    # 레이트 리미터 추가
    app.state.limiter = limiter
    
    # 커스텀 에러 핸들러
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request, exc):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too Many Requests",
                "message": "분당 요청 한도(100개)를 초과했습니다. 잠시 후 다시 시도해주세요."
            }
        )

