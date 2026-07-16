"""
OpenAIService

Lightweight wrapper around the OpenAI Python SDK to provide a simple
ask(prompt: str) -> str function.

Features and constraints (per project requirements):
- Uses the modern OpenAI Python SDK (`from openai import OpenAI`).
- Reads API key from the repository `.env` file (via python-dotenv).
- Keeps the model name as a module-level constant.
- Does not write API keys into source code.
- Returns only a plain string answer from `ask()`.

Note: This module is defensive: it handles missing API key and runtime
errors gracefully and returns an explanatory string in case of failure.
"""

from pathlib import Path
import re
import os
import logging
from typing import Optional

from dotenv import load_dotenv

try:
    # Modern OpenAI Python SDK (recommended):
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore

# Model constant (change as required)
MODEL_NAME = "gpt-5-mini"


class OpenAIService:
    """Wrapper for OpenAI interactions.

    Usage:
        svc = OpenAIService()
        ans = svc.ask("광주에서 가볼만한 곳 추천해줘")
    """

    def __init__(self, model: str = MODEL_NAME, env_path: Optional[str] = None):
        # Determine .env path. Prefer backend/.env if it exists, otherwise
        # fall back to project root .env. An explicit env_path argument
        # overrides this behavior.
        this_dir = Path(__file__).resolve().parent
        project_root = this_dir.parent

        if env_path:
            env_file = Path(env_path)
        else:
            backend_env = this_dir / ".env"
            root_env = project_root / ".env"
            if backend_env.exists():
                env_file = backend_env
            else:
                env_file = root_env

        # Load environment variables from the chosen .env file (if present)
        if env_file and env_file.exists():
            load_dotenv(env_file)
            logging.info(f"Loaded .env from: {env_file}")
        else:
            # still call load_dotenv without path to allow default behaviors
            load_dotenv()

        self.model = model

        # Read API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")

        if OpenAI is None:
            logging.warning("OpenAI SDK not installed; OpenAIService will not function until installed.")

        if not self.api_key:
            logging.warning("OPENAI_API_KEY is not set in environment or .env; OpenAI calls will fail.")

        # Create client only if an API key is present and SDK is available.
        # If no API key is set, avoid instantiating the SDK to prevent
        # runtime errors. This makes the service safe to import in
        # environments without credentials.
        self.client = None
        if OpenAI is None:
            self.client = None
        else:
            if not self.api_key:
                # No API key; skip client creation but warn (already warned above)
                self.client = None
            else:
                try:
                    # ensure environment variable is set for the SDK
                    os.environ.setdefault("OPENAI_API_KEY", self.api_key)
                    self.client = OpenAI()
                except Exception as e:
                    logging.exception("Failed to initialize OpenAI client: %s", e)
                    self.client = None

    def ask(self, prompt: str, timeout: int = 15) -> str:
        """Send `prompt` to the OpenAI model and return the text response.

        Returns a plain string. In case of error, returns a short error message
        string rather than raising, to simplify caller logic.

        The function is intentionally minimal: prompt building/templating
        should be handled by other modules (PromptBuilder), per requirements.
        """
        if not prompt:
            return ""

        if self.client is None:
            return "OpenAI client is not available (SDK missing or init failed)."

        try:
            # Use the Responses API (modern SDK). Many OpenAI SDK versions
            # expose `client.responses.create(...)`. We call that and then try
            # to extract a human-readable string from the response object.
            resp = None
            try:
                resp = self.client.responses.create(model=self.model, input=prompt, timeout=timeout)
            except Exception:
                # Some SDK versions may provide chat completions instead.
                try:
                    resp = self.client.chat.completions.create(model=self.model, messages=[{"role": "user", "content": prompt}], timeout=timeout)
                except Exception as e:
                    logging.exception("OpenAI call failed: %s", e)
                    return "OpenAI request failed."

            # Normalize response into text. Different SDK responses have
            # slightly different shapes; attempt several known extraction
            # patterns safely.
            # Pattern A: Responses API -> resp.output -> list -> content -> list -> {"text": ...}
            try:
                out = getattr(resp, "output", None)
                if out and isinstance(out, list) and len(out) > 0:
                    first = out[0]
                    # first may be a dict-like or object with .get
                    content = None
                    if isinstance(first, dict):
                        cl = first.get("content")
                    else:
                        cl = getattr(first, "content", None)

                    if isinstance(cl, list) and len(cl) > 0:
                        # content elements can be dicts like {"type":"output_text","text":...}
                        for c in cl:
                            if isinstance(c, dict) and ("text" in c or "content" in c):
                                content = c.get("text") or c.get("content")
                                if content:
                                    break
                        if content:
                            return str(content)
                    elif isinstance(cl, str):
                        return cl
            except Exception:
                pass

            # Pattern B: chat completions -> resp.choices[0].message.content
            try:
                choices = getattr(resp, "choices", None) or (resp.get("choices") if isinstance(resp, dict) else None)
                if choices and len(choices) > 0:
                    first = choices[0]
                    # first may be dict or object
                    if isinstance(first, dict):
                        msg = first.get("message") or first.get("delta") or {}
                        if isinstance(msg, dict):
                            # message content could be string in 'content' or nested
                            content = msg.get("content")
                            if isinstance(content, str):
                                return content
                            # sometimes content is a list
                            if isinstance(content, list) and len(content) > 0:
                                c0 = content[0]
                                if isinstance(c0, dict) and "text" in c0:
                                    return c0.get("text")
                    else:
                        # try attribute access
                        msg = getattr(first, "message", None)
                        if msg:
                            text = getattr(msg, "content", None)
                            if isinstance(text, str):
                                return text
            except Exception:
                pass

            # Pattern C: resp is dict-like with 'output_text' or 'text'
            try:
                if isinstance(resp, dict):
                    if "output_text" in resp:
                        return resp["output_text"]
                    if "text" in resp:
                        return resp["text"]
            except Exception:
                pass

            # Last resort: stringify the object
            try:
                # Try to extract a text field from the stringified resp as a fallback
                s = str(resp)
                # common patterns: text='...' or "text": "..."
                m = re.search(r"text\s*=\s*'([\s\S]*?)'", s)
                if not m:
                    m = re.search(r'"text"\s*:\s*"([\s\S]*?)"', s)
                if m:
                    return m.group(1)
                return s
            except Exception:
                return "(empty response)"

        except Exception as e:
            logging.exception("Error while calling OpenAI: %s", e)
            return "An error occurred while contacting OpenAI."


__all__ = ["OpenAIService", "MODEL_NAME"]
