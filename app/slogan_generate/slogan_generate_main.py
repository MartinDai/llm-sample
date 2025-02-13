# slogan_generate_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个宣传标语专家，请根据用户需求设计一个独具创意且引人注目的宣传标语，需结合该产品/活动的核心价值和特点，同时融入新颖的表达方式或视角。"
                "请确保标语能够激发潜在客户的兴趣，并能留下深刻印象，可以考虑采用比喻、双关或其他修辞手法来增强语言的表现力。"
                "标语应简洁明了，需要朗朗上口，易于理解和记忆，一定要押韵，不要太过书面化。"
                "只输出宣传标语，不用解释。"
            )
        }
    ]

    print(
        "Assistant: "
        "请问你需要什么产品/活动的宣传标语"
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