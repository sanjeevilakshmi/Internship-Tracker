🧭 Online Internship Tracker with Daily Logs & Mentor Feedback
A Django-based web application that allows students to log their daily internship tasks, and mentors to provide weekly feedback.
This project simplifies internship monitoring, improves mentor–student communication, and ensures transparent progress tracking.

🚀 Features
👩‍🎓 For Students
Register and log in securely
Add, edit, and delete daily internship logs
View mentor feedback for each log
Track internship progress over time
🧑‍🏫 For Mentors
View students’ daily logs
Provide feedback for each submitted log
Edit or delete previously given feedback
Monitor student performance easily
🛠️ Tech Stack
Category	Technology
Frontend	HTML, CSS (Bootstrap 5), JavaScript
Backend	Django (Python)
Database	MySQL
Version Control	Git & GitHub
IDE Used	VS Code / PyCharm
⚙️ Installation Guide
Follow these steps to run the project locally 👇

1️⃣ Clone the Repository
git clone https://github.com/<your-username>/online-internship-tracker.git
cd online-internship-tracker
2️⃣ Create a Virtual Environment
python -m venv venv
venv\Scripts\activate       # On Windows
source venv/bin/activate    # On Mac/Linux
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Setup Database
Update settings.py with your MySQL credentials:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'internship_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Run migrations:
python manage.py makemigrations
python manage.py migrate
5️⃣ Create a Superuser (Admin)
python manage.py createsuperuser
6️⃣ Run the Server
python manage.py runserver
Then open your browser at 👉 http://127.0.0.1:8000/

🧩 Project Structure
internship_tracker/
│
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── user_logs.html
│   │   ├── add_feedback.html
│   │   └── view_log.html
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── internship_tracker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── manage.py

---

## 📚 Learning Outcomes
- Gained hands-on experience with **Django Models, Views, Templates (MVT)**  
- Implemented **CRUD operations** for logs and feedback  
- Integrated **authentication system** using Django’s built-in User model  
- Improved UI with **Bootstrap 5**  
- Understood relational data handling with **Foreign Keys** (User ↔ Logs ↔ Feedback)

---

## 💡 Future Enhancements
- Add progress analytics using **charts**  
- Role-based dashboards (Student / Mentor / Admin)  
- Email notifications for new feedback  
- Export reports as PDF or Excel  

---

## 👩‍💻 Author
**Sanjeevi Lakshmi Lavanya**  
🎓 B.Tech (4th Year) | Web Development & Cloud Enthusiast  
💼 Skills: Django, HTML, Bootstrap, MySQL, AWS  
📧 Email: 228r1a1252@gmail.com  
🌐 GitHub: [https://github.com/sanjeevilakshmi](https://github.com/sanjeevilakshmi)
