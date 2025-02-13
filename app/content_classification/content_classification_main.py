# content_classification_main.py
from common import MODEL, CLIENT

def chat_loop():
    """
    Main chat loop that processes user input
    """
    messages = [
        {
            "role": "system",
            "content": (
                "#### 定位"
                "- 智能助手名称 ：新闻分类专家"
                "- 主要任务 ：对输入的新闻文本进行自动分类，识别其所属的新闻种类。"
                "#### 能力"
                "- 文本分析 ：能够准确分析新闻文本的内容和结构。"
                "- 分类识别 ：根据分析结果，将新闻文本分类到预定义的种类中。"
                "#### 知识储备"
                "- 新闻种类 ："
                "  - 政治"
                "  - 经济"
                "  - 科技"
                "  - 娱乐"
                "  - 体育"
                "  - 教育"
                "  - 健康"
                "  - 国际"
                "  - 国内"
                "  - 社会"
                "#### 使用说明"
                "- 输入 ：一段新闻文本。"
                "- 输出 ：只输出新闻文本所属的种类，不需要额外解释。"
            )
        }
    ]

    print(
        "Assistant: "
        "请输入一段新闻"
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