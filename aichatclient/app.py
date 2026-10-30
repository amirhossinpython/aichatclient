from typing import Any, Optional
from flask import Flask, render_template, request, jsonify
from .aicustom import AICustom
from pathlib import Path

class ChatApp:
    """وب‌اپ Flask برای چت با یک نمونهٔ شخصی‌سازی‌شده از AICustom."""

    def __init__(
        self,
        ai: Optional[AICustom] = None,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        system_prompt: str = "",
        model: str = "openai/gpt-4o-mini",
        nickname: Optional[str] = None,
        model_provider: str = "",
        model_version: str = "",
        author: str = "",
        dataset: Optional[str] = None,
        personality: Optional[str] = None,
        limitations: Optional[str] = None,
        expertise: Optional[str] = None,
        memory: bool = True,
        conversation_id: str = "default",
        storage_dir: Optional[str] = None,
        history_limit: int = 40,
        timeout: float = 60.0,
        max_retries: int = 2,
        extra_model_params: Optional[dict[str, Any]] = None,
        model_id: Optional[str] = None,
        template_folder: Optional[str] = None,
    ) -> None:
        """
        ساخت وب‌اپ با نمونهٔ آمادهٔ AICustom یا ساخت نمونهٔ جدید.

        اگر ai داده شود، همان نمونه و تنظیمات آن استفاده می‌شود.
        در غیر این صورت، تنظیمات برای ساخت یک AICustom جدید به کار می‌روند.
        """

        if ai is not None:
            self.ai = ai
        else:
            if not api_key:
                raise ValueError(
                    "برای ساخت AICustom جدید باید api_key را وارد کنید "
                    "یا یک نمونهٔ آماده با پارامتر ai بدهید."
                )

            self.ai = AICustom(
                api_key=api_key,
                base_url=base_url,
                system_prompt=system_prompt,
                model_provider=model_provider,
                model_name=model,
                model_version=model_version,
                nickname=nickname or model.replace("/", "_"),
                author=author,
                dataset=dataset,
                personality=personality,
                limitations=limitations,
                expertise=expertise,
                memory=memory,
                conversation_id=conversation_id,
                storage_dir=storage_dir,
                history_limit=history_limit,
                timeout=timeout,
                max_retries=max_retries,
                extra_model_params=extra_model_params,
                model_id=model_id,
            )

        self.app = Flask(
            
    __name__,
    template_folder=str(Path(__file__).resolve().parent / "templates"),
    static_folder=str(Path(__file__).resolve().parent / "static"),
)
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")

        @self.app.route("/chat", methods=["POST"])
        def chat():
            data = request.get_json(silent=True)

            if not isinstance(data, dict):
                return jsonify({"error": "درخواست JSON معتبر نیست"}), 400

            message = data.get("message")

            if not isinstance(message, str) or not message.strip():
                return jsonify({"error": "پیام خالی است"}), 400

            try:
                response = self.ai.chat(message.strip())
                return jsonify({"response": response}), 200
            except Exception:
                self.app.logger.exception("خطا هنگام پردازش پیام")
                return jsonify(
                    {"error": "هنگام دریافت پاسخ از هوش مصنوعی خطایی رخ داد"}
                ), 500

    def run(
        self,
        host: str = "127.0.0.1",
        port: int = 5000,
        debug: bool = False,
    ) -> None:
        """اجرای وب‌اپ."""

        print(
            f"وب‌اپ چت در http://{host}:{port} اجرا می‌شود."
        )
        print(f"مدل فعال: {self.ai.model_name}")
        self.app.run(host=host, port=port, debug=debug)
