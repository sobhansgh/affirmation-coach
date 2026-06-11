import flet as ft
from database.database import SessionLocal
from database.models import Achievement
from services.achievement_service import initialize_achievements


class TimelineView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        self.achievements_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)
        self.load_achievements()

        return ft.Container(
            padding=20,
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("مسیر پیشرفت شما", size=28, weight=ft.FontWeight.BOLD),
                    ft.Text("گزارش دستاوردها و مدال‌های کسب شده", color=ft.colors.OUTLINE),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Text("دستاوردها", size=20, weight=ft.FontWeight.W_600),
                    self.achievements_list
                ],
                expand=True
            )
        )

    def load_achievements(self):
        self.achievements_list.controls.clear()
        db = SessionLocal()
        try:
            # اطمینان از اینکه دستاوردهای اولیه ساخته شده‌اند
            initialize_achievements(db)
            achievements = db.query(Achievement).all()

            for ach in achievements:
                # اگر دستاورد باز شده باشد رنگ آن طلایی و آیکون آن کاپ است، در غیر این صورت خاکستری و قفل
                icon_color = ft.colors.AMBER_400 if ach.is_unlocked else ft.colors.GREY_700
                icon_type = ft.icons.EMOJI_EVENTS if ach.is_unlocked else ft.icons.LOCK_OUTLINE

                self.achievements_list.controls.append(
                    ft.Card(
                        elevation=1,
                        content=ft.ListTile(
                            leading=ft.Icon(icon_type, color=icon_color, size=30),
                            title=ft.Text(ach.title, size=16, weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(ach.description, color=ft.colors.OUTLINE),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            # shape=ft.RoundedRectangleBorder(radius=10)
                        )
                    )
                )
        finally:
            db.close()