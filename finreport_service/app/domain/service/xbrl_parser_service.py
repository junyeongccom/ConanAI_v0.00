from ..repository.xbrl_parser_repository import XBRLParserRepository

class XBRLParserService:
    def __init__(self):
        self.repository = XBRLParserRepository()

    def parse_file(self, filename: str):
        return self.repository.parse_xbrl(filename)
