"""
Identify risks in the project plan.

As of 2025-03-03, the result is sensitive to what LLM is being used.
- Good `openrouter-paid-gemini-2.0-flash-001`.
- Bad `ollama-llama3.1`.

IDEA: assign uuid's to each risk. So later stages of the plan can refer to the risks by their uuid's.

PROMPT> python -m planexe.assume.identify_risks
"""
import json
import time
import logging
from math import ceil
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel, Field
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.llm import LLM

logger = logging.getLogger(__name__)

class LowMediumHigh(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class RiskItem(BaseModel):
    risk_area: str = Field(
        description="The category or domain of the risk, e.g., Regulatory, Financial, Technical."
    )
    risk_description: str = Field(
        description="A detailed explanation outlining the specific nature of the risk."
    )
    potential_impact: str = Field(
        description="Possible consequences or adverse effects on the project if the risk materializes."
    )
    likelihood: LowMediumHigh = Field(
        description="A qualitative measure (e.g., low, medium, high) indicating the probability that the risk will occur."
    )
    severity: LowMediumHigh = Field(
        description="A qualitative measure (e.g., low, medium, high) describing the extent of the potential negative impact if the risk occurs."
    )
    action: str = Field(
        description="Recommended mitigation strategies or steps to reduce the likelihood or impact of the risk."
    )

class DocumentDetails(BaseModel):
    risks: list[RiskItem] = Field(
        description="A list of identified project risks."
    )
    risk_assessment_summary: str = Field(
        description="Providing a high level context."
    )

IDENTIFY_RISKS_SYSTEM_PROMPT = """
You are a world-class planning expert with extensive experience in risk management for a wide range of projects, from small personal tasks to large-scale business ventures. Your objective is to identify potential risks that could jeopardize the success of a project based on its description. When analyzing the project plan, please consider and include the following aspects:

- **Risk Identification & Categorization:**  
  Analyze the project description thoroughly and identify risks across various domains such as Regulatory & Permitting, Technical, Financial, Environmental, Social, Operational, Supply Chain, and Security. Also consider integration with existing infrastructure, market or competitive risks (if applicable), and long-term sustainability. Be creative and consider even non-obvious factors.

- **Detailed Risk Descriptions:**  
  For each risk, provide a detailed explanation of what might go wrong and why it is a concern. Include aspects such as integration challenges with existing systems, maintenance difficulties, or long-term sustainability if relevant.

- **Quantification of Potential Impact:**  
  Where possible, quantify the potential impact. Include estimates of time delays (e.g., “a delay of 2–4 weeks”), financial overruns (e.g., “an extra cost of 5,000–10,000 in the project’s local currency”), and other measurable consequences. Use the appropriate currency or unit based on the project context.

- **Likelihood and Severity Assessments:**  
  Assess both the probability of occurrence (low, medium, high) and the potential severity of each risk (low, medium, high). Remember that even low-probability risks can have high severity.

- **Actionable Mitigation Strategies:**  
  For every identified risk, propose clear, actionable mitigation strategies. Explain how these steps can reduce either the likelihood or the impact of the risk.

- **Assumptions and Missing Information:**  
  If the project description is vague or key details are missing, explicitly note your assumptions and the potential impact of these uncertainties on the risk assessment.

- **Strategic Summary:**  
  Finally, provide a concise summary that highlights the 2–3 most critical risks that, if not properly managed, could significantly jeopardize the project’s success. Discuss any trade-offs or overlapping mitigation strategies.

Output your findings as a JSON object with the following structure:

{
  "risks": [
    {
      "risk_area": "The category or domain of the risk (e.g., Regulatory & Permitting)",
      "risk_description": "A detailed explanation outlining the specific nature of the risk.",
      "potential_impact": "Possible consequences or adverse effects on the project if the risk materializes, with quantifiable details where feasible.",
      "likelihood": "A qualitative measure (low, medium or high) indicating the probability that the risk will occur.",
      "severity": "A qualitative measure (low, medium or high) describing the potential negative impact if the risk occurs.",
      "action": "Recommended mitigation strategies or steps to reduce the likelihood or impact of the risk."
    },
    ...
  ],
  "risk_assessment_summary": "A concise summary of the overall risk landscape and the most critical risks."
}
"""

@dataclass
class IdentifyRisks:
    """
    Take a look at the vague plan description and identify risks.
    """
    system_prompt: str
    user_prompt: str
    response: dict
    metadata: dict
    markdown: str

    @classmethod
    def execute(cls, llm: LLM, user_prompt: str) -> 'IdentifyRisks':
        """
        Invoke LLM with the project description.
        """
        if not isinstance(llm, LLM):
            raise ValueError("Invalid LLM instance.")
        if not isinstance(user_prompt, str):
            raise ValueError("Invalid user_prompt.")

        logger.debug(f"User Prompt:\n{user_prompt}")

        system_prompt = IDENTIFY_RISKS_SYSTEM_PROMPT.strip()

        chat_message_list = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=system_prompt,
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=user_prompt,
            )
        ]

        sllm = llm.as_structured_llm(DocumentDetails)
        start_time = time.perf_counter()
        try:
            chat_response = sllm.chat(chat_message_list)
        except Exception as e:
            logger.debug(f"LLM chat interaction failed: {e}")
            logger.error("LLM chat interaction failed.", exc_info=True)
            raise ValueError("LLM chat interaction failed.") from e

        end_time = time.perf_counter()
        duration = int(ceil(end_time - start_time))
        response_byte_count = len(chat_response.message.content.encode('utf-8'))
        logger.info(f"LLM chat interaction completed in {duration} seconds. Response byte count: {response_byte_count}")

        json_response = chat_response.raw.model_dump()

        metadata = dict(llm.metadata)
        metadata["llm_classname"] = llm.class_name()
        metadata["duration"] = duration
        metadata["response_byte_count"] = response_byte_count

        markdown = cls.convert_to_markdown(chat_response.raw)

        result = IdentifyRisks(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=json_response,
            metadata=metadata,
            markdown=markdown
        )
        return result
    
    def to_dict(self, include_metadata=True, include_system_prompt=True, include_user_prompt=True) -> dict:
        d = self.response.copy()
        if include_metadata:
            d['metadata'] = self.metadata
        if include_system_prompt:
            d['system_prompt'] = self.system_prompt
        if include_user_prompt:
            d['user_prompt'] = self.user_prompt
        return d

    def save_raw(self, file_path: str) -> None:
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=2))

    @staticmethod
    def convert_to_markdown(document_details: DocumentDetails) -> str:
        """
        Convert the raw document details to markdown.
        """
        def format_lowmediumhigh(value: LowMediumHigh) -> str:
            return value.capitalize()
        
        rows = []

        if len(document_details.risks) > 0:
            for risk_index, risk_item in enumerate(document_details.risks, start=1):
                rows.append(f"\n## Risk {risk_index} - {risk_item.risk_area}")
                rows.append(risk_item.risk_description)
                rows.append(f"\n**Impact:** {risk_item.potential_impact}")
                rows.append(f"\n**Likelihood:** {format_lowmediumhigh(risk_item.likelihood)}")
                rows.append(f"\n**Severity:** {format_lowmediumhigh(risk_item.severity)}")
                rows.append(f"\n**Action:** {risk_item.action}")
        else:
            rows.append("No risks identified.")

        rows.append(f"\n## Risk summary\n{document_details.risk_assessment_summary}")
        return "\n".join(rows)

    def save_markdown(self, output_file_path: str):
        with open(output_file_path, 'w', encoding='utf-8') as out_f:
            out_f.write(self.markdown)

if __name__ == "__main__":
    from planexe.llm_factory import get_llm
    from planexe.plan.find_plan_prompt import find_plan_prompt

    llm = get_llm("gemini-paid-flash-2.0")

    plan_prompt = find_plan_prompt("4dc34d55-0d0d-4e9d-92f4-23765f49dd29")
    query = (
        f"{plan_prompt}\n\n"
        "Today's date:\n2025-Feb-27\n\n"
        "Project start ASAP"
    )
    print(f"Query: {query}")

    identify_risks = IdentifyRisks.execute(llm, query)
    json_response = identify_risks.to_dict(include_system_prompt=False, include_user_prompt=False)
    print("\n\nResponse:")
    print(json.dumps(json_response, indent=2))

    print(f"\n\nMarkdown:\n{identify_risks.markdown}")
