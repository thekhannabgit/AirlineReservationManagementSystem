
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    role TEXT CHECK(role IN ('Admin', 'Staff', 'User')) DEFAULT 'User',
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS aircrafts (
    id INTEGER PRIMARY KEY,
    model TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    manufacturer TEXT
);

CREATE TABLE IF NOT EXISTS airports (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS crew (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    role TEXT CHECK(role IN ('Pilot', 'Co-Pilot', 'Flight Attendant'))
);

CREATE TABLE IF NOT EXISTS crew_assignments (
    id INTEGER PRIMARY KEY,
    crew_id INTEGER,
    flight_id INTEGER,
    FOREIGN KEY(crew_id) REFERENCES crew(id),
    FOREIGN KEY(flight_id) REFERENCES flights(id)
);

CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY,
    flight_number TEXT UNIQUE NOT NULL,
    departure_airport_code TEXT,
    arrival_airport_code TEXT,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    aircraft_id INTEGER,
    status TEXT CHECK(status IN ('Scheduled', 'Delayed', 'Departed', 'Arrived', 'Cancelled')) DEFAULT 'Scheduled',
    base_price REAL NOT NULL,
    FOREIGN KEY(departure_airport_code) REFERENCES airports(code),
    FOREIGN KEY(arrival_airport_code) REFERENCES airports(code),
    FOREIGN KEY(aircraft_id) REFERENCES aircrafts(id)
);

CREATE TABLE IF NOT EXISTS passengers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    passport_number TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    flight_id INTEGER,
    passenger_id INTEGER,
    booking_date DATETIME,
    seat_class TEXT,
    status TEXT,
    final_price REAL,
    FOREIGN KEY(flight_id) REFERENCES flights(id),
    FOREIGN KEY(passenger_id) REFERENCES passengers(id)
);
