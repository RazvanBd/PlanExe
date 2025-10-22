# Technical Task List Generator

This module generates language and framework-agnostic technical task lists from project plans. It's designed to help developers build applications by providing detailed, sequential tasks with clear requirements and acceptance criteria.

## Overview

The Technical Task List Generator takes a project plan (from `ProjectPlan`) and optionally a Work Breakdown Structure (WBS) and generates a comprehensive list of development tasks. Each task includes:

- **Title**: Clear, concise description of what needs to be built
- **Description**: Detailed explanation including context, purpose, and technical requirements
- **Acceptance Criteria**: Specific, testable conditions that define completion
- **Examples**: Concrete scenarios, edge cases, and sample implementations
- **Dependencies**: Links to prerequisite tasks
- **Estimated Effort**: Size estimate (Small, Medium, Large, X-Large)
- **Priority**: Importance level (High, Medium, Low)
- **Tags**: Categorization labels (backend, frontend, database, api, etc.)
- **Notes**: Additional implementation tips and considerations

## Usage

### Basic Usage

```python
from planexe.llm_factory import get_llm
from planexe.plan.project_plan import ProjectPlan
from planexe.technical_tasks.generate_technical_tasks import GenerateTechnicalTasks

# Generate a project plan first
llm = get_llm("ollama-llama3.1")
project_plan_result = ProjectPlan.execute(llm, "Build a todo list application")
project_plan_dict = project_plan_result.to_dict(
    include_system_prompt=False, 
    include_user_prompt=False,
    include_metadata=False
)

# Generate technical tasks from the plan
technical_tasks = GenerateTechnicalTasks.execute(
    llm=llm,
    project_plan=project_plan_dict
)

# Access the generated tasks
for task in technical_tasks.task_list.tasks:
    print(f"Task: {task.title}")
    print(f"Priority: {task.priority}, Effort: {task.estimated_effort}")
    print(f"Acceptance Criteria: {len(task.acceptance_criteria)} items")
```

### Saving Output

```python
# Save as JSON
technical_tasks.save_raw("output/technical_tasks.json")

# Save as Markdown
technical_tasks.save_markdown("output/technical_tasks.md")
```

### Integration with Pipeline

The technical task generator is integrated into the PlanExe pipeline as `TechnicalTasksTask`. When running the full pipeline, technical tasks are automatically generated and included in the final report.

Files generated:
- `029-1-technical_tasks_raw.json` - Raw JSON output
- `029-2-technical_tasks.md` - Markdown formatted task list

## Data Models

### TechnicalTask

Represents a single development task with all necessary details for implementation.

```python
from planexe.technical_tasks.technical_task import TechnicalTask, AcceptanceCriteria, TaskExample

task = TechnicalTask(
    id="unique-id",
    title="Implement User Authentication",
    description="Create a user authentication system...",
    acceptance_criteria=[
        AcceptanceCriteria(criterion="Users can register with email and password"),
        AcceptanceCriteria(criterion="Users can log in with valid credentials")
    ],
    examples=[
        TaskExample(
            title="Successful Registration",
            description="When a user provides valid credentials..."
        )
    ],
    dependencies=["task-001"],
    estimated_effort="Medium",
    priority="High",
    tags=["authentication", "backend", "security"],
    notes="Consider industry-standard hashing algorithms"
)
```

### TechnicalTaskList

Collection of tasks for a complete project.

```python
from planexe.technical_tasks.technical_task import TechnicalTaskList

task_list = TechnicalTaskList(
    project_name="My Application",
    project_description="A comprehensive application",
    tasks=[task1, task2, task3]
)

# Convert to markdown
markdown_output = task_list.to_markdown()

# Save to file
task_list.save_markdown("tasks.md")
```

## Design Principles

### Language and Framework Agnostic

Tasks focus on **what** needs to be built, not **how** to build it:

✅ Good: "Implement user authentication with email and password"
❌ Bad: "Use bcrypt with Node.js to hash passwords in MongoDB"

✅ Good: "Create a data model for user profiles with fields for name, email, and preferences"
❌ Bad: "Create a User class in Python with SQLAlchemy ORM"

### Sequential and Logical

Tasks are ordered to follow natural development flow:
1. Data models and core structures
2. Business logic and processing
3. APIs and interfaces
4. User interfaces
5. Integrations and external services

### Complete and Testable

Each task includes:
- Clear acceptance criteria that can be verified
- Examples showing expected behavior
- Dependencies to ensure proper ordering
- Enough detail for independent implementation

## Testing

Run the test suite:

```bash
python -m unittest planexe.technical_tasks.tests.test_technical_task
```

## Examples

### Simple Project

For a simple "Make a cup of coffee" task:
- Title: "Prepare Coffee Ingredients"
- Description: "Gather instant coffee, hot water, and optional milk/sugar"
- Acceptance Criteria: ["All required ingredients are available", "Water is heated to appropriate temperature"]

### Complex Project

For a complex "E-commerce Platform" project:
- Task 1: "Design Product Data Model" (Small, High Priority)
- Task 2: "Implement Shopping Cart Logic" (Medium, High Priority, depends on Task 1)
- Task 3: "Create Payment Processing Interface" (Large, High Priority, depends on Task 2)
- Task 4: "Build Product Catalog UI" (Medium, Medium Priority, depends on Task 1)

## Architecture

```
planexe/technical_tasks/
├── __init__.py
├── README.md                      # This file
├── technical_task.py              # Data models for tasks
├── generate_technical_tasks.py    # LLM-based task generation
└── tests/
    ├── __init__.py
    └── test_technical_task.py     # Unit tests
```

The generator uses the LLM to:
1. Analyze the project plan and requirements
2. Break down the project into logical, sequential tasks
3. Generate detailed task specifications
4. Ensure tasks are properly ordered with dependencies

## Contributing

When adding new features:
1. Keep tasks language/framework agnostic
2. Ensure all tasks have complete information (title, description, acceptance criteria, examples)
3. Maintain logical task ordering with proper dependencies
4. Add tests for new functionality
5. Update documentation
