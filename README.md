# Student Activity Platform API

The **Student Activity Platform API** is a backend service built with FastAPI. This API provides a comprehensive system to manage various aspects of student activities. It includes functionalities for user management, division creation, announcements, meetings, assignments, excuses, feedback, and submissions, along with a robust permission system.

## Features

- **User Management**: Manage user profiles, roles, and permissions.
- **Divisions**: Create and manage divisions within the platform.
- **Announcements**: Post and manage announcements for students.
- **Meetings**: Schedule and manage meetings.
- **Assignments**: Create and track assignments.
- **Excuses**: Manage student excuses for absences.
- **Feedback**: Collect and manage feedback.
- **Submissions**: Handle assignment submissions.

## Project Structure

The project is organized into several directories and modules:

- **`api/`**: Contains CRUD operations, divided into core, feature, and sub-feature categories.
- **`db/`**: Includes database models for various entities.
- **`resources/`**: Houses static files such as HTML templates.
- **`routes/`**: Defines the API routes for different functionalities.
- **`validators/`**: Contains data validation logic.

## Running the Application

To run the application in development mode, use Uvicorn:

```bash
uvicorn main:app --reload
