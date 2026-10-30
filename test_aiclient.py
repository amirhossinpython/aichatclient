from aichatclient import AiClient

client = AiClient.load_model(
    name="mirbotai",
    api_key="",
)

while True:
    message = input("شما: ")

    if message.strip().lower() in ("exit", "quit", "خروج"):
        break

    try:
        response = client.chat(message)
        print("MirBot:", response)
    except Exception as e:
        print("خطا:", e)
