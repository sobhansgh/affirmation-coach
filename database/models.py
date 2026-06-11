from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey
from database.database import Base


class UserProgress(Base):
    """ذخیره اطلاعات کلی، لول، امتیاز و استریک کاربر"""
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    current_xp = Column(Integer, default=0)
    current_level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    best_streak = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Affirmation(Base):
    """مدیریت عبارات تأکیدی تعریف شده یا پیشنهادی"""
    __tablename__ = "affirmations"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    category = Column(String, nullable=False)  # اعتماد به نفس، مالی، سلامتی، روابط، کسب و کار، شخصی
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyLog(Base):
    """ثبت وضعیت پاسخ کاربر به پاپ‌آپ‌ها برای تایم‌لاین و هیت‌مپ"""
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.utcnow().date, unique=True)
    total_reminders = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    missed_count = Column(Integer, default=0)

    # ارزیابی‌های روزانه
    morning_focus = Column(String, nullable=True)  # تمرکز صبحگاهی
    evening_rating = Column(Integer, nullable=True)  # امتیاز شبانه (1 تا 5)


class ActivityLog(Base):
    """جزئیات هر تعامل کاربر با پاپ‌آپ‌ها در طول روز"""
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    affirmation_id = Column(Integer, ForeignKey("affirmations.id"), nullable=True)
    status = Column(String, nullable=False)  # SUCCESS, FAILED, MISSED
    xp_gained = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Achievement(Base):
    """سیستم مدال‌ها و دستاوردهای کاربر"""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    is_unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime, nullable=True)


class Setting(Base):
    """تنظیمات اختصاصی نرم‌افزار"""
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    theme = Column(String, default="dark")  # light, dark
    sound_name = Column(String, default="bell.wav")
    language = Column(String, default="fa")
    popup_timeout = Column(Integer, default=30)  # ثانیه
    startup_enabled = Column(Boolean, default=False)