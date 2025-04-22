from lxml import etree

def validate_xbrl(xml_path: str, xsd_path: str) -> bool:
    from lxml import etree
    try:
        print("🟢 [SKIP VALIDATION MODE] 유효성 검사 생략")
        tree = etree.parse(xml_path)
        print(etree.tostring(tree, pretty_print=True, encoding="unicode"))
        return True
    except Exception as e:
        print("💥 예외 발생:", e)
        return False