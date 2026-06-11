from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# ایجاد یک نمونه سراسری از زمان‌بندی‌کننده
scheduler = BackgroundScheduler()

def start_scheduler():
    """شروع به کار سیستم زمان‌بندی"""
    if not scheduler.running:
        scheduler.start()

def stop_scheduler():
    """توقف سیستم زمان‌بندی"""
    if scheduler.running:
        scheduler.shutdown()

def trigger_popup(affirmation_id: int = None):
    """
    این تابع در زمان مقرر فراخوانی می‌شود.
    در فاز UI، این تابع پنجره پاپ‌آپ Flet را باز خواهد کرد.
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] زمان نمایش پاپ‌آپ فرا رسیده است!")
    # منطق اتصال به UI بعداً اینجا اضافه می‌شود

def schedule_interval_reminder(hours: int):
    """زمان‌بندی به صورت بازه‌ای (مثلاً هر 3 ساعت)"""
    # ابتدا کارهای قبلی را پاک می‌کنیم تا تداخل ایجاد نشود
    scheduler.remove_all_jobs()
    scheduler.add_job(
        trigger_popup,
        'interval',
        hours=hours,
        id='interval_reminder'
    )

def schedule_fixed_times(times: list):
    """
    زمان‌بندی در ساعات مشخص
    ورودی باید لیستی از رشته‌ها باشد، مثال: ["08:00", "13:00", "18:00"]
    """
    scheduler.remove_all_jobs()
    for i, time_str in enumerate(times):
        hour, minute = map(int, time_str.split(':'))
        scheduler.add_job(
            trigger_popup,
            'cron',
            hour=hour,
            minute=minute,
            id=f'fixed_reminder_{i}'
        )