import unittest
from planexe.technical_tasks.technical_task import (
    TechnicalTask,
    TechnicalTaskList,
    AcceptanceCriteria,
    TaskExample
)


class TestTechnicalTask(unittest.TestCase):
    def test_create_technical_task(self):
        """Test creating a technical task with all fields."""
        # Arrange & Act
        task = TechnicalTask(
            id="task-001",
            title="Implement User Authentication",
            description="Create a user authentication system that allows users to register and log in.",
            acceptance_criteria=[
                AcceptanceCriteria(criterion="Users can register with email and password"),
                AcceptanceCriteria(criterion="Users can log in with valid credentials"),
                AcceptanceCriteria(criterion="Invalid login attempts are rejected with clear error messages")
            ],
            examples=[
                TaskExample(
                    title="Successful Registration",
                    description="When a new user provides a valid email and password, they should be registered and receive a confirmation."
                ),
                TaskExample(
                    title="Failed Login",
                    description="When a user provides incorrect credentials, they should see an error message without revealing which field was incorrect."
                )
            ],
            dependencies=["task-000"],
            estimated_effort="Medium",
            priority="High",
            tags=["authentication", "backend", "security"],
            notes="Consider using industry-standard hashing algorithms for password storage."
        )

        # Assert
        self.assertEqual(task.id, "task-001")
        self.assertEqual(task.title, "Implement User Authentication")
        self.assertEqual(len(task.acceptance_criteria), 3)
        self.assertEqual(len(task.examples), 2)
        self.assertEqual(task.dependencies, ["task-000"])
        self.assertEqual(task.estimated_effort, "Medium")
        self.assertEqual(task.priority, "High")
        self.assertEqual(len(task.tags), 3)
        self.assertIsNotNone(task.notes)

    def test_technical_task_to_dict(self):
        """Test converting technical task to dictionary."""
        # Arrange
        task = TechnicalTask(
            id="task-002",
            title="Create Data Model",
            description="Define the core data structures.",
            acceptance_criteria=[
                AcceptanceCriteria(criterion="All entities are properly defined")
            ],
            examples=[
                TaskExample(title="Example", description="Sample data structure")
            ],
            priority="High"
        )

        # Act
        task_dict = task.to_dict()

        # Assert
        self.assertIn("id", task_dict)
        self.assertIn("title", task_dict)
        self.assertIn("description", task_dict)
        self.assertIn("acceptance_criteria", task_dict)
        self.assertIn("examples", task_dict)
        self.assertIn("priority", task_dict)
        self.assertEqual(task_dict["id"], "task-002")

    def test_technical_task_to_markdown(self):
        """Test converting technical task to markdown."""
        # Arrange
        task = TechnicalTask(
            id="task-003",
            title="Build API Endpoints",
            description="Create RESTful API endpoints for data access.",
            acceptance_criteria=[
                AcceptanceCriteria(criterion="All CRUD operations are supported"),
                AcceptanceCriteria(criterion="API returns proper HTTP status codes")
            ],
            examples=[
                TaskExample(
                    title="GET Request",
                    description="A GET request to /api/items should return all items."
                )
            ],
            estimated_effort="Large",
            priority="Medium",
            tags=["api", "backend"]
        )

        # Act
        markdown = task.to_markdown()

        # Assert
        self.assertIn("# Task: Build API Endpoints", markdown)
        self.assertIn("**ID:** task-003", markdown)
        self.assertIn("## Description", markdown)
        self.assertIn("## Acceptance Criteria", markdown)
        self.assertIn("## Examples", markdown)
        self.assertIn("Create RESTful API endpoints", markdown)
        self.assertIn("All CRUD operations are supported", markdown)

    def test_technical_task_minimal(self):
        """Test creating a minimal technical task."""
        # Arrange & Act
        task = TechnicalTask(
            id="task-004",
            title="Simple Task",
            description="A simple task",
            acceptance_criteria=[
                AcceptanceCriteria(criterion="Task is complete")
            ],
            examples=[]
        )

        # Assert
        self.assertEqual(task.id, "task-004")
        self.assertEqual(len(task.dependencies), 0)
        self.assertIsNone(task.estimated_effort)
        self.assertIsNone(task.priority)
        self.assertEqual(len(task.tags), 0)


class TestTechnicalTaskList(unittest.TestCase):
    def test_create_task_list(self):
        """Test creating a technical task list."""
        # Arrange
        task1 = TechnicalTask(
            id="task-1",
            title="Task 1",
            description="First task",
            acceptance_criteria=[AcceptanceCriteria(criterion="Completed")],
            examples=[]
        )
        task2 = TechnicalTask(
            id="task-2",
            title="Task 2",
            description="Second task",
            acceptance_criteria=[AcceptanceCriteria(criterion="Completed")],
            examples=[],
            dependencies=["task-1"]
        )

        # Act
        task_list = TechnicalTaskList(
            project_name="Test Project",
            project_description="A test project",
            tasks=[task1, task2]
        )

        # Assert
        self.assertEqual(task_list.project_name, "Test Project")
        self.assertEqual(len(task_list.tasks), 2)
        self.assertEqual(task_list.tasks[1].dependencies, ["task-1"])

    def test_task_list_to_dict(self):
        """Test converting task list to dictionary."""
        # Arrange
        task = TechnicalTask(
            id="task-1",
            title="Task 1",
            description="First task",
            acceptance_criteria=[AcceptanceCriteria(criterion="Done")],
            examples=[]
        )
        task_list = TechnicalTaskList(
            project_name="Project",
            project_description="Description",
            tasks=[task]
        )

        # Act
        task_list_dict = task_list.to_dict()

        # Assert
        self.assertIn("project_name", task_list_dict)
        self.assertIn("project_description", task_list_dict)
        self.assertIn("tasks", task_list_dict)
        self.assertEqual(len(task_list_dict["tasks"]), 1)

    def test_task_list_to_markdown(self):
        """Test converting task list to markdown."""
        # Arrange
        task = TechnicalTask(
            id="task-1",
            title="Implement Feature",
            description="A feature to implement",
            acceptance_criteria=[
                AcceptanceCriteria(criterion="Feature works as expected")
            ],
            examples=[
                TaskExample(title="Example", description="Example description")
            ],
            priority="High"
        )
        task_list = TechnicalTaskList(
            project_name="My Project",
            project_description="An awesome project",
            tasks=[task]
        )

        # Act
        markdown = task_list.to_markdown()

        # Assert
        self.assertIn("# Technical Task List: My Project", markdown)
        self.assertIn("An awesome project", markdown)
        self.assertIn("**Total Tasks:** 1", markdown)
        self.assertIn("## Task 1: Implement Feature", markdown)
        self.assertIn("**Priority:** High", markdown)


if __name__ == '__main__':
    unittest.main()
