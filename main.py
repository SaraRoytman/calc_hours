import flet as ft
import datetime
import json
import os

JSON_FILE = "shifts.json"

def init_json():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

def main(page: ft.Page):
    page.title = "מחשבון שעות"
    page.rtl = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    init_json()
    
    def get_monthly_total():
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                shifts = json.load(f)
        except Exception:
            shifts = []
            
        current_month = datetime.datetime.now().strftime("%Y-%m")
        total = 0.0
        
        for shift in shifts:
            if shift.get("date", "").startswith(current_month):
                total += shift.get("total_hours", 0.0)
                
        return total

    date_input = ft.TextField(label="Date (YYYY-MM-DD) or leave empty for today", width=300)
    
    saved_start = page.client_storage.get("start_time") or ""
    start_time_input = ft.TextField(label="Start Time", width=300, value=saved_start)
    end_time_input = ft.TextField(label="End of time", width=300)
    
    result_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
    monthly_total_text = ft.Text(value=f"Hours this month: {get_monthly_total():.2f}", size=22, color=ft.Colors.BLUE)

    def save_start(e):
        page.client_storage.set("start_time", start_time_input.value)
        result_text.value = "Saved!"
        result_text.color = ft.Colors.GREEN
        page.update()

    def calculate_and_save_shift(e):
        try:
            x = datetime.datetime.strptime(start_time_input.value, "%H%M")  # type: ignore
            y = datetime.datetime.strptime(end_time_input.value, "%H%M")  # type: ignore
            
            z = y - x
            total_hours = z.total_seconds() / 3600
            
            input_date = (date_input.value or "").strip()
            if input_date:
                datetime.datetime.strptime(input_date, "%Y-%m-%d")
                current_date = input_date
            else:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                shifts = json.load(f)
            
            new_shift = {
                "date": current_date,
                "start": start_time_input.value,
                "end": end_time_input.value,
                "total_hours": total_hours
            }
            shifts.append(new_shift)
            
            with open(JSON_FILE, "w", encoding="utf-8") as f:
                json.dump(shifts, f, indent=4, ensure_ascii=False)
            
            result_text.value = f"Saved on json: {total_hours:.2f} "
            result_text.color = ft.Colors.GREEN
            
            page.client_storage.remove("start_time")
            date_input.value = "" 
            start_time_input.value = ""
            end_time_input.value = ""
            monthly_total_text.value = f"time total: {get_monthly_total():.2f}"
            
        except ValueError:
            result_text.value = "Wrong time/date format"
            result_text.color = ft.Colors.RED
            
        page.update()

    def clear_data(e):
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        
        page.client_storage.remove("start_time")
        date_input.value = ""
        start_time_input.value = ""
        end_time_input.value = ""
        
        monthly_total_text.value = "Hours this month: 0.00"
        result_text.value = "All data cleared!"
        result_text.color = ft.Colors.RED
        
        page.update()

    save_button = ft.ElevatedButton(text="Save Start", on_click=save_start)
    calc_button = ft.ElevatedButton(text="Calc", on_click=calculate_and_save_shift)
    clear_button = ft.ElevatedButton(text="Clear Data", on_click=clear_data, color=ft.Colors.RED)

    page.add(
        monthly_total_text,
        ft.Divider(height=30),
        date_input, 
        ft.Divider(height=10, color="transparent"),
        start_time_input, 
        save_button,
        ft.Divider(height=20, color="transparent"),
        end_time_input, 
        calc_button, 
        ft.Divider(height=20, color="transparent"),
        clear_button,
        result_text
    )

ft.app(target=main)