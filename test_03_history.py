import os
from aichatclient import AICustom


def main():
    ai = AICustom.load_model(
        name="mirbotai",
        api_key= "",
    )

    print("Model:", ai.nickname)
    print("\n--- Chat history ---")

    history = ai.get_history(limit=100)

    if not history:
        print("No history found.")
        return

    for item in history:
        role = item.get("role", "unknown")
        content = item.get("content", "")
        print(f"\n[{role}] {content}")


if __name__ == "__main__":
    main()
