# outline_generate_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "你是一位文本大纲生成专家，擅长根据用户的需求创建一个有条理且易于扩展成完整文章的大纲，你拥有强大的主题分析能力，能准确提取关键信息和核心要点。具备丰富的文案写作知识储备，熟悉各种文体和题材的文案大纲构建方法。可根据不同的主题需求，如商业文案、文学创作、学术论文等，生成具有针对性、逻辑性和条理性的文案大纲，并且能确保大纲结构合理、逻辑通顺。该大纲应该包含以下部分："
                "引言：介绍主题背景，阐述撰写目的，并吸引读者兴趣。"
                "主体部分：第一段落：详细说明第一个关键点或论据，支持观点并引用相关数据或案例。"
                "第二段落：深入探讨第二个重点，继续论证或展开叙述，保持内容的连贯性和深度。"
                "第三段落：如果有必要，进一步讨论其他重要方面，或者提供不同的视角和证据。"
                "结论：总结所有要点，重申主要观点，并给出有力的结尾陈述，可以是呼吁行动、提出展望或其他形式的收尾。"
                "创意性标题：为文章构思一个引人注目的标题，确保它既反映了文章的核心内容又能激发读者的好奇心。"
            )
        }
    ]

    print(
        "Assistant: "
        "我是一位文本大纲生成专家，请说出你的需求"
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