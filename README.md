Project Management Dashboard
A task and project management dashboard inspired by Jira, built with Django to help teams efficiently track projects and tasks.
Features
1. Multiple User Roles: Tester, Web Developer, Project Analyst, and more.
2. Project Management: Admin users can create new projects.
3. Task Management: Regular users can create tasks within projects. Editing and deleting tasks are restricted to maintain integrity.
4. Visibility: All users can view project and task details, including real-time updates.
5. Interactive Charts: Visualize task progress across different roles.
6. Real-Time Notifications: Powered by WebSockets for instant updates.
Technology Stack
1. Backend: Django
2. Frontend: HTML, CSS, JavaScript, Bootstrap
3. Real-Time Updates: WebSockets
What I Learned
1. Gained hands-on experience with complex Django workflows and user role management.
2. Tackled challenging bugs in JavaScript and integration that sometimes required major refactoring.
3. Improved debugging and problem-solving skills throughout the project development.
4. Utilized frontend resources like Deepseek to enhance UI design.
How to Run the Project Locally
1. Clone the repository:
   git clone https://github.com/your-username/your-repo.git
2. Create and activate a virtual environment:
   python -m venv env
   source env/bin/activate (On Windows: env\Scripts\activate)
3. Install dependencies:
   pip install -r requirements.txt
4. Apply migrations:
   python manage.py migrate
5. Start the development server:
   python manage.py runserver
6. Access the application:
   Open your browser and go to http://localhost:8000
Future Improvements
1. Implement task editing and deletion permissions based on user roles.
2. Enhance UI responsiveness and overall design.
3. Expand the notification system with advanced features.
4. Refine user authentication and permission controls.
