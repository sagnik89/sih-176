import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
import ollama


load_dotenv()


class OllamaClient:
    """Local Ollama client used as ORCA's fallback reasoning model."""

    def __init__(self):
        self.host = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434",
        )

        self.model = os.getenv(
            "OLLAMA_MODEL",
            "mistral:latest",
        )

        self.client: Optional[Any] = None

        try:
            self.client = ollama.Client(host=self.host)
        except Exception:
            self.client = None

    def is_available(self) -> bool:
        if self.client is None:
            return False

        try:
            self.client.list()
            return True
        except Exception:
            return False

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
    ) -> Dict[str, Any]:
        if self.client is None:
            return {
                "success": False,
                "error": "Ollama client could not be initialized.",
                "model": self.model,
            }

        try:
            messages = []

            if system_instruction:
                messages.append(
                    {
                        "role": "system",
                        "content": system_instruction,
                    }
                )

            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            response = self.client.chat(
                model=self.model,
                messages=messages,
            )

            message = response.get("message", {})
            text = message.get("content", "")

            if not text:
                return {
                    "success": False,
                    "error": "Ollama returned an empty response.",
                    "model": self.model,
                }

            return {
                "success": True,
                "text": text.strip(),
                "model": self.model,
                "provider": "ollama",
            }

        except Exception as exc:
            return {
                "success": False,
                "error": str(exc),
                "model": self.model,
                "provider": "ollama",
            }


ollama_client = OllamaClient()