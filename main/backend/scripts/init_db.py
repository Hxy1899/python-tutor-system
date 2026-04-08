import sys
import os
from sqlalchemy.orm import Session

# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.db.session import engine, SessionLocal, Base
from app.models import User, UserRole, Assignment
from app.utils.security import get_password_hash

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

    # Check if we have an admin user
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # Create a default admin (teacher)
            new_admin = User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                role=UserRole.TEACHER,
                name="System Administrator"
            )
            db.add(new_admin)
            db.commit()
            print("Admin user created.")
        
        # Add a sample assignment
        sample_assignment = db.query(Assignment).filter(Assignment.title == "Hello World in Python").first()
        if not sample_assignment:
            new_assignment = Assignment(
                title="Hello World in Python",
                description="Write a program that prints 'Hello, World!'",
                test_code="""
def test_hello_world(capsys):
    import solution
    # solution is the name of the file student submitted
    # we'll handle this in dynamic_tester.py
    pass
"""
            )
            db.add(new_assignment)
            db.commit()
            print("Sample assignment created.")
            
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
