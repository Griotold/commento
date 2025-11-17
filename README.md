# Commento 

# 시스템 아키텍쳐
```mermaid
graph TB
    subgraph "Client Layer"
        A[Chrome Extension<br/>유튜브 댓글 UI]
    end
    
    subgraph "Backend Service Layer"
        B[FastAPI Server<br/>Python Backend]
        C[LangChain<br/>Orchestration]
    end
    
    subgraph "AI Model Layer"
        D[beomi/korean-hatespeech-multilabel<br/>KcELECTRA-base]
        E[OpenAI API<br/>GPT-4.1-mini]
    end
    
    subgraph "Data Layer"
        F[Korean UnSmile Dataset<br/>학습 데이터<br/>LRAP: 0.919]
    end
    
    subgraph "Classification Results"
        G[혐오 표현 분류<br/>hate, offensive,<br/>bias_gender, bias_others]
        H[심각도 측정]
    end
    
    A -->|댓글 데이터 전송| B
    B --> C
    C -->|댓글 분석 요청| D
    D -->|분류 결과| G
    D -->|심각도 평가| H
    G --> C
    H --> C
    C -->|댓글 수정/피드백 생성| E
    E -->|수정된 댓글<br/>피드백 메시지| C
    C --> B
    B -->|실시간 피드백<br/>수정 제안| A
    
    F -.->|학습 데이터| D
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#fff4e1
    style D fill:#ffe1f5
    style E fill:#ffe1f5
    style F fill:#e1ffe1
    style G fill:#f5e1ff
    style H fill:#f5e1ff
```

# 서비스 처리 흐름도
- 댓글 분석 프로세스 시퀀스
```
sequenceDiagram
    participant U as 사용자
    participant CE as Chrome Extension
    participant API as FastAPI Server
    participant LC as LangChain
    participant KH as korean-hatespeech<br/>모델
    participant GPT as GPT-4.1-mini

    U->>CE: 유튜브 댓글 작성/조회
    CE->>API: 댓글 텍스트 전송
    API->>LC: 분석 요청
    
    LC->>KH: 혐오 표현 검출 요청
    KH->>KH: 다중 라벨 분류<br/>(hate, offensive,<br/>bias_gender, bias_others)
    KH-->>LC: 분류 결과 + 심각도
    
    alt 문제 댓글 감지됨
        LC->>GPT: 댓글 수정 요청<br/>(원본 + 분류 결과)
        GPT->>GPT: 교정된 댓글 생성<br/>+ 피드백 작성
        GPT-->>LC: 수정 제안 + 피드백
        LC-->>API: 종합 결과 반환
        API-->>CE: 실시간 피드백 전송
        CE-->>U: 수정 제안 표시<br/>+ 교육적 피드백
    else 정상 댓글
        LC-->>API: 정상 판정
        API-->>CE: 문제없음 전송
        CE-->>U: 댓글 게시
    end
```

# 데이터 처리 파이프라인
- AI 모델 처리 과정
```mermaid
graph LR
    subgraph "입력"
        A[유튜브 댓글<br/>텍스트]
    end
    
    subgraph "전처리"
        B[텍스트 정규화]
        C[토큰화]
    end
    
    subgraph "혐오 표현 분류"
        D[KcELECTRA-base<br/>Transformer]
        E[Multi-label<br/>Classification]
    end
    
    subgraph "분류 결과"
        F1[hate<br/>혐오]
        F2[offensive<br/>공격성]
        F3[bias_gender<br/>성차별]
        F4[bias_others<br/>기타 차별]
        G[심각도 점수<br/>0.0 ~ 1.0]
    end
    
    subgraph "댓글 교정"
        H[GPT-4.1-mini]
        I[LangChain<br/>프롬프트 체인]
    end
    
    subgraph "출력"
        J[수정된 댓글]
        K[교육적 피드백]
        L[개선 제안]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F1
    E --> F2
    E --> F3
    E --> F4
    E --> G
    
    F1 --> I
    F2 --> I
    F3 --> I
    F4 --> I
    G --> I
    
    I --> H
    H --> J
    H --> K
    H --> L
    
    style A fill:#e1f5ff
    style D fill:#ffe1f5
    style E fill:#ffe1f5
    style H fill:#ffe1e1
    style J fill:#e1ffe1
    style K fill:#e1ffe1
    style L fill:#e1ffe1
```