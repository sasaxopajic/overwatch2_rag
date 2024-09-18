#Extract hero information and add to metadata (in this case extract hero name)
from typing import Dict, List
from llama_index.core.extractors import BaseExtractor

class HeroNameExtractor(BaseExtractor):
    async def aextract(self, nodes) -> List[Dict]:
        metadata_list = [
            {
                "hero_name": node.ref_doc_id.split('/')[-1]
            }
            for node in nodes
        ]
        return metadata_list