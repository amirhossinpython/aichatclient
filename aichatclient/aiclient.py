from __future__ import annotations
from typing import Optional
from .aicustom import AICustom


class AiClient:
    

    def __init__(self, ai: AICustom) -> None:
        self.ai = ai

    @classmethod
    def load_model(
        cls,
        name: str,
        *,
        api_key: Optional[str] = None,
        storage_dir: Optional[str] = None,
    ) -> "AiClient":
        """فراخوانی یک مدل از قبل ذخیره‌شده."""
        ai = AICustom.load_model(
            name,
            api_key=api_key,
            storage_dir=storage_dir,
        )
        return cls(ai)

    def chat(self, message: str) -> str:
        """ارسال پیام و دریافت پاسخ مدل."""
        return self.ai.chat(message)

    def get_history(self, limit: int = 100):
        """دریافت تاریخچه‌ی چت."""
        return self.ai.get_history(limit=limit)
