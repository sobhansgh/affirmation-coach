import flet as ft
from database.database import Base, engine
from ui.dashboard import DashboardView

# اطمینان از ساخته شدن دیتابیس در اولین اجرا
Base.metadata.create_all(bind=engine)


def main(page: ft.Page):
    # تنظیمات پایه صفحه برای زبان فارسی
    page.title = "Affirmation Coach"
    page.window_width = 800
    page.window_height = 600
    page.rtl = True  # فعال‌سازی استاندارد راست‌چین
    page.theme_mode = ft.ThemeMode.DARK

    # تنظیمات فونت (اگر فونت وزیر یا شبنم در سیستم دارید می‌توانید اینجا اضافه کنید)
    page.theme = ft.Theme(font_family="Segoe UI")

    def on_route_change(e):
        page.views.clear()

        # نمایش ویو داشبورد
        dashboard_view = DashboardView(page)
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("مربی تأکیدی من"), bgcolor=ft.colors.SURFACE_VARIANT),
                    dashboard_view.build()
                ],
            )
        )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = on_route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)