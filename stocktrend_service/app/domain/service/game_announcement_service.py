from typing import Dict, Optional

class GameAnnouncementService:
    """게임사 공시내용 서비스"""
    
    # 하드코딩된 공시내용
    ANNOUNCEMENTS: Dict[str, str] = {
        "네오위즈": "블레스 이터널, 파이널 테스트 시작 (6/8)",
        "엔씨소프트": "TL, 글로벌 테스트 일정 발표 (6/12)",
        "넷마블": "세븐나이츠 레볼루션 글로벌 출시 (6/14)",
        "펄어비스": "도깨비 하반기 출시 예정 발표 (6/10)",
        "크래프톤": "배틀그라운드 모바일 2.7 업데이트 (6/15)",
        "Activision Blizzard": "MS 인수 관련 승인 발표 예정 (6/13)",
        "Electronic Arts": "EA SPORTS FC 24 공개 (6/15)",
        "Take-Two Interactive": "GTA 6 개발 현황 업데이트 예정 (6/16)",
        "NetEase": "Justice Mobile 글로벌 버전 출시 계획 (6/14)",
        "Roblox": "신규 개발자 도구 발표 (6/12)",
        "Tencent": "Honor of Kings 글로벌 버전 CBT 시작 (6/9)",
        "Nintendo": "새로운 Switch 모델 발표 예정 (6/15)"
    }
    
    def get_announcement(self, company_name: str) -> Optional[str]:
        """회사명으로 공시내용 조회"""
        return self.ANNOUNCEMENTS.get(company_name)
