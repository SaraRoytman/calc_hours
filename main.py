import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        page.add(ft.Text("עובד!"))

    page.add(ft.ElevatedButton(text="לחץ עלי", on_click=button_clicked))

ft.app(target=main)