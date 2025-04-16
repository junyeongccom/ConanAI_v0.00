from ..repository.xbrl_parser_repository import XBRLParserRepository

class XBRLParserService:
    def __init__(self):
        self.repository = XBRLParserRepository()

    def filter_balance_sheet_tags(self, xbrl_filename: str, rcept_no: str) -> list[str]:
        return self.repository.get_balance_sheet_tags(xbrl_filename, rcept_no)