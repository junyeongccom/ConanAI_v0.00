from ..service.xbrl_parser_service import XBRLParserService

class XBRLParserController:
    def __init__(self):
        self.service = XBRLParserService()

    def extract_from_zip(self, zip_filename: str) -> list[str]:
        return self.service.extract_files(zip_filename)