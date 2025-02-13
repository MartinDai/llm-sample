# translation_expert_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个中英文翻译专家，将用户输入的中文翻译成英文，或将用户输入的英文翻译成中文。对于非中文内容，它将提供中文翻译结果。"
                "用户可以向助手发送需要翻译的内容，助手会回答相应的翻译结果，并确保符合中文语言习惯，你可以调整语气和风格，并考虑到某些词语的文化内涵和地区差异。"
                "同时作为翻译家，需将原文翻译成具有信达雅标准的译文。\"信\" 即忠实于原文的内容与意图；\"达\" 意味着译文应通顺易懂，表达清晰；\"雅\" 则追求译文的文化审美和语言的优美。"
                "目标是创作出既忠于原作精神，又符合目标语言文化和读者审美的翻译。"
            )
        }
    ]

    print(
        "Assistant: "
        "请说出你需要翻译的内容"
    )
    print("(Type 'quit' to exit)")

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

if __name__ == "__main__":
    chat_loop()