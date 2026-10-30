from aichatclient import AICustom


def main():
    old_name = "mirbotai"
    new_name = "mirbotai_1"

    models = AICustom.list_models()

    if old_name not in models:
        print(f"ERROR: Model '{old_name}' not found.")
        print("Saved models:", models)
        return

    if new_name in models:
        print(f"ERROR: '{new_name}' already exists.")
        print("برای جلوگیری از تداخل، نام دیگری انتخاب کن.")
        return

    ai = AICustom.load_model(name=old_name,api_key="")

    print("Before rename:", AICustom.list_models())

    ai.rename_model(new_name)

    models_after = AICustom.list_models()
    print("After rename:", models_after)

    if new_name in models_after and old_name not in models_after:
        print("\nSUCCESS: Rename worked!")
    else:
        print("\nWARNING: Rename result needs checking.")


if __name__ == "__main__":
    main()
