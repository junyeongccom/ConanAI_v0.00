import os
from lxml import etree


class XBRLParserRepository:
    def __init__(self):
        # 컨테이너 내부 경로를 사용합니다
        self.data_dir = os.getenv("XBRL_FILE_DIR", "/app/documents")

    def parse_xbrl(self, filename: str):
        file_path = os.path.join(self.data_dir, filename)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XBRL 파일을 찾을 수 없습니다: {file_path}")

        tree = etree.parse(file_path)
        root = tree.getroot()

        # 예시: 모든 context 요소 출력
        contexts = root.findall(".//{http://www.xbrl.org/2003/instance}context")
        context_data = []
        for ctx in contexts:
            context_data.append(etree.tostring(ctx, pretty_print=True, encoding='unicode'))

        return context_data