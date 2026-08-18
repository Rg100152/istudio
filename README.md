🏠 iSTUDIO — Interior Design & Architecture Website

A modern, responsive and database-driven Interior Design & Architecture website built with Python Flask, SQLite, HTML, CSS and JavaScript.

iSTUDIO is designed as a complete single-file Flask application that combines a professional frontend with a lightweight backend, SQLite database, dynamic project/team/testimonial data and an AJAX-powered newsletter subscription system.

---

✨ Features

🎨 Modern UI

- Clean and professional interior-design themed interface
- Responsive layout for desktop, tablet and mobile
- Modern typography and visual hierarchy
- Smooth hover animations and transitions
- Sticky navigation header
- Responsive image galleries
- Professional teal/white color scheme

🏡 Homepage

- Hero section with interior-design imagery
- Company introduction
- Call-to-action buttons
- Service highlights
- Company statistics
- Responsive image grid

📖 About / History

- Company history section
- Studio philosophy
- Experience statistics
- Architecture and interior-design showcase

⭐ Why Choose Us

Six feature cards covering:

- 25+ Years Experience
- Best Interior Design
- Innovative Architects
- Customer Satisfaction
- Budget Friendly
- Sustainable Materials

🖼️ Projects Portfolio

Projects are loaded dynamically from SQLite.

Includes:

- Living Room
- Kitchen
- Commercial
- Bedroom
- Home Office
- Outdoor

The portfolio includes client-side category filtering.

🛠️ Services

Available services include:

- Interior Design
- Renovation
- Commercial Design
- Implementation

👨‍🎨 Professional Designers

Team members are stored in the database and dynamically rendered.

Each designer includes:

- Profile image
- Name
- Professional title
- Biography
- Social media links

💬 Customer Testimonials

Dynamic testimonials with:

- Client profile image
- Rating
- Review
- Client name
- Client occupation

Includes:

- Previous button
- Next button
- Automatic slideshow
- Smooth fade animation

📧 Newsletter Subscription

The website includes an AJAX-based newsletter system.

Users can submit their email without reloading the page.

Backend endpoint:

POST /api/subscribe

The email address is stored inside SQLite.

Duplicate email addresses are handled automatically using a "UNIQUE" database constraint.

---

🧰 Technology Stack

Technology| Purpose
Python 3| Backend programming
Flask| Web framework
SQLite| Database
HTML5| Page structure
CSS3| Styling and responsive design
JavaScript| Interactive functionality
Jinja2| Dynamic HTML templating
Fetch API| AJAX newsletter requests
SVG| Interface icons
Unsplash| Demo imagery

---

📁 Project Structure

The project is intentionally designed as a single-file Flask application.

iSTUDIO/
│
├── app.py
│
├── istudio.db
│
└── README.md

"app.py"

Contains:

- Flask application
- SQLite database functions
- Database schema
- Database seed data
- Jinja2 template
- HTML
- CSS
- JavaScript
- API endpoint
- Application startup logic

"istudio.db"

SQLite database containing:

projects
team
testimonials
subscribers

---

🗄️ Database Schema

Projects

projects (
    id INTEGER PRIMARY KEY,
    title TEXT,
    category TEXT,
    description TEXT,
    image_url TEXT
)

Stores portfolio projects.

---

Team

team (
    id INTEGER PRIMARY KEY,
    name TEXT,
    title TEXT,
    bio TEXT,
    image_url TEXT,
    facebook TEXT,
    twitter TEXT,
    linkedin TEXT
)

Stores professional designer information.

---

Testimonials

testimonials (
    id INTEGER PRIMARY KEY,
    client_name TEXT,
    client_title TEXT,
    quote TEXT,
    rating INTEGER,
    image_url TEXT
)

Stores customer reviews.

---

Subscribers

subscribers (
    id INTEGER PRIMARY KEY,
    email TEXT UNIQUE,
    subscribed_at TIMESTAMP
)

Stores newsletter subscribers.

---

🚀 Installation

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/istudio.git
cd istudio

2. Install Flask

pip install flask

Or:

python3 -m pip install flask

---

▶️ Run the Application

Start the Flask server:

python3 app.py

You should see:

iSTUDIO - Architecture & Interior Design
Production Server
Starting Flask development server...
Access the website at:
http://127.0.0.1:5000

Open your browser and visit:

http://127.0.0.1:5000

---

📱 Running on Android

The application can also be used in a Python-capable Android environment.

For example, after installing Python and Flask:

python3 app.py

Then open:

http://127.0.0.1:5000

If the server is accessible over the local network, another device can potentially connect using the host device's local IP address and port "5000".

---

🔌 API

Newsletter Subscription

Endpoint

POST /api/subscribe

Request

The endpoint expects:

email=user@example.com

Successful Response

{
    "success": true,
    "message": "Subscription successful."
}

Invalid Email

{
    "success": false,
    "message": "Invalid email address."
}

Duplicate Email

{
    "success": false,
    "message": "This email is already subscribed."
}

---

