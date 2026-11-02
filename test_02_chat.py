import os
from  aichatclient import AICustom


def main():
    print("=" * 45)
    print("TEST 02: LOAD SAVED MODEL AND CHAT")
    print("=" * 45)

    # کلید API را از محیط می‌خوانیم.
    api_key = ""

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    # مدل ذخیره‌شده در مرحله اول را بارگذاری می‌کنیم.
    # اینجا مدل جدیدی نمی‌سازیم.
    ai = AICustom.load_model(
        name="mirbotai",
        api_key=api_key,
        
        
        
    
    )
    print(ai._build_system_message(True))

    print("\n[OK] Saved model loaded.")
    print("Nickname:", ai.nickname)
    print("Model:", ai.model_name)
    print("Conversation:", ai.conversation_id)

    # چت تعاملی با همان مدل
    print("\nChat started. Type 'exit' to stop.\n")

    while True:
        message = input("You: ").strip()

        if message.lower() in ("exit", "quit"):
            break

        if not message:
            continue

        try:
            response = ai.chat(message)
            print(f"\nAssistant: {response}\n")

        except Exception as error:
            print(f"\nChat error: {error}\n")

    # نمایش تاریخچه همین گفتگو
    print("\n--- Conversation history ---")

    history = ai.get_history(limit=100)

    for item in history:
        print(
            f"[{item['role']}] {item['content']}"
        )

    print("\n[OK] Test finished.")


if __name__ == "__main__":
    main()
