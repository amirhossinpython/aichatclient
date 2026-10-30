from aichatclient import AICustom


def main():
    models = AICustom.list_models()

    print("Saved models:")

    if not models:
        print("No saved models found.")
        return

    for model in models:
        print("-", model)

    if "mirbotai" in models:
        print("\nSUCCESS: mirbotai found!")
    else:
        print("\nWARNING: mirbotai was not found.")


if __name__ == "__main__":
    main()