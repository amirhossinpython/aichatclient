from aichatclient import AICustom


def main():
    model_name = "mirbotai_1"

    models = AICustom.list_models()

    print("Saved models:", models)
    print("Model exists:", model_name in models)

    print(
        "delete_model available:",
        callable(getattr(AICustom, "delete_model", None)),
    )

    print("\nPre-check completed. No model was deleted.")


if __name__ == "__main__":
    main()