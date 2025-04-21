import pandas as pd
from difflib import get_close_matches

class IFRSMappingService:
    def __init__(self, taxonomy_path: str):
        self.taxonomy_df = pd.read_excel(taxonomy_path)
        self.kor_to_concept = self._build_mapping_dict()

    def _build_mapping_dict(self) -> dict:
        mapping = {}
        for _, row in self.taxonomy_df.iterrows():
            kor_label = str(row['Preferred label']).strip()
            concept = str(row['Concept name']).strip()
            if pd.notna(kor_label) and pd.notna(concept):
                mapping[kor_label] = concept
        return mapping

    def map_account(self, account_name: str) -> str:
        if account_name in self.kor_to_concept:
            return self.kor_to_concept[account_name]
        
        candidates = get_close_matches(account_name, self.kor_to_concept.keys(), n=1, cutoff=0.7)
        return self.kor_to_concept[candidates[0]] if candidates else None

    def bulk_map(self, account_list: list[str]) -> dict:
        return {acc: self.map_account(acc) for acc in account_list}
