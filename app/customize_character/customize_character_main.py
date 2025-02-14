# customize_character_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "请你扮演一个刚从美国留学回国的人，说话时候会故意中文夹杂部分英文单词，显得非常fancy，对话中总是带有很强的优越感。"
            )
        }
    ]

    print(
        "Assistant: "
        "随便聊聊"
    )
    print("(Type 'quit' to exit)")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "quit":
                break

            messages.append({"role": "user", "content": user_input})
            try:
                stream_response = CLIENT.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    stream=True
                )

                print("\nAssistant:", end=" ", flush=True)
                collected_content = ""
                for chunk in stream_response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        print(content, end="", flush=True)
                        collected_content += content
                print()  # New line after streaming completes
                messages.append(
                    {
                        "role": "assistant",
                        "content": collected_content,
                    }
                )
            except Exception as e:
                print(
                    f"\nError chatting with the LM Studio server!\n\n"
                    f"Please ensure:\n"
                    f"1. LM Studio server is running at 127.0.0.1:1234 (hostname:port)\n"
                    f"2. Model '{MODEL}' is downloaded\n"
                    f"3. Model '{MODEL}' is loaded, or that just-in-time model loading is enabled\n\n"
                    f"Error details: {str(e)}\n"
                    "See https://lmstudio.ai/docs/basics/server for more information"
                )
                exit(1)
    except KeyboardInterrupt:
        print("\nYou have interrupted the program. Exiting gracefully...")

if __name__ == "__main__":
    chat_loop()