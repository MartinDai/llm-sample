# prompt_generate_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "你是一位大模型提示词生成专家，请根据用户的需求编写一个智能助手的提示词，来指导大模型进行内容生成，要求："
                "1. 以 Markdown 格式输出"
                "2. 贴合用户需求，描述智能助手的定位、能力、知识储备"
                "3. 提示词应清晰、精确、易于理解，在保持质量的同时，尽可能简洁"
                "4. 只输出提示词，不要输出多余解释"
                "5. 必须使用中文输出"
            )
        }
    ]

    print(
        "Assistant: "
        "您好，请问您要生成关于什么领域的提示词"
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