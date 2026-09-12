from typing import Any, Dict, Optional

from backend.ai.gemini import gemini_client
from backend.ai.ollama import ollama_client


class AIRouter:
    """Routes ORCA reasoning requests through Gemini with Ollama fallback."""

    def __init__(self):
        self.gemini = gemini_client
        self.ollama = ollama_client

    def generate(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Primary: Gemini
        if self.gemini.is_available():
            result = self.gemini.generate(
                prompt=prompt,
                system_instruction=system_instruction,
            )

            if result.get("success"):
                return result

        # Fallback: local Ollama
        if self.ollama.is_available():
            result = self.ollama.generate(
                prompt=prompt,
                system_instruction=system_instruction,
            )

            if result.get("success"):
                return result

        return {
            "success": False,
            "text": "",
            "provider": None,
            "model": None,
            "error": (
                "No AI reasoning provider is currently available. "
                "Configure Gemini or start Ollama."
            ),
        }

    def status(self) -> Dict[str, Any]:
        return {
            "gemini": {
                "configured": self.gemini.is_available(),
                "model": self.gemini.model,
            },
            "ollama": {
                "available": self.ollama.is_available(),
                "model": self.ollama.model,
            },
        }


ai_router = AIRouter()