import json
from datetime import datetime, timedelta

FILE_NAME = "events.json"


# ---------- Вивід події ----------
def print_event(event):
    if event.get("end_time"):
        print(f"{event['name']} | {event['date']} {event['time']} - {event['end_time']} | {event['category']}")
    else:
        print(f"{event['name']} | {event['date']} {event['time']} | {event['category']}")


# ---------- Отримати datetime ----------
def event_datetime(event):
    return datetime.strptime(event["date"] + " " + event["time"], "%Y-%m-%d %H:%M")


# ---------- Сортування ----------
def sort_events(events):
    now = datetime.now()

    future = [e for e in events if event_datetime(e) >= now]
    past = [e for e in events if event_datetime(e) < now]

    future.sort(key=event_datetime)
    past.sort(key=event_datetime)

    return future + past


# ---------- Робота з файлом ----------
def load_events():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_events(events):
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
фільтр - фільтрація подій
видалити - видалити подію
редагувати - змінити подію
вийти - завершити програму
""")


# ---------- Додати ----------
def add_event(events):

    name = input("Назва події: ").strip()

    while True:
        date = input("Дата (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            break
        except:
            print("Невірний формат дати!")

    while True:
        time = input("Час (HH:MM) або Enter: ").strip()
        if time == "":
            time = "00:00"
            break
        try:
            datetime.strptime(time, "%H:%M")
            break
        except:
            print("Невірний формат часу!")

    end_time = input("Час завершення або Enter: ").strip()
    category = input("Категорія або опис: ").strip()

    events.append({
        "name": name,
        "date": date,
        "time": time,
        "end_time": end_time,
        "category": category
    })

    save_events(events)
    print("Подію додано!")


# ---------- Показати ----------
def show_events(events):

    if not events:
        print("Подій немає.")
        return

    sorted_events = sort_events(events)

    print("\n=== Список подій ===")
    for i, event in enumerate(sorted_events, 1):
        print(f"{i}. ", end="")
        print_event(event)


# ---------- Сьогодні ----------
def today_events(events):
    today = datetime.now().strftime("%Y-%m-%d")

    found = False
    for e in events:
        if e["date"] == today:
            print_event(e)
            found = True

    if not found:
        print("Подій на сьогодні немає.")


# ---------- Завтра ----------
def tomorrow_events(events):
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    found = False
    for e in events:
        if e["date"] == tomorrow:
            print_event(e)
            found = True

    if not found:
        print("Подій на завтра немає.")


# ---------- Поточний тиждень ----------
def week_events(events):

    today = datetime.now()
    week_end = today + timedelta(days=7)

    found = False

    for e in events:
        d = event_datetime(e)
        if today <= d <= week_end:
            print_event(e)
            found = True

    if not found:
        print("Подій на цей тиждень немає.")


# =====================================================
#                ФІЛЬТРИ (ЗГІДНО ТЗ)
# =====================================================

def filter_menu(events):

    print("""
Оберіть тип фільтра:
1 - події на конкретну дату
2 - події за період
3 - події за категорією
""")

    choice = input("Ваш вибір: ")

    if choice == "1":
        filter_by_date(events)
    elif choice == "2":
        filter_by_period(events)
    elif choice == "3":
        filter_by_category(events)
    else:
        print("Невірний вибір.")


# --- за датою ---
def filter_by_date(events):
    date = input("Дата (YYYY-MM-DD): ")

    found = False
    for e in events:
        if e["date"] == date:
            print_event(e)
            found = True

    if not found:
        print("Подій немає.")


# --- за періодом ---
def filter_by_period(events):

    try:
        start = datetime.strptime(input("Дата початку: "), "%Y-%m-%d")
        end = datetime.strptime(input("Дата кінця: "), "%Y-%m-%d")
    except:
        print("Невірний формат дат.")
        return

    found = False

    for e in events:
        d = datetime.strptime(e["date"], "%Y-%m-%d")

        if start <= d <= end:
            print_event(e)
            found = True

    if not found:
        print("Подій немає.")


# --- за категорією ---
def filter_by_category(events):

    category = input("Категорія: ").lower()

    found = False

    for e in events:
        if category in e["category"].lower():
            print_event(e)
            found = True

    if not found:
        print("Подій немає.")


# ---------- Редагування ----------
def edit_event(events):

    sorted_events = sort_events(events)
    show_events(events)

    num = int(input("Номер події: "))

    if not (1 <= num <= len(sorted_events)):
        print("Невірний номер.")
        return

    selected = sorted_events[num - 1]
    index = events.index(selected)
    event = events[index]

    name = input(f"Назва ({event['name']}): ")
    date = input(f"Дата ({event['date']}): ")
    time = input(f"Час ({event['time']}): ")
    category = input(f"Категорія ({event['category']}): ")

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


# ---------- Видалення ----------
def delete_event(events):

    sorted_events = sort_events(events)
    show_events(events)

    num = int(input("Номер події: "))

    if not (1 <= num <= len(sorted_events)):
        print("Невірний номер.")
        return

    events.remove(sorted_events[num - 1])
    save_events(events)

    print("Подію видалено.")


# ---------- MAIN ----------
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
            filter_menu(events)

        elif command == "редагувати":
            edit_event(events)

        elif command == "видалити":
            delete_event(events)

        elif command == "вийти":
            print("До побачення!")
            break

        else:
            print("Невідома команда. Напишіть 'допомога'.")


if __name__ == "__main__":
    main()
