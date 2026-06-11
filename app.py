import flet as ft
import random
from database.database import Base, engine, SessionLocal
from ui.dashboard import DashboardView
from ui.affirmations import AffirmationsView
from ui.timeline import TimelineView
from ui.popup import show_affirmation_popup
from services.affirmation_service import get_active_affirmations
from services.reminder_service import start_scheduler, set_ui_callback, schedule_interval_reminder

# اطمینان از ساخته شدن دیتابیس
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    page.title = "مربی تأکیدی من (Affirmation Coach)"
    page.window_width = 1000
    page.window_height = 700
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # تنظیمات فونت
    page.fonts = {
        "IRANYekan": "fonts/iranyekan/iranyekan.ttf"
    }
    page.theme = ft.Theme(font_family="IRANYekan")


    # --- منطق زمان‌بندی و پاپ‌آپ ---
    def handle_scheduler_trigger():
        """این تابع زمانی که وقت یادآوری برسد اجرا می‌شود"""
        db = SessionLocal()
        try:
            active_affs = get_active_affirmations(db)
            if active_affs:
                # انتخاب یک عبارت تصادفی از بین عبارات فعال
                chosen_aff = random.choice(active_affs)
                # اجرای نمایش پاپ‌آپ در Thread امن رابط کاربری
                page.run_task(show_affirmation_popup, page, chosen_aff.text)
            else:
                print("هیچ عبارت فعالی برای نمایش وجود ندارد.")
        finally:
            db.close()


    # اتصال Scheduler به Flet و شروع زمان‌بندی (تست: هر 1 دقیقه)
    set_ui_callback(handle_scheduler_trigger)
    start_scheduler()
    schedule_interval_reminder(minutes=1) # برای تست روی 1 دقیقه تنظیم شده است
    # -------------------------------

    # آماده‌سازی صفحات
    dashboard_view = DashboardView(page)
    affirmations_view = AffirmationsView(page)
    timeline_view = TimelineView(page)

    main_content = ft.Container(expand=True, padding=20)

    def on_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            main_content.content = dashboard_view.build()
        elif selected_index == 1:
            main_content.content = affirmations_view.build()
        elif selected_index == 2:
            main_content.content = timeline_view.build()
        page.update()

    # منوی کناری (Sidebar)
    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.DASHBOARD_OUTLINED,
                selected_icon=ft.icons.DASHBOARD,
                label="داشبورد",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.FORMAT_QUOTE_OUTLINED,
                selected_icon=ft.icons.FORMAT_QUOTE,
                label="عبارات من",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.INSIGHTS_OUTLINED,
                selected_icon=ft.icons.INSIGHTS,
                label="پیشرفت",
            ),
        ],
        on_change=on_nav_change,
    )

    # چیدمان اولیه برنامه
    main_content.content = dashboard_view.build()

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                main_content
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")