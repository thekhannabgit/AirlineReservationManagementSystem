from presentation.app import AirlineApp
from database.initialization import initialize_database
from sqlalchemy.orm import sessionmaker


def main():
    engine = initialize_database()
    Session = sessionmaker(bind=engine)
    session = Session()

    app = AirlineApp(session)
    app.mainloop()
    session.close()


if __name__ == "__main__":
    main()