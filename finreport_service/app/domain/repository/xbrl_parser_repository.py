import re
import os
from pathlib import Path
from bs4 import BeautifulSoup

class XBRLParserRepository:
    def __init__(self):
        # docker-compose에서 볼륨 마운트된 경로로 설정
        self.extracted_dir = Path("/app/app/dart_documents/extracted")
        # 디렉토리가 없으면 생성
        os.makedirs(self.extracted_dir, exist_ok=True)
        print(f"[INFO] XBRL 파일 경로 기본 디렉토리: {self.extracted_dir}")

    def get_balance_sheet_tags(self, xbrl_filename: str, rcept_no: str) -> list[str]:
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
        soup = BeautifulSoup(content, 'xml')
        if soup is None:
            print("[WARN] XML 파서로 파싱 실패, lxml로 재시도합니다.")
            soup = BeautifulSoup(content, 'lxml')
            
        # 재무상태표 관련 키워드
        keywords = [
            "Assets", "Liabilities", "Equity", "RetainedEarnings", "IssuedCapital",
            "CurrentAssets", "NoncurrentAssets", "CurrentLiabilities", "NoncurrentLiabilities",
            "CashAndCashEquivalents", "Borrowings", "PropertyPlantAndEquipment",
            "Inventories", "TradeReceivables"
        ]

        print(f"[INFO] 키워드 검색 중: {keywords}")
        
        # BeautifulSoup을 활용한 태그 검색
        matching_elements = []
        tag_names = set()
        
        # 모든 태그 검색
        all_tags = soup.find_all()
        print(f"[INFO] 총 태그 수: {len(all_tags)}")
        
        # 각 키워드가 포함된 태그 찾기
        for tag in all_tags:
            tag_name = tag.name
            # 네임스페이스(콜론) 처리
            if ':' in tag_name:
                _, tag_name = tag_name.split(':', 1)
                
            # 태그 이름에 키워드가 포함되어 있는지 확인
            if any(keyword in tag_name for keyword in keywords):
                matching_elements.append(tag)
                tag_names.add(tag_name)
                
            # 태그 텍스트에 키워드가 포함되어 있는지 확인
            elif tag.string and any(keyword in tag.string for keyword in keywords):
                matching_elements.append(tag)
                tag_names.add(tag_name)
        
        print(f"[INFO] 찾은 매칭 요소 수: {len(matching_elements)}")
        
        # 매칭된 요소 콘솔에 출력
        print("\n===== 재무상태표 관련 항목 =====")
        for element in matching_elements:
            print(element)
        print("==============================\n")
        
        sorted_tags = sorted(tag_names)
        print(f"[INFO] 추출된 고유 태그 수: {len(sorted_tags)}")
        return sorted_tags