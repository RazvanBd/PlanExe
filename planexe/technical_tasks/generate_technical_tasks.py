"""
Generate technical task list from a project plan.

This module takes a project plan (from ProjectPlan) and WBS structure
and generates a list of language/framework-agnostic technical tasks
that developers can follow to build the application.
"""
import json
import time
import logging
from math import ceil
from uuid import uuid4
from dataclasses import dataclass
from pydantic import BaseModel, Field
from llama_index.core.llms.llm import LLM
from llama_index.core.llms import ChatMessage, MessageRole
from planexe.technical_tasks.technical_task import (
    TechnicalTask,
    TechnicalTaskList,
    AcceptanceCriteria,
    TaskExample
)

logger = logging.getLogger(__name__)


class GeneratedTaskList(BaseModel):
    """Structured output from LLM for generating technical tasks."""
    tasks: list[dict] = Field(
        description="List of technical tasks with all required details"
    )


TECHNICAL_TASKS_SYSTEM_PROMPT = """
You are an expert software architect and project planner tasked with breaking down project plans into actionable, language-agnostic technical tasks for developers.

Your goal is to generate a comprehensive list of technical tasks that:
1. Are completely agnostic of programming language and frameworks - focus on logical requirements and business logic
2. Can be followed sequentially by a developer to build the application
3. Include all necessary details: title, description, acceptance criteria, examples, dependencies, effort estimates, and implementation notes

For each task, you must provide:
- **title**: A clear, concise title (3-8 words) that describes what needs to be built
- **description**: A detailed description explaining:
  - What needs to be built and why
  - The business logic and requirements
  - Key technical considerations (without prescribing specific technologies)
  - How this task fits into the overall system
- **acceptance_criteria**: A list of 3-5 specific, testable conditions that define when the task is complete. Each criterion should be:
  - Specific and measurable
  - Testable (can be verified)
  - Focused on behavior and outcomes, not implementation details
- **examples**: 2-4 concrete examples that illustrate:
  - Expected behavior and edge cases
  - Sample inputs and outputs
  - Implementation approaches (conceptually, not code)
  - Common scenarios the feature should handle
- **dependencies**: List of other task numbers that must be completed first
- **estimated_effort**: Size estimate (Small: 1-4 hours, Medium: 4-16 hours, Large: 16+ hours, or X-Large: multiple days)
- **priority**: Priority level (High, Medium, Low) based on dependencies and criticality
- **tags**: Relevant tags for categorization (e.g., 'backend', 'frontend', 'database', 'api', 'authentication', 'data-model', 'business-logic', 'ui', 'validation', 'integration')
- **notes**: Additional implementation tips, considerations, security concerns, or references to relevant sections of the project plan

Guidelines:
- Break down complex features into smaller, manageable tasks
- Ensure tasks are logically ordered with clear dependencies
- Start with foundational tasks (data models, core logic) before building on them (APIs, UI, integrations)
- Each task should be independently testable
- Focus on WHAT needs to be built, not HOW (avoid language/framework specifics)
- Be comprehensive but practical - tasks should be completable within the estimated time
- Consider all aspects: data models, business logic, APIs, user interfaces, validation, error handling, security, testing
- Use clear, professional language that any developer can understand

Output format:
Generate a JSON object with a "tasks" array, where each task follows this structure:
{
  "title": "Task title",
  "description": "Detailed description...",
  "acceptance_criteria": [
    {"criterion": "Specific testable condition 1"},
    {"criterion": "Specific testable condition 2"}
  ],
  "examples": [
    {"title": "Example scenario", "description": "Detailed example..."}
  ],
  "dependencies": [],
  "estimated_effort": "Medium",
  "priority": "High",
  "tags": ["tag1", "tag2"],
  "notes": "Additional notes..."
}
"""


