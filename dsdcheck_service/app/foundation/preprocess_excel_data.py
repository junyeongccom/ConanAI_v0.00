import pandas as pd
import re
from typing import List, Dict, Optional, Tuple
import logging
from fastapi import UploadFile
from io import BytesIO

from app.domain.model.dsdcheck_schema import (
    FinancialStatementFromExcel,
    FinancialStatementItem,
    SheetMapping
)

logger = logging.getLogger(__name__)


def parse_index_row(cell_value: str) -> Optional[Tuple[str, str, str]]:
    """
    Index 시트의 셀 값을 파싱하여 시트 ID, fs_div, sj_div를 추출
    
    Args:
        cell_value: 셀 값 (예: "[D210000] 재무상태표, 유동/비유동법 - 연결")
        
    Returns:
        (sheet_id, fs_div, sj_div) 또는 None
    """
    if not cell_value or not isinstance(cell_value, str):
        return None
    
    # 정규표현식으로 파싱: [D210000] 재무상태표, 유동/비유동법 - 연결
    match = re.match(r'\[(D\d+)\]\s*(.+?)\s*-\s*(연결|별도)', cell_value.strip())
    if not match:
        return None
    
    sheet_id, name, report_type = match.groups()
    
    # fs_div 매핑 (연결/별도)
    fs_div = "CFS" if report_type == "연결" else "OFS"
    
    # sj_div 매핑 (보고서 종류)
    sj_div = "UNKNOWN"
    name_lower = name.lower()
    
    if "재무상태표" in name:
        sj_div = "BS"
    elif "손익계산서" in name:
        sj_div = "IS"
    elif "포괄손익" in name:
        sj_div = "CIS"
    elif "자본변동표" in name:
        sj_div = "SCE"
    elif "현금흐름표" in name:
        sj_div = "CF"
    
    if sj_div == "UNKNOWN":
        logger.warning(f"알 수 없는 재무제표 종류: {name}")
        return None
    
    return sheet_id, fs_div, sj_div


def extract_sheet_mappings(excel_file: BytesIO) -> List[SheetMapping]:
    """
    엑셀 파일의 Index 시트에서 시트 매핑 정보를 추출
    
    Args:
        excel_file: 엑셀 파일 BytesIO 객체
        
    Returns:
        시트 매핑 정보 리스트
    """
    mappings = []
    
    try:
        # Index 시트 읽기
        df_index = pd.read_excel(excel_file, sheet_name='Index', engine='openpyxl')
        
        # 모든 시트명 가져오기
        xl_file = pd.ExcelFile(excel_file, engine='openpyxl')
        all_sheets = xl_file.sheet_names
        
        logger.info(f"전체 시트 목록: {all_sheets}")
        
        # Index 시트에서 제목 정보 추출 (A열과 C열 우선 검사)
        for idx, row in df_index.iterrows():
            # A열과 C열을 우선적으로 검사
            priority_cols = []
            if len(df_index.columns) > 0:
                priority_cols.append(df_index.columns[0])  # A열
            if len(df_index.columns) > 2:
                priority_cols.append(df_index.columns[2])  # C열
            
            # 나머지 열들도 추가
            for col in df_index.columns:
                if col not in priority_cols:
                    priority_cols.append(col)
            
            for col in priority_cols:
                cell_value = str(row[col]) if pd.notna(row[col]) else ""
                
                if cell_value and '[D' in cell_value:
                    # 정규표현식으로 파싱
                    parsed = parse_index_row(cell_value)
                    
                    if parsed:
                        sheet_id, fs_div, sj_div = parsed
                        
                        # 실제 시트명 찾기 (시트 ID 기반 매칭)
                        matched_sheet = None
                        for sheet_name in all_sheets:
                            if sheet_id in sheet_name:
                                matched_sheet = sheet_name
                                break
                        
                        # 시트 ID로 찾지 못한 경우 부분 매칭 시도
                        if not matched_sheet:
                            for sheet_name in all_sheets:
                                if (sj_div == 'BS' and '재무상태표' in sheet_name) or \
                                   (sj_div == 'IS' and '손익' in sheet_name) or \
                                   (sj_div == 'CIS' and '포괄' in sheet_name) or \
                                   (sj_div == 'CF' and '현금' in sheet_name) or \
                                   (sj_div == 'SCE' and '자본' in sheet_name):
                                    
                                    if (fs_div == 'CFS' and '연결' in sheet_name) or \
                                       (fs_div == 'OFS' and '별도' in sheet_name):
                                        matched_sheet = sheet_name
                                        break
                        
                        if matched_sheet:
                            # 중복 방지
                            existing = [m for m in mappings if m.sheet_name == matched_sheet]
                            if not existing:
                                mappings.append(SheetMapping(
                                    sheet_name=matched_sheet,
                                    title=cell_value,
                                    fs_div=fs_div,
                                    sj_div=sj_div
                                ))
                                logger.info(f"시트 매핑 성공: {matched_sheet} -> {fs_div}/{sj_div}")
                        else:
                            logger.warning(f"매핑 실패 - 시트를 찾을 수 없음: {cell_value} (ID: {sheet_id})")
                    else:
                        logger.warning(f"매핑 실패 - 파싱 불가: {cell_value}")
    
    except Exception as e:
        logger.error(f"시트 매핑 추출 오류: {e}")
    
    logger.info(f"총 {len(mappings)}개 시트 매핑 완료")
    return mappings


