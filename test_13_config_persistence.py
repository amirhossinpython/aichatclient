from aichatclient import AICustom


def main():
    ai = AICustom.load_model(name="mirbotai_1",api_key="")

    print("Nickname:", ai.nickname)
    print("Provider:", ai.model_provider)
    print("Model:", ai.model_name)
    print("Base URL:", ai.base_url)
    print("Memory:", ai.memory)
    print("History limit:", ai.history_limit)
    print("Timeout:", ai.timeout)
    print("Max retries:", ai.max_retries)

    expected_base_url = "https://houshyar24.ir/api/openai/v1"

    if ai.base_url.rstrip("/") == expected_base_url:
        print("\nSUCCESS: Base URL is correct.")
    else:
        print("\nWARNING: Base URL differs from expected value.")

    print("\nConfig check completed. No settings were changed.")


if __name__ == "__main__":
    main()
