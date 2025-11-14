from transformers import pipeline
from typing import Optional

class HateSpeechClassifier:
    _instance = None
    classifier = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self.classifier is None:
            print("✅ 혐오 표현 분류 모델 로딩 중...")
            self.classifier = pipeline(
                "text-classification",
                model="beomi/korean-hatespeech-multilabel",
                device=-1,  # CPU
                top_k=None  # 모든 라벨 반환
            )
            print("✅ 모델 로드 완료!")
    
    def predict(self, text: str) -> list:
        """모델 예측"""
        return self.classifier(text)

# 싱글톤 패턴 (모델은 한 번만 로드)
classifier_instance = HateSpeechClassifier()