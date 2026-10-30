from aichatclient import AICustom


def main():
    ai = AICustom.load_model(name="mirbotai_1",api_key="sk-hy24-u2h3TyQdaCr0wTwzlXMS3wc7FQsJWl_t_giauAYqMkQ")

    print("Model:", ai.nickname)
    print("Conversation ID:", getattr(ai, "conversation_id", "Not available"))

    history = ai.get_history(limit=100)
    print("Messages in current conversation:", len(history))

    print("\nConversation IDs supported by this instance:")
    print("Attribute exists:", hasattr(ai, "conversation_id"))


if __name__ == "__main__":
    main()