**Project Management Dashboard**
A task and project management dashboard inspired by Jira, built with Django to help teams track projects and tasks efficiently.

**Features**

Multiple user roles: Tester, Web Developer, Project Analyst, and more

Admin users can create new projects

Regular users can create tasks under projects but cannot edit or delete them

Everyone can view project and task details, along with updates

Interactive charts to visualize task progress by role

Real-time notifications powered by WebSockets

**Technology Stack**

Backend: Django

Frontend: HTML, CSS, JavaScript, Bootstrap

Real-time communication: WebSockets

**What I Learned**

This project helped me understand complex Django workflows and user role management. I faced many challenges fixing bugs, especially in JavaScript and frontend-backend integration. Some issues required significant refactoring, which improved my debugging and problem-solving skills.

**How to Run**

Clone the repo

Create a virtual environment and install dependencies (pip install -r requirements.txt)

Run migrations: python manage.py migrate

Start the development server: python manage.py runserver

Access the app at http://localhost:8000

**Future Improvements**

Add task editing and deletion permissions based on roles

Enhance the UI for better responsiveness

Integrate advanced notification system

Add user authentication and permissions refinements


