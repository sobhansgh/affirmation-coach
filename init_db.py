from database.database import engine, Base
from database.models import UserProgress, Affirmation, DailyLog, ActivityLog, Achievement, Setting

def initialize():
    print("در حال ساخت جداول دیتابیس...")
    Base.metadata.create_all(bind=engine)
    print("دیتابیس با موفقیت ساخته شد و جداول آماده هستند.")

if __name__ == "__main__":
    initialize()