from aichatclient import AICustom


def main():
    model_name = "mirbotai_1"

    models = AICustom.list_models()
    print("Saved models:", models)

    if model_name not in models:
        print(f"ERROR: {model_name} not found.")
        return

    ai = AICustom.load_model(name=model_name,api_key="")

    history = ai.get_history(limit=100)

    print(f"\nHistory for {model_name}:")
    print("Messages found:", len(history))

    for item in history:
        role = item.get("role", "unknown")
        content = item.get("content", "")
        print(f"\n[{role}] {content}")

    if history:
        print("\nSUCCESS: History is available.")
    else:
        print("\nNo history found for this model/conversation.")


if __name__ == "__main__":
    main()
