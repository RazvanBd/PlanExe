"""
Ping the LLM to check if it is running. Depends on the external dependencies: LlamaIndex + LlamaIndex-Gemini.
No use of PlanExe's llm_factory.
No use of Pydantic for structured output.

If you use venv:
PROMPT> python -m venv venv
PROMPT> source venv/bin/activate
(venv) PROMPT> pip install llama-index llama-index-llms-gemini
(venv) PROMPT> export GEMINI_API_KEY=your-gemini-api-key-here
(venv) PROMPT> python -m planexe.proof_of_concepts.run_ping_medium

If you use virtualenvwrapper, remove the virtualenv afterwards:
PROMPT> mkvirtualenv mypingenv --python=/usr/bin/python3.13
(mypingenv) PROMPT> pip install llama-index llama-index-llms-gemini
(mypingenv) PROMPT> export GEMINI_API_KEY=your-gemini-api-key-here
(mypingenv) PROMPT> python -m planexe.proof_of_concepts.run_ping_medium
(mypingenv) PROMPT> rm -rf ~/.virtualenvs/mypingenv
"""
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.gemini import Gemini
import os

model_name = "models/gemini-2.0-flash-exp"
gemini_api_key = os.getenv("GEMINI_API_KEY")

llm = Gemini(
    api_key=gemini_api_key,
    max_tokens=256,
    model=model_name,
)

messages = [
    ChatMessage(
        role=MessageRole.USER,
        content="List names of 3 planets in the solar system. Comma separated. No other text.",
    )
]
print("connecting to gemini...")
response = llm.chat(messages)
print(f"response:\n{response!r}")
