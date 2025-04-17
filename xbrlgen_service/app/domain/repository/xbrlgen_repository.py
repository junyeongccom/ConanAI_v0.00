from app.domain.model.xbrlgen_entity import XBRLGenEntity

class XBRLGenRepository:
    async def save_xbrl(self, xbrl_entity):
        """
        XBRL 문서를 저장하는 리포지토리 메소드
        """
        # 데이터베이스 저장 로직
        
        return {"status": "success", "message": "XBRL document saved successfully"}
        
    async def get_xbrl(self, id):
        """
        XBRL 문서를 조회하는 리포지토리 메소드
        """
        # 데이터베이스 조회 로직
        
        return None 