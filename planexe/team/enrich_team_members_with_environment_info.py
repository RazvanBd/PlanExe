"""
Enrich the team members with what kind of equipment and facilities they need for the task.

PROMPT> python -m planexe.team.enrich_team_members_with_environment_info
"""
import json
import time
import logging
from math import ceil
from dataclasses import dataclass
from pydantic import BaseModel, Field
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.llms.llm import LLM
from planexe.format_json_for_use_in_query import format_json_for_use_in_query

logger = logging.getLogger(__name__)

class TeamMember(BaseModel):
    """A human with domain knowledge."""
    id: int = Field(
        description="A unique id for the job_category."
    )
    equipment_needs: str = Field(
        description="What expensive resources are needed for the daily job."
    )
    facility_needs: str = Field(
        description="What facilities are needed for the daily job."
    )

class DocumentDetails(BaseModel):
    team_members: list[TeamMember] = Field(
        description="The experts with domain knowledge about the problem."
    )

ENRICH_TEAM_MEMBERS_ENVIRONMENT_INFO_SYSTEM_PROMPT = """
You are an expert at determining what equipment and facilities are needed for different job roles given a project description.

For each team member provided, identify the specific equipment and facilities they require to effectively perform their daily tasks within the context of the given project description. Provide concise but descriptive answers.
"""

@dataclass
class EnrichTeamMembersWithEnvironmentInfo:
    """
    Enrich each team member with more info.
    """
    system_prompt: str
    user_prompt: str
    response: dict
    metadata: dict
    team_member_list: list[dict]

    @classmethod
    def format_query(cls, job_description: str, team_member_list: list[dict]) -> str:
        if not isinstance(job_description, str):
            raise ValueError("Invalid job_description.")
        if not isinstance(team_member_list, list):
            raise ValueError("Invalid team_member_list.")

        query = (
            f"Project description:\n{job_description}\n\n"
            f"Here is the list of team members that needs to be enriched:\n{format_json_for_use_in_query(team_member_list)}"
        )
        return query

    @classmethod
    def execute(cls, llm: LLM, user_prompt: str, team_member_list: list[dict]) -> 'EnrichTeamMembersWithEnvironmentInfo':
        """
        Invoke LLM with each team member.
        """
        if not isinstance(llm, LLM):
            raise ValueError("Invalid LLM instance.")
        if not isinstance(user_prompt, str):
            raise ValueError("Invalid user_prompt.")
        if not isinstance(team_member_list, list):
            raise ValueError("Invalid team_member_list.")

        logger.debug(f"User Prompt:\n{user_prompt}")

        system_prompt = ENRICH_TEAM_MEMBERS_ENVIRONMENT_INFO_SYSTEM_PROMPT.strip()

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

        team_member_list_enriched = cls.cleanup_enriched_team_members_with_environment_info_and_merge_with_team_members(chat_response.raw, team_member_list)

        metadata = dict(llm.metadata)
        metadata["llm_classname"] = llm.class_name()
        metadata["duration"] = duration
        metadata["response_byte_count"] = response_byte_count

        result = EnrichTeamMembersWithEnvironmentInfo(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=json_response,
            metadata=metadata,
            team_member_list=team_member_list_enriched,
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

    def cleanup_enriched_team_members_with_environment_info_and_merge_with_team_members(document_details: DocumentDetails, team_member_list: list[dict]) -> list:
        result_team_member_list = team_member_list.copy()
        enriched_team_member_list = document_details.team_members
        id_to_enriched_team_member = {item.id: item for item in enriched_team_member_list}
        for team_member_index, team_member in enumerate(result_team_member_list):
            if 'id' not in team_member:
                logger.warning(f"Team member #{team_member_index} does not have an id")
                continue
            id = team_member['id']
            enriched_team_member = id_to_enriched_team_member.get(id)
            if enriched_team_member:
                team_member['equipment_needs'] = enriched_team_member.equipment_needs
                team_member['facility_needs'] = enriched_team_member.facility_needs
        return result_team_member_list

if __name__ == "__main__":
    from planexe.llm_factory import get_llm

    llm = get_llm("gemini-paid-flash-2.0")
    # llm = get_llm("deepseek-chat")

    job_description = "Establish a new police station in a high crime area."

    team_member_list = [
        {
            "id": 1,
            "category": "Law Enforcement",
            "explanation": "Police officers and detectives are essential for patrolling, investigation, and maintaining public safety."
        },
        {
            "id": 2,
            "category": "Administration",
            "explanation": "Administrative staff manage paperwork, scheduling, and coordination of police activities."
        },
        {
            "id": 3,
            "category": "Forensics",
            "explanation": "Forensic experts analyze crime scene evidence to support investigations."
        },
        {
            "id": 4,
            "category": "Community Relations",
            "explanation": "Officers or liaisons engage with the community to build trust and cooperation."
        }
    ]

    query = EnrichTeamMembersWithEnvironmentInfo.format_query(job_description, team_member_list)
    print(f"Query:\n{query}\n\n")

    enrich_team_members_with_environment_info = EnrichTeamMembersWithEnvironmentInfo.execute(llm, query, team_member_list)
    json_response = enrich_team_members_with_environment_info.to_dict(include_system_prompt=False, include_user_prompt=False)
    print(json.dumps(json_response, indent=2))

    print("\n\nTeam members:")
    json_team = enrich_team_members_with_environment_info.team_member_list
    print(json.dumps(json_team, indent=2))
