from typing import Dict, Any
from app.foundation.pdf_loader import convert_pdf_to_image
from app.foundation.ocr_engine import extract_text_from_image
from app.foundation.text_cleaner import clean_text
from app.platform.openai_client import GPTSummarizer

class ESGDSDService:
    def __init__(self):
        """
        ESGDSD 서비스를 초기화합니다.
        GPT 요약 클라이언트를 주입받습니다.
        """
        self.gpt = GPTSummarizer()

    def extract_text_from_pdf(self, pdf_path: str, page_num: int) -> Dict[str, Any]:
        """
        PDF 파일의 특정 페이지에서 텍스트를 추출하고 요약합니다.

        Args:
            pdf_path (str): PDF 파일 경로
            page_num (int): 추출할 페이지 번호 (1-based)

        Returns:
            Dict[str, Any]: 추출된 텍스트 정보와 요약을 담은 딕셔너리
                {
                    "page_number": int,
                    "total_text": str,
                    "summary": str
                }
        """
        # PDF를 이미지로 변환
        image = convert_pdf_to_image(pdf_path, page_num)
        
        # 이미지에서 텍스트 추출
        raw_text = extract_text_from_image(image)
        
        # 텍스트 정리
        cleaned_text = clean_text(raw_text)
        
        # GPT로 요약
        summary = self.gpt.summarize(cleaned_text)
        
        return {
            "page_number": page_num,
            "total_text": cleaned_text,
            "summary": summary
        } 