import os
from app.domain.service.xbrl_validator import validate_xbrl

base_dir = os.path.dirname(os.path.abspath(__file__))

xml_path = os.path.join(base_dir, "../../../xbrl_output/20250421_132752_samsung.xml")
xsd_path = os.path.join(base_dir, "../../resources/taxonomy/ifrs-full_2023/full_ifrs_entry_point_2023-03-23.xsd")

print("🟡 유효성 검사 시작")
print("XML 경로:", os.path.abspath(xml_path))
print("XSD 경로:", os.path.abspath(xsd_path))

validate_xbrl(xml_path, xsd_path)