@dataclass
class GenerateTechnicalTasks:
    """
    Generate technical task list from project plan and WBS.
    """
    system_prompt: str
    user_prompt: str
    response: dict
    metadata: dict
    task_list: TechnicalTaskList

    @classmethod
    def execute(cls, llm: LLM, project_plan: dict, wbs_structure: dict = None) -> 'GenerateTechnicalTasks':
        """
        Generate technical tasks from a project plan and optional WBS structure.

        :param llm: An instance of LLM.
        :param project_plan: Dictionary containing the project plan (from ProjectPlan.to_dict())
        :param wbs_structure: Optional WBS structure for additional task context
        :return: An instance of GenerateTechnicalTasks.
        """
        if not isinstance(llm, LLM):
            raise ValueError("Invalid LLM instance.")
        if not isinstance(project_plan, dict):
            raise ValueError("Invalid project_plan.")

        system_prompt = TECHNICAL_TASKS_SYSTEM_PROMPT.strip()

        # Build user prompt from project plan
        user_prompt_parts = []
        user_prompt_parts.append("Generate a comprehensive technical task list for the following project:\n")
        
        # Extract key information from project plan
        if 'goal_statement' in project_plan:
            user_prompt_parts.append(f"**Project Goal:** {project_plan['goal_statement']}\n")
        
        if 'smart_criteria' in project_plan:
            smart = project_plan['smart_criteria']
            user_prompt_parts.append("\n**Project Requirements:**")
            user_prompt_parts.append(f"- Specific: {smart.get('specific', 'N/A')}")
            user_prompt_parts.append(f"- Measurable: {smart.get('measurable', 'N/A')}")
            user_prompt_parts.append(f"- Achievable: {smart.get('achievable', 'N/A')}")
            user_prompt_parts.append(f"- Relevant: {smart.get('relevant', 'N/A')}")
            user_prompt_parts.append(f"- Time-bound: {smart.get('time_bound', 'N/A')}\n")
        
        if 'dependencies' in project_plan and project_plan['dependencies']:
            user_prompt_parts.append("\n**Project Dependencies:**")
            for dep in project_plan['dependencies']:
                user_prompt_parts.append(f"- {dep}")
            user_prompt_parts.append("")
        
        if 'resources_required' in project_plan and project_plan['resources_required']:
            user_prompt_parts.append("\n**Resources Required:**")
            for resource in project_plan['resources_required']:
                user_prompt_parts.append(f"- {resource}")
            user_prompt_parts.append("")

        # Include WBS structure if available
        if wbs_structure:
            user_prompt_parts.append("\n**Work Breakdown Structure:**")
            user_prompt_parts.append(json.dumps(wbs_structure, indent=2))
            user_prompt_parts.append("")

        user_prompt_parts.append("\nGenerate a detailed, sequential list of technical tasks that will guide developers to build this application. Ensure tasks are language and framework agnostic, focusing on logical requirements and business functionality.")

        user_prompt = "\n".join(user_prompt_parts)

        logger.debug(f"System Prompt:\n{system_prompt}")
        logger.debug(f"User Prompt:\n{user_prompt}")

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

        sllm = llm.as_structured_llm(GeneratedTaskList)

        logger.debug("Starting LLM chat interaction for technical task generation.")
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

        # Convert LLM response to TechnicalTaskList
        project_name = project_plan.get('goal_statement', 'Unnamed Project')
        project_description = project_plan.get('smart_criteria', {}).get('specific', 'No description available')

        technical_tasks = []
        for i, task_data in enumerate(json_response.get('tasks', []), 1):
            task_id = str(uuid4())
            
            # Extract acceptance criteria
            acceptance_criteria = []
            for criterion_data in task_data.get('acceptance_criteria', []):
                if isinstance(criterion_data, dict):
                    acceptance_criteria.append(AcceptanceCriteria(criterion=criterion_data.get('criterion', '')))
                elif isinstance(criterion_data, str):
                    acceptance_criteria.append(AcceptanceCriteria(criterion=criterion_data))
            
            # Extract examples
            examples = []
            for example_data in task_data.get('examples', []):
                if isinstance(example_data, dict):
                    examples.append(TaskExample(
                        title=example_data.get('title', 'Example'),
                        description=example_data.get('description', '')
                    ))
            
            technical_task = TechnicalTask(
                id=task_id,
                title=task_data.get('title', f'Task {i}'),
                description=task_data.get('description', ''),
                acceptance_criteria=acceptance_criteria,
                examples=examples,
                dependencies=task_data.get('dependencies', []),
                estimated_effort=task_data.get('estimated_effort'),
                priority=task_data.get('priority'),
                tags=task_data.get('tags', []),
                notes=task_data.get('notes')
            )
            technical_tasks.append(technical_task)

        task_list = TechnicalTaskList(
            project_name=project_name,
            project_description=project_description,
            tasks=technical_tasks
        )

        result = GenerateTechnicalTasks(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response=json_response,
            metadata=metadata,
            task_list=task_list
        )
        logger.debug("GenerateTechnicalTasks instance created successfully.")
        return result

    def to_dict(self, include_metadata=True, include_user_prompt=True, include_system_prompt=True) -> dict:
        """Convert to dictionary representation."""
        d = self.task_list.to_dict()
        if include_metadata:
            d['metadata'] = self.metadata
        if include_user_prompt:
            d['user_prompt'] = self.user_prompt
        if include_system_prompt:
            d['system_prompt'] = self.system_prompt
        return d

    def save_raw(self, file_path: str) -> None:
        """Save raw response to JSON file."""
        d = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(d, indent=2))

    def save_markdown(self, output_file_path: str):
        """Save task list as markdown file."""
        self.task_list.save_markdown(output_file_path)


if __name__ == "__main__":
    import logging
    from planexe.llm_factory import get_llm
    from planexe.plan.project_plan import ProjectPlan
    from planexe.plan.find_plan_prompt import find_plan_prompt

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

    # Generate a simple project plan first
    plan_prompt = find_plan_prompt("4dc34d55-0d0d-4e9d-92f4-23765f49dd29")
    
    llm = get_llm("ollama-llama3.1")
    
    print("Generating project plan...")
    project_plan_result = ProjectPlan.execute(llm, plan_prompt)
    project_plan_dict = project_plan_result.to_dict(
        include_system_prompt=False, 
        include_user_prompt=False,
        include_metadata=False
    )
    
    print("\nGenerating technical tasks...")
    result = GenerateTechnicalTasks.execute(llm, project_plan_dict)
    
    print(f"\n\nGenerated {len(result.task_list.tasks)} technical tasks:")
    for i, task in enumerate(result.task_list.tasks, 1):
        print(f"\n{i}. {task.title}")
        print(f"   Priority: {task.priority}, Effort: {task.estimated_effort}")
        print(f"   Tags: {', '.join(task.tags)}")
    
    print(f"\n\nSaving to files...")
    result.save_raw("/tmp/technical_tasks.json")
    result.save_markdown("/tmp/technical_tasks.md")
    print("Saved to /tmp/technical_tasks.json and /tmp/technical_tasks.md")
