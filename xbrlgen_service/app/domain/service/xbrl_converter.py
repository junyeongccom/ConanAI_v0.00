import os
import xml.etree.ElementTree as ET
from typing import List, Dict

class XBRLConverter:
    def __init__(self):
        self.output_dir = "xbrl_output"
        os.makedirs(self.output_dir, exist_ok=True)

        # ✅ 계정과목 → XBRL 태그명 매핑 테이블
        self.xbrl_tag_map = {
             # 🧊 유동자산
            "유동자산": "CurrentAssets",
            "현금및현금성자산": "CashAndCashEquivalents",
            "단기금융상품": "ShortTermInvestments",
            "단기상각후원가금융자산": "AmortisedCostInvestmentsCurrent",
            "단기당기손익-공정가치금융자산": "FairValueThroughProfitOrLossInvestmentsCurrent",
            "매출채권": "TradeReceivables",
            "미수금": "OtherReceivablesCurrent",
            "선급비용": "PrepaidExpensesCurrent",
            "재고자산": "Inventories",
            "기타유동자산": "OtherCurrentAssets",
            "매각예정분류자산": "AssetsHeldForSale",

            # 🧊 비유동자산
            "비유동자산": "NoncurrentAssets",
            "기타포괄손익-공정가치금융자산": "FairValueThroughOCIInvestments",
            "당기손익-공정가치금융자산": "FairValueThroughProfitOrLossInvestments",
            "관계기업 및 공동기업 투자": "InvestmentsInAssociatesAndJointVentures",
            "유형자산": "PropertyPlantAndEquipment",
            "무형자산": "IntangibleAssets",
            "순확정급여자산": "DefinedBenefitAssets",
            "이연법인세자산": "DeferredTaxAssets",
            "기타비유동자산": "OtherNoncurrentAssets",

            # 🧊 자산총계
            "자산총계": "Assets",

            # 🧊 유동부채
            "부채 [개요]": "LiabilitiesAndEquity",
            "유동부채": "CurrentLiabilities",
            "매입채무": "TradePayables",
            "단기차입금": "ShortTermBorrowings",
            "미지급금": "OtherPayablesCurrent",
            "선수금": "AdvancesFromCustomers",
            "예수금": "Withholdings",
            "미지급비용": "AccruedExpenses",
            "당기법인세부채": "IncomeTaxPayable",
            "유동성장기부채": "CurrentPortionOfLongTermDebt",
            "충당부채": "ProvisionsCurrent",
            "기타유동부채": "OtherCurrentLiabilities",
            "매각예정분류부채": "LiabilitiesHeldForSale",

            # 🧊 비유동부채
            "비유동부채": "NoncurrentLiabilities",
            "사채": "BondsIssued",
            "장기차입금": "LongTermBorrowings",
            "장기미지급금": "OtherNoncurrentLiabilities",
            "순확정급여부채": "DefinedBenefitLiabilities",
            "이연법인세부채": "DeferredTaxLiabilities",
            "장기충당부채": "ProvisionsNoncurrent",
            "기타비유동부채": "OtherNoncurrentLiabilities",

            # 🧊 부채총계
            "부채총계": "Liabilities",

            # 🧊 자본
            "자본 [개요]": "Equity",
            "지배기업 소유주지분": "EquityAttributableToOwnersOfParent",
            "자본금": "CapitalStock",
            "우선주자본금": "PreferredCapital",
            "보통주자본금": "CommonCapital",
            "주식발행초과금": "SharePremium",
            "이익잉여금": "RetainedEarnings",
            "기타자본항목": "OtherComponentsOfEquity",
            "비지배지분": "NoncontrollingInterests",

            # 🧊 자본총계
            "자본총계": "Equity",

            # 🧊 부채와자본총계
            "부채와자본총계": "LiabilitiesAndEquityTotal"
        }

    def convert_to_xbrl(self, json_data: List[Dict], filename: str) -> str:
        # XML 루트 생성 (네임스페이스 포함)
        ns = "http://xbrl.ifrs.org/taxonomy/2023-03-01/ifrs-full"
        ET.register_namespace("ifrs", ns)
        root = ET.Element("xbrl")

        for row in json_data:
            print("🍇🍇계정과목:", row.get("계정과목"))  
            account_name = row.get("계정과목", "").strip()
            tag_name = self.xbrl_tag_map.get(account_name)

            # 매핑된 태그가 없으면 건너뛰기
            if not tag_name:
                print(f"⚠️ 매핑되지 않은 계정과목: {account_name}")
                continue

            for key, value in row.items():
                if key == "계정과목":
                    continue
                # 빈 문자열이나 None만 거름
                if value in ("", None):  
                    continue

                element = ET.SubElement(
                    root,
                    f"{{{ns}}}{tag_name}",
                    attrib={"contextRef": "current", "unitRef": "KRW"}
                )
                print("✅ XML 태그 추가 중:", tag_name, key, value)
                element.text = str(value)

        # XML 저장
        save_filename = filename.replace(".xlsx", ".xml").replace(" ", "_")
        save_path = os.path.join(self.output_dir, save_filename)

        tree = ET.ElementTree(root)
        tree.write(save_path, encoding="utf-8", xml_declaration=True)

        return save_path
