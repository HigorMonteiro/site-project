# Todo List App

## Description
A web application for managing tasks, built with Next.js, TypeScript, Tailwind CSS, and ShadCN on the front-end, and Django REST Framework on the back-end. The project is dockerized for easy deployment and development.

## Features
- **User Authentication**: Create an account and log in.
- **Task CRUD Operations**: Create, read, update, and delete tasks.
- **Task Status**: Mark tasks as completed or not completed.
- **Task Filtering and Pagination**: View tasks with filters and pagination.
- **Dockerized Environment**: Run the application using Docker and Docker Compose.

## Technologies Used
### Front-end
- **Vite** (with TypeScript)
- **Tailwind CSS**
- **ShadCN UI components**

### Back-end
- **Django REST Framework**
- **Pytest** for unit testing

## Getting Started

### Prerequisites
- Node.js and npm
- Pnpm
- Python and poetry
- Docker and Docker Compose

### Installation

1 **Clone the repository**:
```bash
git clone git@github.com:HigorMonteiro/site-project.git
cd site-project
```

2 **Run backend**
  ```bash
   docker compose up --build
  ```
  http://localhost:8000/

3 **Run frontend**
  ```bash
   cd fronend/
   pnpm install && pnpm run dev
  ```
  http://localhost:5173/

4 **Login frontend**
```bash
   email: pedro@gmail.com
   password: asdf1234
```
Some users were created using the command, `python manage.py populate_users`.