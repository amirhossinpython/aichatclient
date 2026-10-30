import os
from aichatclient import AICustom


def main():
    ai = AICustom.load_model(
        name="mirbotai",
        api_key="sk-hy24-u2h3TyQdaCr0wTwzlXMS3wc7FQsJWl_t_giauAYqMkQ",
    )

    print(f"Model: {ai.nickname}")
    print("Memory test started.\n")

    first_message = (
        "اسم رمز آزمایشی من آبی-۷۲ است. "
        "در پیام بعدی از تو می‌پرسم اسم رمز چه بود. "
        "اگر این پیام را دریافت کردی، فقط بگو ثبت شد."
    )

    print("You:", first_message)
    print("Assistant:", ai.chat(first_message))

    second_message = "اسم رمز آزمایشی من چه بود؟"
    print("\nYou:", second_message)
    print("Assistant:", ai.chat(second_message))


if __name__ == "__main__":
    main()