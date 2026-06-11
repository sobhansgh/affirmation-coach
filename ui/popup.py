import flet as ft
from services.sound_service import play_sound
from database.database import SessionLocal
from services.streak_service import add_xp, update_streak


def show_affirmation_popup(page: ft.Page, affirmation_text: str):
    """نمایش پاپ‌آپ عبارت تأکیدی و ثبت امتیاز"""

    # پخش صدای آرامش‌بخش
    play_sound("zen.wav")

    def handle_done(e):
        db = SessionLocal()
        try:
            # اضافه کردن 10 امتیاز برای انجام موفق
            add_xp(db, 10)
            # آپدیت استریک
            update_streak(db, all_daily_reminders_completed=True)
        finally:
            db.close()

        dialog.open = False
        page.update()

    def handle_snooze(e):
        # فعلا فقط پنجره بسته می‌شود (منطق تعویق در زمان‌بندی بعدا اضافه می‌شود)
        dialog.open = False
        page.update()

    def handle_failed(e):
        db = SessionLocal()
        try:
            # در صورت عدم انجام، استریک صفر می‌شود
            update_streak(db, all_daily_reminders_completed=False)
        finally:
            db.close()

        dialog.open = False
        page.update()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("زمان تمرین ذهنی", text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            padding=20,
            content=ft.Text(
                affirmation_text,
                size=22,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            )
        ),
        actions=[
            ft.TextButton("انجام دادم ✓", on_click=handle_done, style=ft.ButtonStyle(color=ft.colors.GREEN)),
            ft.TextButton("بعداً", on_click=handle_snooze),
            ft.TextButton("انجام ندادم ✗", on_click=handle_failed, style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=15)
    )

    page.dialog = dialog
    dialog.open = True
    page.update()