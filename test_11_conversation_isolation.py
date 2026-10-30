from aichatclient import AICustom


def main():
    model_name = "mirbotai_1"

    history_a = AICustom.list_history(
        nickname=model_name,
        limit=100,
        conversation_id="test-chat-A",
        
    )

    history_b = AICustom.list_history(
        nickname=model_name,
        limit=100,
        conversation_id="test-chat-B",
        
    )

    print("Conversation A messages:", len(history_a))
    print("Conversation B messages:", len(history_b))

    if not history_a and not history_b:
        print(
            "\nBoth test conversations are empty. "
            "This is expected if they have never been used."
        )
    elif history_a and history_b:
        print("\nBoth conversations have history.")
    else:
        print("\nOnly one conversation has history.")


if __name__ == "__main__":
    main()