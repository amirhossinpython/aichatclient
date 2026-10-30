import os
from aichatclient import AICustom


def main():
    api_key = ""
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY تنظیم نشده است.")

    # همان مدل ذخیره‌شده را بارگذاری می‌کنیم؛ مدل جدید نمی‌سازیم.
    ai = AICustom.load_model(
        name="mirbotai",
        api_key=api_key,
    )

    # دیتاست را برای همین اجرای تست تنظیم می‌کنیم.
    ai.dataset = "mirbot_dataset.txt"

    question = "طبق فایل اطلاعاتی، سازنده پروژه MirBot کیست؟"

    print("Model:", ai.nickname)
    print("Question:", question)

    response = ai.chat(question)
    print("Answer:", response)


if __name__ == "__main__":
    main()
