"""
PromptBuilder

Builds a human- and model-friendly prompt from a user question and a list
of travel places (as returned by `TravelSearchService.search_places`).

This module only constructs prompt strings; it does not call OpenAI or any
external service.
"""

from typing import List, Dict


class PromptBuilder:
    """Convert search results into a formatted prompt for LLM consumption.

    Usage:
        from backend.services.prompt_builder import PromptBuilder
        prompt = PromptBuilder.build_prompt(question, travel_list)
    """

    @staticmethod
    def build_prompt(question: str, travel_list: List[Dict]) -> str:
        """Build and return the prompt string.

        Args:
            question: The original user question (Korean expected).
            travel_list: A list of places, each being a dict with keys like
                'title', 'address', 'category', 'phone', 'image'. This matches
                the output of `TravelSearchService.search_places()`.

        Returns:
            A single string containing the full prompt. The caller can send
            this string to an LLM. This method does not perform any network
            I/O or model calls.
        """

        # System instruction: set LLM behavior and constraints
        system_lines = [
            "System:",
            "너는 대한민국 여행 전문가이다.",
            "반드시 제공된 여행 정보만 이용하여 답변한다.",
            "없는 정보는 추측하지 않는다.",
            "",
        ]

        # User block: include the user's question, followed by formatted results
        user_lines = [
            "User:",
            f"사용자 질문: {question}",
            "",
            "검색된 여행지 목록:",
        ]

        # For each place, format a readable block containing the requested fields
        # The travel_list items are expected to contain at least the keys noted
        for idx, place in enumerate(travel_list, start=1):
            title = place.get("title") or ""
            address = place.get("address") or ""
            category = place.get("category") or ""
            phone = place.get("phone") or ""
            image = place.get("image") or ""

            # Each place is presented in a tidy, human-readable way.
            user_lines.append(f"{idx}. 이름: {title}")
            user_lines.append(f"   주소: {address}" if address else "   주소: ")
            user_lines.append(f"   카테고리: {category}" if category else "   카테고리: ")
            user_lines.append(f"   전화번호: {phone}" if phone else "   전화번호: ")
            user_lines.append(f"   이미지: {image}" if image else "   이미지: ")
            user_lines.append("")

        # Append the original user question clearly at the end as requested
        user_lines.append(f'"{question}"')

        # Combine system and user sections into the final prompt string
        prompt = "\n".join(system_lines + user_lines)

        return prompt


__all__ = ["PromptBuilder"]
