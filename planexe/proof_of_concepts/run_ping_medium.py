"""
Ping the LLM to check if it is running. Depends on the external dependencies: LlamaIndex + LlamaIndex-OpenRouter.
No use of PlanExe's llm_factory.
No use of Pydantic for structured output.

If you use venv:
PROMPT> python -m venv venv
PROMPT> source venv/bin/activate
(venv) PROMPT> pip install llama-index llama-index-llms-openrouter
(venv) PROMPT> export OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
(venv) PROMPT> python -m planexe.proof_of_concepts.run_ping_medium

If you use virtualenvwrapper, remove the virtualenv afterwards:
PROMPT> mkvirtualenv mypingenv --python=/usr/bin/python3.13
(mypingenv) PROMPT> pip install llama-index llama-index-llms-openrouter
(mypingenv) PROMPT> export OPENROUTER_API_KEY=sk-or-v1-your-openrouter-api-key-here
(mypingenv) PROMPT> python -m planexe.proof_of_concepts.run_ping_medium
(mypingenv) PROMPT> rm -rf ~/.virtualenvs/mypingenv
"""
from llama_index.core.llms import ChatMessage, MessageRole
import os

model_name = "meta-llama/llama-3.3-8b-instruct:free"
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

llm = OpenRouter(
    api_key=openrouter_api_key,
    max_tokens=256,
    context_window=2048,
    model=model_name,
)

messages = [
    ChatMessage(
        role=MessageRole.USER,
        content="List names of 3 planets in the solar system. Comma separated. No other text.",
    )
]
print("connecting to openrouter...")
response = llm.chat(messages)
print(f"response:\n{response!r}")