def extract_corp_info_from_excel(excel_file: BytesIO) -> Tuple[Optional[str], Optional[int]]:
    """
    엑셀 파일에서 기업명과 연도 정보를 추출
    
    Args:
        excel_file: 엑셀 파일 BytesIO 객체
        
    Returns:
        (corp_name, year) 튜플
    """
    corp_name = None
    year = None
    
    try:
        # Index 시트에서 기업명과 연도 찾기
        df_index = pd.read_excel(excel_file, sheet_name='Index', engine='openpyxl')
        
        # 첫 몇 행에서 기업명과 연도 패턴 찾기
        for idx, row in df_index.head(10).iterrows():
            for col in df_index.columns:
                cell_value = str(row[col]) if pd.notna(row[col]) else ""
                
                # 연도 패턴 찾기 (2020-2030)
                if not year:
                    year_match = re.search(r'(20[2-3]\d)', cell_value)
                    if year_match:
                        year = int(year_match.group(1))
                
                # 기업명 패턴 찾기 (한글 포함, 주식회사 등)
                if not corp_name and len(cell_value) > 1:
                    if re.search(r'[가-힣]', cell_value) and ('주식회사' in cell_value or '㈜' in cell_value or len(cell_value.strip()) < 20):
                        # 특수문자 제거하고 기업명 추출
                        clean_name = re.sub(r'[^\w가-힣\s]', '', cell_value).strip()
                        if len(clean_name) > 1:
                            corp_name = clean_name
        
        # 기본값 설정
        if not year:
            year = 2023
        if not corp_name:
            corp_name = "업로드된 엑셀 기반 추정값"
            
    except Exception as e:
        logger.warning(f"기업 정보 추출 오류: {e}")
        corp_name = "업로드된 엑셀 기반 추정값"
        year = 2023
    
    return corp_name, year


def clean_amount_value(value) -> str:
    """
    금액 값을 정리하여 문자열로 변환
    
    Args:
        value: 원본 값
        
    Returns:
        정리된 문자열 (쉼표 제거, 숫자만)
    """
    if pd.isna(value) or value == "" or value == "-":
        return "0"
    
    # 문자열로 변환
    str_value = str(value)
    
    # 쉼표 제거 및 숫자만 추출
    cleaned = re.sub(r'[^\d]', '', str_value)
    
    return cleaned if cleaned else "0"


