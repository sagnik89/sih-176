import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiClient:
    """Gemini client used as ORCA's primary reasoning model."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.1-flash-lite",
        )

        self.client: Optional[Any] = None

        if self.api_key and self.api_key != "your_key_here":
            self.client = genai.Client(api_key=self.api_key)

    def is_available(self) -> bool:
        return self.client is not None

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.client:
            return {
                "success": False,
                "error": "Gemini API key is not configured.",
                "model": self.model,
            }

        try:
            config = {}

            if system_instruction:
                config["system_instruction"] = system_instruction

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config or None,
            )

            text = getattr(response, "text", None)

            if not text:
                return {
                    "success": False,
                    "error": "Gemini returned an empty response.",
                    "model": self.model,
                }

            return {
                "success": True,
                "text": text.strip(),
                "model": self.model,
                "provider": "gemini",
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "model": self.model,
                "provider": "gemini",
            }


gemini_client = GeminiClient()