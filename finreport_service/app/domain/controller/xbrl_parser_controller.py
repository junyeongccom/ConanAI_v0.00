from ..service.xbrl_parser_service import XBRLParserService


class XBRLParserController:
    def __init__(self):
        self.parser_service = XBRLParserService()

    def parse_xbrl_file(self, filename: str):
        return self.parser_service.parse_file(filename)