from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

# متغیری برای نگهداری تابع رابط کاربری
_ui_trigger_callback = None

def set_ui_callback(callback):
    """ثبت تابعی از Flet که باید در زمان مقرر فراخوانی شود"""
    global _ui_trigger_callback
    _ui_trigger_callback = callback

def start_scheduler():
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()

def trigger_popup():
    """این تابع توسط زمان‌بندی‌کننده فراخوانی می‌شود"""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] زمان نمایش پاپ‌آپ فرا رسیده است!")
    # فراخوانی تابع Flet برای نمایش دیالوگ
    if _ui_trigger_callback:
        _ui_trigger_callback()

def schedule_interval_reminder(minutes: int):
    scheduler.remove_all_jobs()
    scheduler.add_job(
        trigger_popup,
        'interval',
        minutes=minutes,
        id='interval_reminder'
    )