from ..service.xbrl_parser_service import XBRLParserService

class XBRLParserController:
    def __init__(self):
        self.service = XBRLParserService()

    def print_balance_sheet_tags(self, xbrl_filename: str, rcept_no: str) -> list[str]:
        return self.service.filter_balance_sheet_tags(xbrl_filename, rcept_no)