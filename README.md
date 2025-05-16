# AirlineReservationManagementSystem
Nabeel

# SkyLink Airways Reservation System

A comprehensive airline management system with:
- Flight scheduling
- Passenger booking
- Crew management
- Operational analytics

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Run main.py: `python main.py`

# ✈️ Airline Reservation Management System

A Python-based GUI application for managing airline operations such as flights, bookings, passengers, and crew, with integrated analytics support. Built with `Tkinter`, `SQLite`, `SQLAlchemy`, and optional `MongoDB`.

---

## 🚀 Features

- 🔐 **Admin/Staff Login** with session tracking
- ✈️ **Flight Management** (Add, View, Update, Cancel)
- 👤 **Passenger Booking** and **My Bookings**
- 🧑‍✈️ **Crew Assignment** to flights
- 📊 **Analytics Dashboard** (Flight occupancy, route popularity)
- ✅ **Data Persistence** with SQLite & SQLAlchemy ORM
- 🌐 Optional MongoDB for real-time analytics
- 📁 Clean, modular architecture (dialogs, windows, services, DAO)

---

## 📦 Technologies Used

- Python 3.11+
- Tkinter (GUI)
- SQLite (local DB)
- SQLAlchemy ORM
- Plotly (analytics visualization)
- MongoDB (optional, for analytics)
- dotenv (for environment configs)

---

## 📁 Folder Structure

<pre>
AirlineReservationManagementSystem/
├── assets/
│   ├── icons/
│   ├── images/
│   └── __init__.py
├── business_logic/
│   ├── auth_services.py
│   ├── booking_services.py
│   ├── crew_services.py
│   ├── flight_services.py
│   └── reporting_services.py
├── config/
│   └── settings.py
├── data_access/
│   ├── analytics_dao.py
│   ├── booking_dao.py
│   ├── crew_dao.py
│   ├── flight_dao.py
│   └── passenger_dao.py
├── database/
│   ├── initialization.py
│   ├── models.py
│   ├── sample_analytics.py
│   └── skylink_db.sqlite
├── presentation/
│   ├── dialogs/
│   │   ├── booking_dialog.py
│   │   ├── crew_dialog.py
│   │   ├── flight_dialog.py
│   │   └── passenger_dialog.py
│   ├── widgets/
│   │   └── date_picker.py
│   ├── windows/
│   │   ├── auth_window.py
│   │   ├── booking_window.py
│   │   ├── crew_window.py
│   │   ├── dashboard.py
│   │   ├── flight_window.py
│   │   └── reports_window.py
│   ├── app.py
│   ├── plotly_chart.py
│   └── styles.py
├── scripts/
│   └── __init__.py
├── tests/
│   ├── test_booking_dao.py
│   ├── test_booking_service.py
│   ├── test_models.py
│   └── test_services.py
├── .env
├── main.py
├── requirements.txt
└── README.md
</pre>

---

## 🛠️ Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/AirlineReservationManagementSystem.git
   cd AirlineReservationManagementSystem


##Install dependencies:

pip install -r requirements.txt

🗃️ Initialize the Database

python database/initialization.py

This will:

Create all necessary tables

Insert 3 sample flights, 3 crew members

Add default admin and staff accounts

Link airports with city codes

▶️ Run the Application
After setup, simply run:

python main.py

The GUI launcher will open. Log in with one of the test accounts or register new ones.

🧪 Sample Credentials
You can use the following credentials after running initialization.py:

Role	username	Password
Admin	admin	admin123
Crew	crew	staff123
User nabeel  2416877

You may also register your own staff accounts.

🧪 Run Unit Tests
Run tests for your business logic and data access layers:

pytest tests/
Ensure pytest is installed (pip install pytest).

🧩 MongoDB Analytics (Optional)
MongoDB is used to:

Store booking logs

Generate analytics like route trends, flight occupancy

To enable:

Make sure MongoDB is running locally or use MongoDB Atlas

Update .env with the correct URI

python database/sample_analytics.py
If MongoDB is not available, analytics features will fall back gracefully or be skipped.

⚙️ Customization
To disable analytics completely, set USE_MONGO=False in config/settings.py

To change default flight routes or airports, edit initialization.py → seed_flights() and seed_airports()

To change the style/theme of the app, tweak presentation/styles.py

📌 Known Limitations
Analytics “Open in Browser” may require system default browser support

MongoDB features are optional, not critical


👤 Author
Made with ❤️ by Nabeel
Project submitted as part of MSc Software Engineering coursework (CPS7003B - Database Systems)
