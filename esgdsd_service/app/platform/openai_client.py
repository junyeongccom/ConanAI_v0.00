import os
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class GPTSummarizer:
    """
    OpenAI GPT를 사용하여 텍스트를 요약하는 클라이언트
    """
    def __init__(self):
        """
        OpenAI 클라이언트를 초기화합니다.
        환경 변수에서 API 키를 로드합니다.
        """
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def summarize(self, text: str) -> str:
        """
        GPT를 사용하여 텍스트를 요약합니다.

        Args:
            text (str): 요약할 텍스트

        Returns:
            str: 요약된 텍스트

        Raises:
            RuntimeError: GPT API 호출 중 오류가 발생한 경우
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "너는 ESG 전문가야. 아래 텍스트를 세 문장으로 요약해줘"},
                    {"role": "user", "content": text}
                ],
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"GPT summarization failed: {str(e)}") 