🧠 Application Architecture

              ┌──────────────────────┐
              │      Web Browser     │
              └──────────┬───────────┘
                         │
                         │ HTTP
                         ▼
              ┌──────────────────────┐
              │      Flask App      │
              │       app.py        │
              └──────────┬───────────┘
                         │
              ┌──────────┴───────────┐
              │                      │
              ▼                      ▼
       ┌─────────────┐       ┌──────────────┐
       │   Jinja2    │       │  API Routes  │
       │   Template  │       │ /api/subscribe│
       └──────┬──────┘       └──────┬───────┘
              │                     │
              └──────────┬──────────┘
                         ▼
                 ┌──────────────┐
                 │    SQLite    │
                 │  istudio.db  │
                 └──────────────┘

---

🖥️ Frontend Architecture

The frontend is contained inside the Flask template.

HTML
 │
 ├── Header
 ├── Hero
 ├── About
 ├── Features
 ├── Projects
 ├── Services
 ├── Designers
 ├── Testimonials
 ├── Newsletter
 └── Footer
      │
      ▼
    CSS
      │
      ├── Responsive Design
      ├── Animations
      ├── Grid Layout
      └── Components
      │
      ▼
 JavaScript
      │
      ├── Project Filtering
      ├── Testimonial Slider
      └── Newsletter AJAX

---

🖼️ Images

Demo project images are loaded from Unsplash using remote image URLs.

For production usage, replacing external demo images with locally hosted or properly licensed assets is recommended.

Example:

<img src="static/images/living-room.jpg" alt="Modern Living Room">

---

🔐 Security Considerations

This project is primarily intended as a portfolio/educational application.

Before using it in a real production environment, consider implementing:

- Environment variables for secrets
- Strong "SECRET_KEY"
- CSRF protection
- Server-side email validation
- Rate limiting
- Authentication for administrative functionality
- Secure HTTP headers
- Production WSGI server
- Database migrations
- Proper logging
- Input sanitization
- HTTPS
- Error handling without exposing internal information

Do not use Flask's development server as the production server.

---

⚠️ Important Development Note

The current application uses:

app.run(
    host='0.0.0.0',
    port=5000,
    debug=True
)

For production deployment, "debug=True" should be disabled.

Example:

app.run(
    host='0.0.0.0',
    port=5000,
    debug=False
)

A production WSGI server such as Gunicorn should be preferred.

---

🧪 Demo Data

The application automatically creates and seeds the SQLite database when "istudio.db" does not exist.

Initial demo content includes:

- 6 projects
- 4 designers
- 3 testimonials
- Newsletter subscriber table

---

🔄 Database Initialization

On first execution:

app.py
   │
   ├── Check istudio.db
   │
   ├── Database doesn't exist
   │
   ├── Create tables
   │
   └── Insert demo data

On subsequent executions:

app.py
   │
   └── Existing database
           │
           └── Use existing data

---

📸 Screenshots

Add screenshots of your running application here.

Example:

screenshots/
├── homepage.png
├── projects.png
├── services.png
├── designers.png
└── testimonials.png

Then add them to this README:

![iSTUDIO Homepage](screenshots/homepage.png)

---

🎯 Project Objectives

The main objectives of iSTUDIO are:

- Demonstrate Flask web development
- Demonstrate SQLite database integration
- Create a responsive professional website
- Implement dynamic content rendering
- Implement AJAX-based API communication
- Demonstrate CRUD-oriented database architecture
- Practice frontend/backend integration
- Build a portfolio-ready web application

---

🔮 Future Improvements

Possible future versions can include:

- [ ] Admin dashboard
- [ ] Designer management system
- [ ] Project CRUD operations
- [ ] Testimonial management
- [ ] Contact form
- [ ] Appointment booking
- [ ] User authentication
- [ ] Admin authentication
- [ ] Image upload system
- [ ] Project detail pages
- [ ] Search functionality
- [ ] Dark mode
- [ ] Email notification system
- [ ] PostgreSQL support
- [ ] REST API expansion
- [ ] Flask Blueprints
- [ ] Database migrations
- [ ] Production deployment
- [ ] Docker support

---

📊 Current Features Summary

Frontend
├── Responsive UI              ✓
├── Navigation                 ✓
├── Hero Section               ✓
├── About Section              ✓
├── Services                  ✓
├── Portfolio                 ✓
├── Portfolio Filtering       ✓
├── Team Section              ✓
├── Testimonials              ✓
├── Testimonial Carousel      ✓
├── Newsletter UI             ✓
└── Footer                    ✓

Backend
├── Flask                     ✓
├── SQLite                    ✓
├── Database Initialization   ✓
├── Database Seeding          ✓
├── Dynamic Templates         ✓
└── Newsletter API            ✓

Database
├── Projects                  ✓
├── Team                      ✓
├── Testimonials              ✓
└── Subscribers               ✓

---

👨‍💻 Author

Raj Gautam

BCA Student & Web Development Enthusiast

Interested in:

- Web Development
- Python
- Flask
- Databases
- Cybersecurity
- Open Source

---

📄 License

This project can be used for educational and portfolio purposes.

Before redistributing the project commercially, verify the licenses/terms of any third-party assets, including images, fonts and external resources.

---

⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

iSTUDIO — Designing Spaces. Creating Experiences.