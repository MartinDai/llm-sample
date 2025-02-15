# fetch_wikipedia_main.py
import shutil
import json
from common import Spinner, MODEL, CLIENT
from function import wikipedia

def chat_loop():
    """
    Main chat loop that processes user input and handles tool calls.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that can retrieve Wikipedia articles. "
                "When asked about a topic, you can retrieve Wikipedia articles "
                "and cite information from them."
            ),
        }
    ]

    print(
        "Assistant: "
        "Hi! I can access Wikipedia to help answer your questions about history, "
        "science, people, places, or concepts - or we can just chat about "
        "anything else!"
    )
    print("(Type 'quit' to exit)")

    try:
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "quit":
                break

            messages.append({"role": "user", "content": user_input})
            try:
                with Spinner("Thinking..."):
                    response = CLIENT.chat.completions.create(
                        model=MODEL,
                        messages=messages,
                        tools=[wikipedia.WIKI_TOOL],
                    )

                if response.choices[0].message.tool_calls:
                    # Handle all tool calls
                    tool_calls = response.choices[0].message.tool_calls

                    # Add all tool calls to messages
                    messages.append(
                        {
                            "role": "assistant",
                            "tool_calls": [
                                {
                                    "id": tool_call.id,
                                    "type": tool_call.type,
                                    "function": tool_call.function,
                                }
                                for tool_call in tool_calls
                            ],
                        }
                    )

                    # Process each tool call and add results
                    for tool_call in tool_calls:
                        args = json.loads(tool_call.function.arguments)
                        result = wikipedia.fetch_content(args["search_query"])

                        # Print the Wikipedia content in a formatted way
                        terminal_width = shutil.get_terminal_size().columns
                        print("\n" + "=" * terminal_width)
                        if result["status"] == "success":
                            print(f"\nWikipedia article: {result['title']}")
                            print("-" * terminal_width)
                            print(result["content"])
                        else:
                            print(
                                f"\nError fetching Wikipedia content: {result['message']}"
                            )
                        print("=" * terminal_width + "\n")

                        messages.append(
                            {
                                "role": "tool",
                                "content": json.dumps(result),
                                "tool_call_id": tool_call.id,
                            }
                        )

                    # Stream the post-tool-call response
                    print("\nAssistant:", end=" ", flush=True)
                    stream_response = CLIENT.chat.completions.create(
                        model=MODEL, messages=messages, stream=True
                    )
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
                else:
                    # Handle regular response
                    print("\nAssistant:", response.choices[0].message.content)
                    messages.append(
                        {
                            "role": "assistant",
                            "content": response.choices[0].message.content,
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