"""
Technical Task data model for representing developer tasks.

A technical task is a language/framework-agnostic unit of work that a developer
can follow to implement part of an application.
"""
from typing import Optional
from pydantic import BaseModel, Field


class AcceptanceCriteria(BaseModel):
    """Acceptance criteria for a technical task."""
    criterion: str = Field(
        description="A specific, testable condition that must be met for the task to be considered complete"
    )


class TaskExample(BaseModel):
    """Example for a technical task."""
    title: str = Field(
        description="Brief title of the example"
    )
    description: str = Field(
        description="Detailed description of the example scenario or implementation approach"
    )


class TechnicalTask(BaseModel):
    """
    Represents a single technical task for a developer to implement.
    
    Tasks are designed to be agnostic of programming language and frameworks,
    focusing on the logical implementation and business requirements.
    """
    id: str = Field(
        description="Unique identifier for the task"
    )
    title: str = Field(
        description="Clear, concise title that summarizes what needs to be built"
    )
    description: str = Field(
        description="Detailed description of the task, including context, purpose, and technical requirements. Should be comprehensive enough for a developer to understand what needs to be done without being prescriptive about implementation details."
    )
    acceptance_criteria: list[AcceptanceCriteria] = Field(
        description="List of specific, measurable conditions that must be met for the task to be considered complete"
    )
    examples: list[TaskExample] = Field(
        description="Examples that illustrate the expected behavior, edge cases, or implementation approaches"
    )
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of task IDs that must be completed before this task can be started"
    )
    estimated_effort: Optional[str] = Field(
        default=None,
        description="Estimated effort or time to complete the task (e.g., 'Small', 'Medium', 'Large', or '2-4 hours')"
    )
    priority: Optional[str] = Field(
        default=None,
        description="Priority level of the task (e.g., 'High', 'Medium', 'Low')"
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags or labels for categorizing the task (e.g., 'backend', 'frontend', 'database', 'api')"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes, considerations, or implementation tips"
    )

    def to_dict(self) -> dict:
        """Convert the technical task to a dictionary."""
        return self.model_dump(exclude_none=True)

    def to_markdown(self) -> str:
        """Convert the technical task to markdown format."""
        lines = []
        
        lines.append(f"# Task: {self.title}")
        lines.append("")
        lines.append(f"**ID:** {self.id}")
        
        if self.priority:
            lines.append(f"**Priority:** {self.priority}")
        
        if self.estimated_effort:
            lines.append(f"**Estimated Effort:** {self.estimated_effort}")
        
        if self.tags:
            lines.append(f"**Tags:** {', '.join(self.tags)}")
        
        lines.append("")
        lines.append("## Description")
        lines.append("")
        lines.append(self.description)
        lines.append("")
        
        if self.dependencies:
            lines.append("## Dependencies")
            lines.append("")
            for dep in self.dependencies:
                lines.append(f"- Task {dep}")
            lines.append("")
        
        lines.append("## Acceptance Criteria")
        lines.append("")
        for i, criterion in enumerate(self.acceptance_criteria, 1):
            lines.append(f"{i}. {criterion.criterion}")
        lines.append("")
        
        if self.examples:
            lines.append("## Examples")
            lines.append("")
            for example in self.examples:
                lines.append(f"### {example.title}")
                lines.append("")
                lines.append(example.description)
                lines.append("")
        
        if self.notes:
            lines.append("## Notes")
            lines.append("")
            lines.append(self.notes)
            lines.append("")
        
        return "\n".join(lines)


class TechnicalTaskList(BaseModel):
    """Collection of technical tasks for a project."""
    project_name: str = Field(
        description="Name of the project these tasks belong to"
    )
    project_description: str = Field(
        description="Brief description of the project"
    )
    tasks: list[TechnicalTask] = Field(
        description="List of technical tasks to be completed"
    )

    def to_dict(self) -> dict:
        """Convert the task list to a dictionary."""
        return self.model_dump()

    def to_markdown(self) -> str:
        """Convert the entire task list to markdown format."""
        lines = []
        
        lines.append(f"# Technical Task List: {self.project_name}")
        lines.append("")
        lines.append(self.project_description)
        lines.append("")
        lines.append(f"**Total Tasks:** {len(self.tasks)}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        for i, task in enumerate(self.tasks, 1):
            lines.append(f"## Task {i}: {task.title}")
            lines.append("")
            lines.append(f"**ID:** {task.id}")
            
            if task.priority:
                lines.append(f"**Priority:** {task.priority}")
            
            if task.estimated_effort:
                lines.append(f"**Estimated Effort:** {task.estimated_effort}")
            
            if task.tags:
                lines.append(f"**Tags:** {', '.join(task.tags)}")
            
            lines.append("")
            lines.append("### Description")
            lines.append("")
            lines.append(task.description)
            lines.append("")
            
            if task.dependencies:
                lines.append("### Dependencies")
                lines.append("")
                for dep in task.dependencies:
                    lines.append(f"- Task {dep}")
                lines.append("")
            
            lines.append("### Acceptance Criteria")
            lines.append("")
            for j, criterion in enumerate(task.acceptance_criteria, 1):
                lines.append(f"{j}. {criterion.criterion}")
            lines.append("")
            
            if task.examples:
                lines.append("### Examples")
                lines.append("")
                for example in task.examples:
                    lines.append(f"#### {example.title}")
                    lines.append("")
                    lines.append(example.description)
                    lines.append("")
            
            if task.notes:
                lines.append("### Notes")
                lines.append("")
                lines.append(task.notes)
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)

    def save_markdown(self, output_file_path: str):
        """Save the task list as a markdown file."""
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_markdown())
