import os
from aichatclient import AICustom


def main():
    ai = AICustom.load_model(
        name="mirbotai",
        api_key="",
    )

    response = ai.chat(
        "هوش مصنوعی را در یک جمله توضیح بده.",
        short=True,
    )

    print("Model:", ai.nickname)
    print("Short response:", response)


if __name__ == "__main__":
    main()