def extract_financial_data_from_sheet(excel_file: BytesIO, sheet_mapping: SheetMapping) -> Optional[FinancialStatementFromExcel]:
    """
    특정 시트에서 재무데이터를 추출
    
    Args:
        excel_file: 엑셀 파일 BytesIO 객체
        sheet_mapping: 시트 매핑 정보
        
    Returns:
        추출된 재무제표 데이터 또는 None
    """
    try:
        df = pd.read_excel(excel_file, sheet_name=sheet_mapping.sheet_name, engine='openpyxl')
        
        if df.empty:
            logger.warning(f"빈 시트: {sheet_mapping.sheet_name}")
            return None
        
        # 데이터 정리
        df = df.dropna(how='all')  # 모든 값이 NaN인 행 제거
        
        # 첫 번째 열을 계정명으로 사용
        account_col = df.columns[0]
        
        # 날짜 형식의 컬럼 찾기 (2023-12-31, 2022-12-31 형태)
        date_columns = []
        for col in df.columns[1:]:  # 첫 번째 열 제외
            col_str = str(col)
            if re.match(r'\d{4}-\d{2}-\d{2}', col_str):
                date_columns.append(col)
        
        # 최신 2개 연도 컬럼만 사용 (2024 제외하고 2023, 2022 사용)
        date_columns = sorted(date_columns, reverse=True)  # 최신순 정렬
        if len(date_columns) >= 3:
            # 2024년 제외하고 2023, 2022 사용
            thstrm_col = date_columns[1]  # 2023 (당기)
            frmtrm_col = date_columns[2]  # 2022 (전기)
        elif len(date_columns) >= 2:
            thstrm_col = date_columns[0]  # 최신
            frmtrm_col = date_columns[1]  # 그 다음
        else:
            logger.warning(f"충분한 날짜 컬럼이 없습니다: {sheet_mapping.sheet_name}")
            return None
        
        # 데이터 추출
        items = []
        for idx, row in df.iterrows():
            account_nm = str(row[account_col]) if pd.notna(row[account_col]) else ""
            
            # 계정명이 유효한 경우만 처리
            if account_nm and account_nm.strip() and not account_nm.startswith('Unnamed'):
                thstrm_amount = clean_amount_value(row[thstrm_col])
                frmtrm_amount = clean_amount_value(row[frmtrm_col])
                
                items.append(FinancialStatementItem(
                    account_nm=account_nm.strip(),
                    thstrm_amount=thstrm_amount,
                    frmtrm_amount=frmtrm_amount
                ))
        
        if items:
            logger.info(f"데이터 추출 완료: {sheet_mapping.sheet_name}, {len(items)}개 항목")
            return FinancialStatementFromExcel(
                fs_div=sheet_mapping.fs_div,
                sj_div=sheet_mapping.sj_div,
                items=items
            )
        
    except Exception as e:
        logger.error(f"시트 데이터 추출 오류 ({sheet_mapping.sheet_name}): {e}")
    
    return None


def parse_financial_excel(file: UploadFile) -> Tuple[List[FinancialStatementFromExcel], Optional[str], Optional[int]]:
    """
    업로드된 엑셀 파일에서 재무제표 데이터를 파싱
    
    Args:
        file: 업로드된 엑셀 파일
        
    Returns:
        (파싱된 재무제표 리스트, 기업명, 연도) 튜플
    """
    statements = []
    corp_name = None
    year = None
    
    try:
        # 파일을 BytesIO로 읽기
        file_content = file.file.read()
        excel_file = BytesIO(file_content)
        
        # 1. 기업 정보 추출
        corp_name, year = extract_corp_info_from_excel(excel_file)
        excel_file.seek(0)
        
        # 2. Index 시트에서 매핑 정보 추출
        sheet_mappings = extract_sheet_mappings(excel_file)
        
        if not sheet_mappings:
            logger.warning("시트 매핑 정보를 찾을 수 없습니다.")
            return statements, corp_name, year
        
        # 3. 각 시트에서 데이터 추출
        for mapping in sheet_mappings:
            # 파일 포인터 리셋
            excel_file.seek(0)
            
            statement = extract_financial_data_from_sheet(excel_file, mapping)
            if statement:
                statements.append(statement)
        
        logger.info(f"엑셀 파싱 완료: {len(statements)}개 재무제표")
        
    except Exception as e:
        logger.error(f"엑셀 파싱 오류: {e}")
    
    finally:
        # 파일 포인터 리셋
        file.file.seek(0)
    
    return statements, corp_name, year 