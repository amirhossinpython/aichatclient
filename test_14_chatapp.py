import os
from aichatclient import AICustom, ChatApp


def main():
    api_key = "sk-hy24-u2h3TyQdaCr0wTwzlXMS3wc7FQsJWl_t_giauAYqMkQ"

    if not api_key:
        raise RuntimeError("متغیر OPENAI_API_KEY تنظیم نشده است.")

    # بارگذاری مدل ذخیره‌شده؛ مدل جدیدی ساخته نمی‌شود.
    ai = AICustom.load_model(
        name="mirbotai",
        api_key=api_key,
    )

    print("Loaded model:", ai.nickname)
    print("Model name:", ai.model_name)
    print("Base URL:", ai.base_url)

    # تحویل همان نمونه به ChatApp
    web_chat = ChatApp(ai=ai)

    # تأیید می‌کنیم که هر دو از یک نمونه استفاده می‌کنند.
    assert web_chat.ai is ai

    print("\nSUCCESS: ChatApp is using the existing AICustom instance.")

    web_chat.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
    )


if __name__ == "__main__":
    main()