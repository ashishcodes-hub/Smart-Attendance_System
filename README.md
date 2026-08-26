 Smart AI Attendance System Using Face Recognition
 About the Project

Smart AI Attendance System is a web-based application developed to automate the traditional attendance process using Face Recognition technology.

In a traditional classroom, teachers have to manually mark the attendance of students. This process takes time and can also allow proxy attendance. This project helps solve these problems by automatically identifying students from classroom images and generating attendance records.

The system has separate portals for Teachers and Students. Teachers can create subjects, manage students, generate QR codes, upload classroom photos, and generate attendance. Students can register, join subjects using QR codes, and check their attendance history.

 Main Features

### Teacher Module

The Teacher Portal allows teachers to:

* Register and log into the system
* Create and manage subjects
* Generate a QR code for each subject
* Share the QR code with students for enrollment
* Upload classroom photographs
* Run the face recognition system
* Automatically generate attendance
* View attendance records

### Student Module

The Student Portal allows students to:

* Register and log into the system
* Join subjects using a QR code
* View enrolled subjects
* Check their attendance history

---

## Face Recognition Attendance

Face Recognition is the main part of this project.

When a teacher uploads a classroom photograph, the system detects the faces present in the image. It then generates face encodings and compares them with the face data of registered students.

If a face matches a registered student, that student is identified and marked as present. The attendance information is then stored in the database.

This process helps reduce manual work and makes attendance generation faster.

---

## System Workflow

The basic workflow of the project is:

Teacher Login

↓

Create Subject

↓

Generate QR Code

↓

Student Scans QR Code

↓

Student Joins the Subject

↓

Teacher Uploads Classroom Photos

↓

Face Detection and Recognition

↓

Attendance is Generated

↓

Attendance is Stored in the Supabase Database

↓

Teacher and Student Can View Attendance Records

---

## Technologies Used

The following technologies and libraries were used in this project:

* Python
* Streamlit
* Supabase
* PostgreSQL
* Face Recognition
* Dlib
* OpenCV
* NumPy
* Pandas
* Pillow
* bcrypt for password hashing
* Segno for QR code generation
* Git and GitHub for version control
* Streamlit Community Cloud for deployment

---

## Project Structure

The project follows a modular structure. The main application file handles navigation between the different parts of the system.

The project includes separate modules for:

* Home Screen
* Teacher Portal
* Student Portal
* Database Operations
* Face Recognition Pipeline
* User Interface Components
* QR Code Enrollment
* Authentication and Session Management

This modular structure makes the project easier to maintain and update.

---

## Database

The project uses Supabase with PostgreSQL as the cloud database.

The database stores information related to:

* Teachers
* Students
* Subjects
* Student Subject Enrollment
* Attendance Records

The attendance records are stored after the face recognition process is completed.

---

## Security

User passwords are not stored directly as plain text. The project uses bcrypt to securely hash passwords.

Sensitive information such as the Supabase URL and API key is managed using Streamlit Secrets during deployment.

The required environment variables are:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-key"
```

The actual Supabase credentials should not be uploaded to a public GitHub repository.

---

## How to Run the Project Locally

First, clone the repository:

```bash
git clone https://github.com/ashishcodes-hub/Machine-Learning2.git
```

Move to the project directory:

```bash
cd Machine-Learning2
```

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

After configuring the Supabase credentials, run the application:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Deployment

The project is deployed using Streamlit Community Cloud.

GitHub is used to store and manage the project source code. Supabase is used as the cloud database, while Streamlit Community Cloud is used to deploy the application online.

---

## Future Improvements

The project can be improved further by adding the following features:

* Real-time camera-based attendance
* Mobile application
* Anti-spoofing and liveness detection
* Face mask detection
* Attendance analytics and reports
* Email notifications
* SMS alerts
* Admin dashboard
* Multi-class and multi-subject support
* Attendance percentage analysis

---

## Developer

Ashish Kumar
B.Tech - Computer Science and Design

---

This project was developed to explore the practical use of Artificial Intelligence, Face Recognition, web development, cloud databases, and automated attendance management.

**Note:** README me ek cheez check kar lena: agar tumhari current repository ka naam `Machine-Learning2` nahi hai, to `git clone` wala link apni actual GitHub repository ke according change kar dena.
