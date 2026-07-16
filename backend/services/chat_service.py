"""
ChatService

This module composes three services to implement the chat flow:

- TravelSearchService: local place search from JSON files
- PromptBuilder: builds a prompt text given the user question and places
- OpenAIService: sends the prompt to OpenAI and returns a text answer

ChatService.ask(question: str) -> str provides the high-level business logic:
1. search local places for the question
2. build a prompt including the search results
3. call OpenAIService.ask(prompt)
4. return the answer (string)

The module is intentionally self-contained and defensive: failures in the
search or OpenAI call return readable error strings instead of raising.
"""

from typing import List, Dict
import logging

from backend.services.travel_search_service import TravelSearchService
from backend.services.openai_service import OpenAIService


class PromptBuilder:
    """Small helper to construct a prompt for the LLM.

    This builder is intentionally simple: it places a short instruction at the
    top, includes the user's original question, and appends a compact list of
    the local search results (title, address, category, phone).

    Keeping the prompt simple makes it easy to replace this class with a more
    advanced templating system later.
    """

    MAX_PLACES = 10

    @staticmethod
    def build_prompt(question: str, places: List[Dict], history: List[Dict] = None) -> str:
        """Return a prompt string built from `question` and `places`.

        - question: original user question
        - places: list of place dicts from TravelSearchService.search_places()
        - history: optional conversation history in the form
          [{"role":"user","content":"..."}, {"role":"assistant","content":"..."}, ...]
        """
        lines = []
        lines.append("You are a helpful travel assistant.")
        lines.append("Use the local place data provided to answer the user's question.")
        lines.append("")
        # If there is a conversation history, include it to provide context
        if history:
            lines.append("Conversation history:")
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                lines.append(f"- {role}: {content}")
            lines.append("")

        lines.append(f"User question: {question}")
        lines.append("")

        if not places:
            lines.append("Note: no local places matched the query. Answer using general knowledge.")
            return "\n".join(lines)

        lines.append(f"Here are up to {PromptBuilder.MAX_PLACES} relevant local places:")
        for idx, p in enumerate(places[: PromptBuilder.MAX_PLACES], start=1):
            title = p.get("title", "")
            address = p.get("address", "")
            category = p.get("category", "")
            phone = p.get("phone", "") or ""
            lines.append(f"{idx}. {title} | {category} | {address} | {phone}")

        lines.append("")
        lines.append("Provide a concise recommendation (2-3 short sentences) using the above local places when relevant.")
        lines.append("If none of the places are a good fit, explain briefly and provide alternatives.")

        return "\n".join(lines)


class ChatService:
    """High-level service that binds search, prompt building and OpenAI.

    The constructor lazily instantiates the underlying services. The
    ask(question) method orchestrates the flow and returns the final answer
    as a plain string. It does not perform prompt engineering beyond
    using PromptBuilder.
    """

    def __init__(self, *, local_dir: str = None, openai_env: str = None):
        # TravelSearchService loads local JSONs into memory
        self.search_service = TravelSearchService(local_dir=local_dir)

        # OpenAIService reads .env for API key; pass env path if required
        self.ai_service = OpenAIService(env_path=openai_env)

        # PromptBuilder is stateless; use its static method
        self.prompt_builder = PromptBuilder
        # In-memory conversation history. Each entry is {"role":"user"|"assistant","content":str}
        # We keep this in-memory only and cap to the most recent 10 messages.
        self.history: List[Dict] = []

    def ask(self, question: str) -> str:
        """Main orchestration method.

        Steps:
        1. Use TravelSearchService.search_places() to find local matches
        2. Build a prompt from the question and results
        3. Ask the OpenAIService and return the textual answer

        Any failures are caught and a readable error string is returned.
        """
        if not question or not question.strip():
            return "질문을 입력해 주세요."

        try:
            # 1) search local places
            places = self.search_service.search_places(question, max_results=10)
        except Exception as e:
            logging.exception("Error during local search: %s", e)
            places = []  # fallback to empty list

        try:
            # 2) update memory with the user's message, then build prompt including history
            # Append user message to history
            try:
                self.history.append({"role": "user", "content": question})
                # Keep only the last 10 messages
                if len(self.history) > 10:
                    self.history = self.history[-10:]
            except Exception:
                # non-fatal; proceed without mutating history
                pass

            prompt = self.prompt_builder.build_prompt(question, places, history=self.history)
        except Exception as e:
            logging.exception("Error building prompt: %s", e)
            return "문장을 생성하는 중 오류가 발생했습니다."

        try:
            # 3) call OpenAI
            answer = self.ai_service.ask(prompt)
            if answer is None:
                return "OpenAI로부터 응답을 받지 못했습니다."
            # Ensure the return value is a plain string
            ans_text = str(answer)

            # Append assistant reply to history and cap to last 10
            try:
                self.history.append({"role": "assistant", "content": ans_text})
                if len(self.history) > 10:
                    self.history = self.history[-10:]
            except Exception:
                # ignore history update failures
                pass

            return ans_text
        except Exception as e:
            logging.exception("Error calling OpenAIService: %s", e)
            return "OpenAI 호출 중 오류가 발생했습니다."


__all__ = ["ChatService", "PromptBuilder"]
