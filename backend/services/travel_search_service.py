"""
TravelSearchService

This module provides a simple in-memory loader and searcher for the JSON files
under `backend/local_infos`. It is intentionally lightweight (no external deps)
and safe to import into `main.py`.

Features:
- UTF-8 safe loading of all .json files in `local_infos`
- `load_all_places()` returns a Python list of normalized place dicts
- Basic helpers to extract region/category from a user question
- `search_places()` to find relevant items by region, category and text

The implementation is defensive: it catches JSON/read errors and normalizes
missing fields to `None` to make downstream code simpler.
"""

from pathlib import Path
import json
from typing import List, Dict, Any, Optional, Tuple
import re


class TravelSearchService:
    """Service that loads local JSON files and provides a simple search API.

    Usage:
        svc = TravelSearchService()
        all_places = svc.load_all_places()
        results = svc.search_places(region='광주', category='음식점', query='떡갈비')
    """

    def __init__(self, local_dir: Optional[str] = None):
        # Determine the local_infos directory relative to this file
        base = Path(__file__).resolve().parent.parent
        self.local_dir = Path(local_dir) if local_dir else base / "local_infos"

        # In-memory storage for normalized places and file->meta mapping
        self.places: List[Dict[str, Any]] = []
        self._regions: List[str] = []
        self._content_types: List[str] = []

        # Load all JSON files on initialization
        self._load_all()

    # ------------------ Loading / normalization ------------------
    def _safe_load_json(self, path: Path) -> Optional[Dict[str, Any]]:
        """Read JSON file with UTF-8 and return parsed object. Returns None on error."""
        try:
            text = path.read_text(encoding="utf-8")
            return json.loads(text)
        except Exception:
            # Don't raise; caller can decide. For debugging, consider logging the path.
            return None

    def _to_float(self, s: Any) -> Optional[float]:
        try:
            if s is None or s == "":
                return None
            return float(s)
        except Exception:
            return None

    def _normalize_item(self, item: Dict[str, Any], source_file: str, content_type: str, content_type_id: int) -> Dict[str, Any]:
        """Convert raw item to the unified output schema."""
        addr1 = (item.get("addr1") or "").strip()
        addr2 = (item.get("addr2") or "").strip()
        full_address = ", ".join([p for p in (addr1, addr2) if p])

        image = item.get("firstimage") or item.get("firstimage2") or None

        # Prepare a human-readable display text that PromptBuilder can use directly.
        # Keep it concise and multiline for readability.
        title = item.get("title") or ""
        phone = item.get("tel") or ""
        category_label = content_type or ""
        display_lines = []
        if title:
            display_lines.append(title)
        if full_address:
            display_lines.append(f"주소 : {full_address}")
        elif item.get("addr1") or item.get("addr2"):
            # fallback if either addr part exists but full_address empty
            display_lines.append(f"주소 : {(item.get('addr1') or '')} {(item.get('addr2') or '')}".strip())
        if category_label:
            display_lines.append(f"카테고리 : {category_label}")
        if phone:
            display_lines.append(f"전화 : {phone}")
        display_text = "\n".join(display_lines) if display_lines else None

        return {
            "id": str(item.get("contentid") or item.get("id") or ""),
            "title": item.get("title") or None,
            "address": full_address or None,
            "category": content_type or None,
            "cat1": item.get("cat1") or None,
            "cat2": item.get("cat2") or None,
            "phone": item.get("tel") or None,
            "image": image,
            "latitude": self._to_float(item.get("mapy")),
            "longitude": self._to_float(item.get("mapx")),
            "source_file": source_file,
            "content_type_id": int(content_type_id or 0),
            # keep raw for debug if needed
            "_raw": item,
            "display_text": display_text,
        }

    def _load_all(self) -> None:
        """Load and normalize all JSON files from `local_infos` into memory.

        This method is tolerant of malformed files: files that fail to parse
        are skipped rather than causing the whole service to fail.
        """
        self.places = []
        self._regions = []
        self._content_types = []

        if not self.local_dir.exists() or not self.local_dir.is_dir():
            return

        for p in sorted(self.local_dir.glob("*.json")):
            data = self._safe_load_json(p)
            if not data:
                continue

            # extract top-level metadata
            region = data.get("region") or p.stem
            content_type = data.get("contentType") or ""
            content_type_id = data.get("contentTypeId") or 0

            if region and region not in self._regions:
                self._regions.append(region)
            if content_type and content_type not in self._content_types:
                self._content_types.append(content_type)

            items = data.get("items") or []
            # items might be a dict (single item) in some datasets
            if isinstance(items, dict):
                items = [items]

            for item in items:
                try:
                    norm = self._normalize_item(item, p.name, content_type, content_type_id)
                    # attach region to each normalized place for filtering
                    norm["region"] = region
                    self.places.append(norm)
                except Exception:
                    # Skip problematic item but continue loading
                    continue

    # Public loader
    def load_all_places(self) -> List[Dict[str, Any]]:
        """Return the in-memory list of normalized places.

        Returns a shallow copy to prevent external mutation of internal state.
        """
        return list(self.places)

    # ------------------ Simple extraction helpers ------------------
    def extract_region(self, question: str) -> Optional[str]:
        """Try to find a region token in the question by matching loaded regions.

        The logic is intentionally simple: it lowercases both question and region
        names and looks for a substring match. This works for inputs like
        '광주 맛집 추천' matching a region named '광주_전라권'.
        """
        if not question:
            return None
        q = question.lower()
        for reg in self._regions:
            # try variants: raw, underscore->space, only first token
            tokens = [reg, reg.replace("_", " "), reg.split("_")[0]]
            for t in tokens:
                if not t:
                    continue
                if t.lower() in q:
                    return reg
        return None

    def extract_category(self, question: str) -> Optional[str]:
        """Extract one of known contentType keywords from the question.

        Returns the matched contentType (exact string as in JSON files) or None.
        """
        if not question:
            return None
        q = question.lower()

        # canonical categories available in local files
        candidates = [c for c in self._content_types if c]
        # also allow matching by simple keywords (Korean)
        keyword_map = {
            "관광지": "관광지",
            "음식": "음식점",
            "음식점": "음식점",
            "숙박": "숙박",
            "문화": "문화시설",
            "문화시설": "문화시설",
            "레포츠": "레포츠",
            "쇼핑": "쇼핑",
            "축제": "축제공연행사",
            "공연": "축제공연행사",
            "여행코스": "여행코스",
            "코스": "여행코스",
        }

        # first try keyword map
        for k, v in keyword_map.items():
            if k in q:
                # ensure that v exists in our loaded content types
                if v in candidates:
                    return v
                # accept mapping even if not loaded
                return v

        # fallback: try substring match against loaded contentType names
        for c in candidates:
            if c and c.lower() in q:
                return c

        return None

    # ------------------ Search ------------------
    def search_places(self, question: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """High-level search: extract region/category then search matching places.

        Returns up to `max_results` items in the requested output format.
        """
        region = self.extract_region(question)
        category = self.extract_category(question)

        # Build a simple token list from question for matching
        tokens = [t for t in re.split(r"\W+", question.lower()) if t]

        # Filter by region/category
        filtered = self.places
        if region:
            filtered = [p for p in filtered if p.get("region") == region]
        if category:
            filtered = [p for p in filtered if p.get("category") == category]

        # Score matches by presence of tokens in title/address/category codes
        results: List[Tuple[int, Dict[str, Any]]] = []
        for p in filtered:
            score = 0
            title = (p.get("title") or "").lower()
            addr = (p.get("address") or "").lower()
            cat1 = (p.get("cat1") or "").lower()
            cat2 = (p.get("cat2") or "").lower()

            for t in tokens:
                if t in title:
                    score += 3
                if t in addr:
                    score += 2
                if t in cat1 or t in cat2:
                    score += 1

            # small boost when category/region explicitly matched
            if region and p.get("region") == region:
                score += 1
            if category and p.get("category") == category:
                score += 1

            # Only consider items with non-zero score, but if question is short
            # (e.g., only '광주 음식점'), we still want many candidates -> accept score>=0
            results.append((score, p))

        # sort by score desc then by title
        results.sort(key=lambda x: (-x[0], (x[1].get("title") or "")))

        # limit results
        selected = [r[1] for r in results[: max_results]]

        # final formatting to the required output shape
        out = []
        for p in selected:
            out.append(
                {
                    "id": p.get("id") or "",
                    "title": p.get("title") or "",
                    "address": p.get("address") or "",
                    "category": p.get("category") or "",
                    "phone": p.get("phone") or "",
                    "display_text": p.get("display_text") or "",
                    "image": p.get("image") or "",
                    "latitude": p.get("latitude") or 0,
                    "longitude": p.get("longitude") or 0,
                }
            )

        return out


if __name__ == "__main__":
    # quick local smoke test when running this module directly
    svc = TravelSearchService()
    print("Loaded places:", len(svc.load_all_places()))
    print("Regions:", svc._regions)
    print("Content types:", svc._content_types)
