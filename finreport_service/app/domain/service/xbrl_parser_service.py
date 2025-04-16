from ..repository.xbrl_parser_repository import XBRLParserRepository

class XBRLParserService:
    def __init__(self):
        self.repository = XBRLParserRepository()

    def extract_files(self, zip_filename: str) -> list[str]:
        return self.repository.unzip_xbrl_files(zip_filename)