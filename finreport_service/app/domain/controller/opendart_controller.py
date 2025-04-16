from ..service.opendart_service import OpenDartService
import asyncio

class DocumentFetchController:
    def __init__(self):
        self.service = OpenDartService()

    async def fetch_and_store(self, rcept_no: str, reprt_code: str = "11011") -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.service.fetch_and_store_xbrl, rcept_no, reprt_code)
