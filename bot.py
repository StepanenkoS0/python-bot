import json
from datetime import datetime, timedelta

FILE_NAME = "events.json"

# ---------- Красивий вивід події ----------
def print_event(event):
    print(f"{event['name']} | {event['date']} {event['time']} | {event['category']}")


# ---------- Сортування подій ----------
def sort_events(events):
    """Сортує події: спочатку найближчі, потім минулі"""

    now = datetime.now()

    def event_datetime(event):
        return datetime.strptime(event["date"] + " " + event["time"], "%Y-%m-%d %H:%M")

    future_events = []
    past_events = []

    for event in events:
        if event_datetime(event) >= now:
            future_events.append(event)
        else:
            past_events.append(event)

    future_events.sort(key=event_datetime)
    past_events.sort(key=event_datetime)

    return future_events + past_events


# ---------- Робота з файлом ----------
def load_events():
    """Завантажує події з файлу"""
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_events(events):
    """Зберігає події у файл"""
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)


# ---------- Вітання ----------
def greet():
    print("Привіт! Я бот-організатор подій.")
    print("Напиши 'допомога', щоб побачити список команд.")


# ---------- Допомога ----------
def help_command():
    print("""
Доступні команди:
додати - додати нову подію
показати - показати всі події
сьогодні - події на сьогодні
завтра - події на завтра
тиждень - події на тиждень
фільтр - події на конкретну дату
видалити - видалити подію
редагувати - змінити подію
вийти - завершити програму
""")

    # ---------- Додати подію ----------
def add_event(events):

    while True:
        name = input("Назва події: ").strip()

        if name == "":
            print("Назва не може бути порожньою!")
        else:
            break

    while True:
        date = input("Дата (YYYY-MM-DD): ").strip()

        if date == "":
            print("Дата обов'язкова!")
            continue

        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except:
            print("Неправильний формат дати!")

    while True:
        time = input("Час (HH:MM) або Enter: ").strip()

        if time == "":
            time = "00:00"
            break

        try:
            datetime.strptime(time, "%H:%M")
            break
        except:
            print("Неправильний формат часу!")

    category = input("Категорія або опис (можна Enter): ").strip()

    # --- Перевірка конфлікту ---
    for event in events:
        if event["date"] == date and event["time"] == time:
            print("⚠ Увага! У цей час вже є інша подія:")
            print_event(event)

    new_event = {
        "name": name,
        "date": date,
        "time": time,
        "category": category
    }

    events.append(new_event)
    save_events(events)

    print("Подію додано!")


# ---------- Показати всі події ----------
def show_events(events):

    if not events:
        print("Подій немає.")
        return

    print("\n=== Список подій ===")

    sorted_events = sort_events(events)

    for i, event in enumerate(sorted_events):
        print(f"{i+1}. {event['name']} | {event['date']} {event['time']} | {event['category']}")


# ---------- Події на сьогодні ----------
def today_events(events):

    today = datetime.now().strftime("%Y-%m-%d")
    found = False

    for event in events:
        if event["date"] == today:
            print_event(event)
            found = True

    if not found:
        print("Подій на сьогодні немає.")


# ---------- Події на завтра ----------
def tomorrow_events(events):

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    found = False

    for event in events:
        if event["date"] == tomorrow:
            print_event(event)
            found = True

    if not found:
        print("Подій на завтра немає.")


# ---------- Події на тиждень ----------
def week_events(events):

    today = datetime.now()
    week = today + timedelta(days=7)

    found = False

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")

        if today <= event_date <= week:
            print_event(event)
            found = True

    if not found:
        print("Подій на цей тиждень немає.")


# ---------- Фільтр за датою ----------
def filter_by_date(events):

    date = input("Введіть дату (YYYY-MM-DD): ")
    found = False

    for event in events:
        if event["date"] == date:
            print_event(event)
            found = True

    if not found:
        print("Подій на цю дату немає.")


# ---------- Видалення ----------
def delete_event(events):

    if not events:
        print("Немає подій для видалення.")
        return

    show_events(events)

    num = int(input("Номер події для видалення: "))

    if 0 < num <= len(events):
        events.pop(num - 1)
        save_events(events)
        print("Подію видалено")
    else:
        print("Невірний номер.")


# ---------- Редагування ----------
def edit_event(events):

    if not events:
        print("Подій для редагування немає.")
        return

    show_events(events)

    num = int(input("Номер події для редагування: "))

    if 0 < num <= len(events):

        event = events[num - 1]

        name = input(f"Нова назва ({event['name']}): ")
        date = input(f"Нова дата ({event['date']}): ")
        time = input(f"Новий час ({event['time']}): ")
        category = input(f"Нова категорія ({event['category']}): ")

        if name:
            event["name"] = name

        if date:
            event["date"] = date

        if time:
            event["time"] = time

        if category:
            event["category"] = category

        save_events(events)

        print("Подію оновлено!")

    else:
        print("Невірний номер.")


# ---------- Основна програма ----------
def main():

    events = load_events()

    greet()

    while True:

        command = input("\nВведіть команду: ").lower()

        if command == "допомога":
            help_command()

        elif command == "додати":
            add_event(events)

        elif command == "показати":
            show_events(events)

        elif command == "сьогодні":
            today_events(events)

        elif command == "завтра":
            tomorrow_events(events)

        elif command == "тиждень":
            week_events(events)

        elif command == "фільтр":
            filter_by_date(events)

        elif command == "видалити":
            delete_event(events)

        elif command == "редагувати":
            edit_event(events)

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда. Напишіть 'допомога'.")


if __name__ == "__main__":
    main()