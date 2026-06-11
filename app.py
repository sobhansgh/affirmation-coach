import flet as ft
from database.database import Base, engine
from ui.dashboard import DashboardView
from ui.affirmations import AffirmationsView

# اطمینان از ساخته شدن دیتابیس
Base.metadata.create_all(bind=engine)

def main(page: ft.Page):
    page.title = "مربی تأکیدی من (Affirmation Coach)"
    page.window_width = 1000
    page.window_height = 700
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    # page.theme = ft.Theme(font_family="Segoe UI")
    page.padding = 0

    # --- تنظیمات فونت اختصاصی ---
    page.fonts = {
        "IRANYekan": "fonts/iranyekan/iranyekan.ttf"
    }
    # اعمال فونت روی کل تم برنامه
    page.theme = ft.Theme(font_family="IRANYekan")


    # def on_route_change(e):
    #     page.views.clear()
    #
    #     # نمایش ویو داشبورد
    #     dashboard_view = DashboardView(page)
    #     page.views.append(
    #         ft.View(
    #             "/",
    #             [
    #                 ft.AppBar(title=ft.Text("مربی تأکیدی من", weight=ft.FontWeight.BOLD), bgcolor=ft.colors.SURFACE_VARIANT),
    #                 dashboard_view.build()
    #             ],
    #         )
    #     )
    #     page.update()
    #
    # def view_pop(e):
    #     page.views.pop()
    #     top_view = page.views[-1]
    #     page.go(top_view.route)
    #
    # page.on_route_change = on_route_change
    # page.on_view_pop = view_pop
    # page.go(page.route)


    # مقداردهی صفحات
    dashboard_view = DashboardView(page)
    affirmations_view = AffirmationsView(page)

    # محفظه اصلی برای نمایش محتوای صفحات
    main_content = ft.Container(
        expand=True,
        padding=20,
        content=dashboard_view.build()
    )
    def on_nav_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            main_content.content = dashboard_view.build()
        elif selected_index == 1:
            main_content.content = affirmations_view.build()
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

    # چیدمان کلی صفحه
    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                main_content,
            ],
            expand=True,
        )
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")