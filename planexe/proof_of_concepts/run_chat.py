from planexe.llm_factory import get_llm
from llama_index.core.llms import ChatMessage

llm = get_llm("gemini-paid-flash-2.0")
# llm = get_llm("gemini-paid-flash-2.0")
# llm = get_llm("deepseek-chat")
# llm = get_llm("together-llama3.3")
# llm = get_llm("groq-gemma2")

messages = [
    ChatMessage(
        role="system", content="You are a pirate with a colorful personality"
    ),
    ChatMessage(role="user", content="What is your name"),
]
resp = llm.stream_chat(messages)

for r in resp:
    print(r.delta, end="")
