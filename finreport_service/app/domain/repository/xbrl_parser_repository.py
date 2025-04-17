import re
import os
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

class XBRLParserRepository:
    def __init__(self):
        # docker-compose에서 볼륨 마운트된 경로로 설정
        self.extracted_dir = Path("/app/app/dart_documents/extracted")
        # 디렉토리가 없으면 생성
        os.makedirs(self.extracted_dir, exist_ok=True)
        print(f"[INFO] XBRL 파일 경로 기본 디렉토리: {self.extracted_dir}")

    def _find_xbrl_file(self, xbrl_filename: str, rcept_no: str) -> tuple[Path, BeautifulSoup]:
        """
        XBRL 파일을 찾고 BeautifulSoup 객체로 파싱하는 내부 메서드
        
        Args:
            xbrl_filename: XBRL 파일명
            rcept_no: 접수번호
            
        Returns:
            tuple[Path, BeautifulSoup]: (파일 경로, 파싱된 BeautifulSoup 객체)
        """
        # 확장자가 없는 경우 .xbrl 확장자 추가
        if not xbrl_filename.endswith('.xbrl'):
            xbrl_filename = f"{xbrl_filename}.xbrl"
        
        # rcept_no 디렉토리 찾기 - 전체 이름 또는 부분 이름 매칭
        rcept_dir = None
        available_dirs = [d for d in os.listdir(self.extracted_dir) 
                          if os.path.isdir(self.extracted_dir / d)]
        
        print(f"[INFO] 사용 가능한 디렉토리: {available_dirs}")
        
        # 접수번호로 시작하는 디렉토리가 있는지 확인
        for dir_name in available_dirs:
            if dir_name.startswith(rcept_no):
                rcept_dir = self.extracted_dir / dir_name
                print(f"[INFO] 접수번호 {rcept_no}로 시작하는 디렉토리를 찾았습니다: {dir_name}")
                break
        
        # 정확한 디렉토리를 찾지 못한 경우
        if rcept_dir is None:
            print(f"[ERROR] 접수번호 {rcept_no}에 해당하는 디렉토리를 찾을 수 없습니다.")
            
            # 유사한 디렉토리 찾기 시도
            for dir_name in available_dirs:
                if rcept_no in dir_name:
                    rcept_dir = self.extracted_dir / dir_name
                    print(f"[INFO] 접수번호 {rcept_no}가 포함된 디렉토리를 찾았습니다: {dir_name}")
                    break
            
            # 그래도 찾지 못한 경우 가장 최근 디렉토리 사용
            if rcept_dir is None and available_dirs:
                dir_name = available_dirs[-1]
                rcept_dir = self.extracted_dir / dir_name
                print(f"[INFO] 접수번호에 맞는 디렉토리를 찾지 못해 가장 최근 디렉토리를 사용합니다: {dir_name}")
        
        # 디렉토리를 찾지 못한 경우
        if rcept_dir is None:
            raise FileNotFoundError(f"추출된 디렉토리가 비어 있거나 접수번호에 해당하는 디렉토리를 찾을 수 없습니다: {self.extracted_dir}")
        
        # 파일 경로 생성
        xbrl_path = rcept_dir / xbrl_filename
        print(f"[INFO] 검색할 XBRL 파일 경로: {xbrl_path}")
        
        # 파일이 존재하는지 확인
        if not os.path.exists(xbrl_path):
            print(f"[ERROR] 파일을 찾을 수 없습니다: {xbrl_path}")
            
            # 디렉토리 내의 파일 목록 출력
            available_files = os.listdir(rcept_dir)
            print(f"[INFO] 디렉토리 {rcept_dir.name}에 있는 파일: {available_files}")
            
            # xbrl 확장자를 가진 파일 찾기
            xbrl_files = [f for f in available_files if f.endswith('.xbrl')]
            if xbrl_files:
                print(f"[INFO] 사용 가능한 XBRL 파일: {xbrl_files}")
                # 첫 번째 xbrl 파일 사용
                suggested_file = xbrl_files[0]
                print(f"[INFO] 파일명이 정확히 일치하지 않아 {suggested_file} 파일을 대신 사용합니다.")
                xbrl_path = rcept_dir / suggested_file
            else:
                raise FileNotFoundError(f"XBRL 파일을 찾을 수 없습니다: {xbrl_path}")
        
        print(f"[INFO] XBRL 파일을 성공적으로 찾았습니다: {xbrl_path}")
        
        # 파일 읽기 및 BeautifulSoup으로 파싱
        with open(xbrl_path, "r", encoding="utf-8") as file:
            content = file.read()

        # BeautifulSoup으로 XML 파싱
        try:
            soup = BeautifulSoup(content, 'xml')
            parser = 'xml'
        except:
            print("[WARN] XML 파서로 파싱 실패, lxml로 재시도합니다.")
            soup = BeautifulSoup(content, 'lxml')
            parser = 'lxml'
            
        print(f"[INFO] XBRL 파일을 {parser} 파서로 파싱했습니다.")
        
        return xbrl_path, soup

    def get_balance_sheet_tags(self, xbrl_filename: str, rcept_no: str) -> list[dict]:
        """
        XBRL 파일에서 재무상태표 관련 태그를 추출합니다.
        
        Args:
            xbrl_filename: XBRL 파일명 (예: entity00165459_2024-12-31.xbrl)
            rcept_no: 접수번호 (예: 20250331002860_11011)
            
        Returns:
            list[dict]: 추출된 태그 정보 목록 (항목명, 값, contextRef, 단위, 소수점 포함)
        """
        # 파일 찾고 파싱
        _, soup = self._find_xbrl_file(xbrl_filename, rcept_no)
        
        # 추출하려는 특정 태그 이름 목록 (네임스페이스 포함)
        allowed_tags = [
            "ifrs-full:CurrentAssets",
            "ifrs-full:CashAndCashEquivalents",
            "ifrs-full:ShorttermDepositsNotClassifiedAsCashEquivalents",
            "ifrs-full:CurrentTradeReceivables",
            "dart:ShortTermOtherReceivablesNet",
            "ifrs-full:CurrentPrepaidExpenses",
            "ifrs-full:Inventories",
            "ifrs-full:OtherCurrentAssets",
            "ifrs-full:NoncurrentAssets",
            "ifrs-full:NoncurrentFinancialAssetsMeasuredAtFairValueThroughOtherComprehensiveIncome",
            "ifrs-full:NoncurrentFinancialAssetsAtFairValueThroughProfitOrLoss",
            "ifrs-full:InvestmentsInSubsidiariesJointVenturesAndAssociates",
            "ifrs-full:NoncurrentRecognisedAssetsDefinedBenefitPlan",
            "ifrs-full:DeferredTaxAssets",
            "ifrs-full:OtherNoncurrentAssets",
            "ifrs-full:Assets",
            "ifrs-full:CurrentLiabilities",
            "ifrs-full:TradeAndOtherCurrentPayablesToTradeSuppliers",
            "ifrs-full:OtherCurrentPayables",
            "ifrs-full:CurrentAdvances",
            "dart:ShortTermWithholdings",
            "ifrs-full:AccrualsClassifiedAsCurrent",
            "ifrs-full:CurrentTaxLiabilities",
            "ifrs-full:CurrentPortionOfLongtermBorrowings",
            "ifrs-full:CurrentProvisions",
            "ifrs-full:OtherCurrentLiabilities",
            "ifrs-full:NoncurrentLiabilities",
            "ifrs-full:NoncurrentPortionOfNoncurrentBondsIssued",
            "ifrs-full:NoncurrentPortionOfNoncurrentLoansReceived",
            "ifrs-full:OtherNoncurrentPayables",
            "ifrs-full:NoncurrentProvisions",
            "ifrs-full:OtherNoncurrentLiabilities",
            "ifrs-full:Liabilities",
            "ifrs-full:IssuedCapital",
            "dart:IssuedCapitalOfPreferredStock",
            "dart:IssuedCapitalOfCommonStock",
            "ifrs-full:SharePremium",
            "ifrs-full:RetainedEarnings",
            "dart:ElementsOfOtherStockholdersEquity",
            "ifrs-full:EquityAndLiabilities"
        ]
        
        print(f"[INFO] 추출할 태그 목록: {len(allowed_tags)} 개")
        
        # 태그 이름을 정확히 매칭하여 추출
        extracted_tags = []
        processed_count = 0
        filtered_count = 0
        
        for tag_name in allowed_tags:
            # 해당 태그 이름을 가진 모든 요소 찾기
            matching_tags = soup.find_all(tag_name)
            
            if matching_tags:
                for tag in matching_tags:
                    # 네임스페이스(콜론) 처리
                    if ':' in tag.name:
                        namespace, local_name = tag.name.split(':', 1)
                    else:
                        local_name = tag.name
                    
                    # 값 (텍스트 내용)
                    value = tag.text.strip() if tag.text else ""
                    
                    # contextRef 속성
                    context_ref = tag.get('contextRef', '')
                    
                    # 별도재무제표(SeparateMember)가 포함된 항목만 필터링
                    if 'SeparateMember' not in context_ref:
                        continue
                    
                    # 단위 (unitRef 속성)
                    unit_ref = tag.get('unitRef', '')
                    
                    # 수치 정보에 포함된 소수점 정보 (decimals 속성)
                    decimals = tag.get('decimals', '')
                    
                    # 데이터가 모두 있는 경우만 추가
                    if value and context_ref:
                        extracted_tags.append({
                            "항목명": local_name,
                            "값": value,
                            "contextRef": context_ref,
                            "단위": unit_ref,
                            "소수점": decimals
                        })
                        processed_count += 1
                        filtered_count += 1
        
        print(f"[INFO] 추출된 총 항목 수: {processed_count}")
        print(f"[INFO] 별도재무제표(SeparateMember) 항목 수: {filtered_count}")
        return extracted_tags
        
    def extract_balance_sheet_dataframe(self, xbrl_filename: str, rcept_no: str) -> pd.DataFrame:
        """
        get_balance_sheet_tags 메서드를 호출하여 추출한 태그 정보를 DataFrame으로 변환합니다.
        
        Args:
            xbrl_filename: XBRL 파일명 (예: entity00165459_2024-12-31.xbrl)
            rcept_no: 접수번호 (예: 20250331002860_11011)
            
        Returns:
            pandas.DataFrame: 재무상태표 항목, 값, contextRef, 단위, 소수점 정보
        """
        # 추출된 태그 정보 가져오기
        extracted_tags = self.get_balance_sheet_tags(xbrl_filename, rcept_no)
        
        if not extracted_tags:
            print("[WARN] 추출된 태그가 없습니다.")
            return pd.DataFrame()
        
        # 추출된 정보로 DataFrame 생성
        df = pd.DataFrame(extracted_tags)
        
        # 결과 정보 출력
        print(f"[INFO] DataFrame 열: {df.columns.tolist()}")
        print("\n===== 추출된 재무상태표 데이터 =====")
        # 최대 10개 항목만 출력
        max_rows = min(100, len(df))
        if not df.empty:
            print(df.head(max_rows))
        else:
            print("추출된 데이터가 없습니다.")
        print("==================================\n")
        
        return df