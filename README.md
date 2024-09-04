Task Manager

This project is a simple task management system that allows an IT company to manage positions, task types, tasks, and workers. The system provides views for listing, creating, updating, and deleting records for each model.

Models
Position
Represents the job positions within the company.

Fields:

name: The name of the position (e.g., Developer, QA).
Meta Options:

ordering: Orders the positions by name.
Methods:

__str__(): Returns the name of the position.

TaskType
Represents the different types of tasks within the company.

Fields:

name: The name of the task type (e.g., Bug, New Feature).
Meta Options:

ordering: Orders the task types by name.
Methods:

__str__(): Returns the name of the task type.

Task
Represents a task assigned to one or more workers.

Fields:

name: The name of the task.
description: A detailed description of the task.
deadline: The deadline for the task.
is_completed: A boolean indicating whether the task is completed.
priority: The priority of the task. Choices include Low, Medium, High, and Urgent.
task_type: A foreign key linking to TaskType.
assignees: A many-to-many relationship with Worker.
Meta Options:

ordering: Orders the tasks by deadline.
Methods:

get_absolute_url(): Returns the absolute URL for the task detail view.
__str__(): Returns a string representation of the task, including its name, priority, completion status, and deadline.

Worker
Represents a user (worker) in the system.

Fields:

position: A foreign key linking to Position.
Meta Options:

ordering: Orders the workers by username.
verbose_name: Customizes the display name of the model in the admin interface.
verbose_name_plural: Customizes the plural display name of the model in the admin interface.
Methods:

get_absolute_url(): Returns the absolute URL for the worker detail view.
__str__(): Returns the username and position of the worker.

URLs
The app name is task_manager. The following are the main URL patterns used in the project:

Positions:

position-list: List all positions.
position-create: Create a new position.
position-update: Update an existing position.
position-delete: Delete a position.

Task Types:

task-type-list: List all task types.
task-type-create: Create a new task type.
task-type-update: Update an existing task type.
task-type-delete: Delete a task type.

Tasks:

task-list: List all tasks.
task-detail: View details of a specific task.
task-create: Create a new task.
task-update: Update an existing task.
task-delete: Delete a task.
task-update-assignee: Update the assignee(s) of a task.

Workers:

worker-list: List all workers.
worker-detail: View details of a specific worker.
worker-sign-up: Sign up a new worker.
worker-create: Create a new worker.
worker-update: Update an existing worker's position.
worker-delete: Delete a worker.

Views
The project uses class-based views (CBVs) and function-based views (FBVs) for different functionalities.

Position Views:

PositionListView: Lists all positions.
PositionCreateView: Allows the creation of a new position.
PositionUpdateView: Allows updating an existing position.
PositionDeleteView: Allows deleting a position.

Task Type Views:

TaskTypeListView: Lists all task types.
TaskTypeCreateView: Allows the creation of a new task type.
TaskTypeUpdateView: Allows updating an existing task type.
TaskTypeDeleteView: Allows deleting a task type.

Task Views:

TaskListView: Lists all tasks.
TaskDetailView: Displays details of a specific task.
TaskCreateView: Allows the creation of a new task.
TaskUpdateView: Allows updating an existing task.
TaskDeleteView: Allows deleting a task.

Worker Views:

WorkerListView: Lists all workers.
WorkerDetailView: Displays details of a specific worker.
WorkerSignUPView: Allows a new worker to sign up.
WorkerCreateView: Allows creating a new worker.
WorkerUpdatePositionView: Allows updating a worker's position.
WorkerDeleteView: Allows deleting a worker.

Index View:

index: The homepage of the app, displaying statistics like the number of positions, task types, tasks, and workers, as well as the number of visits.

Forms
The project includes several forms for searching and managing data:

PositionSearchForm: A form for searching positions by name.
TaskTypeSearchForm: A form for searching task types by name.
TaskForm: A form for creating or updating tasks, including fields for name, description, deadline, completion status, priority, and task type.
TaskSearchForm: A form for searching tasks by name.
WorkerCreationForm: A form for creating new workers, including fields for first name, last name, and position.
WorkerPositionUpdateForm: A form for updating a worker's position.
WorkerSearchForm: A form for searching workers by username.

This README provides an overview of the key components of the project, including the models, URLs, views, and forms. It serves as a guide for understanding the structure and functionality of the task management system.
