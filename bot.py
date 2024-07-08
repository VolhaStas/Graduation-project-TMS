import pandas as pd
import numpy as np

# Словарь для хранения информации о расходах
expenses = {}

# Обработчик команды /start
def start():
    try:
        print("Привет! Чтобы начать, введите количество людей:")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Обработчик команды /names
def handle_names():
    try:
        num_people = int(input())
        for i in range(num_people):
            name = input(f"Введите имя человека #{i+1}: ")
            expenses[name] = {}
        print("Отлично! Теперь внесите суммы расходов каждого человека.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Обработчик команды /expenses
def handle_expenses():
    try:
        for name in expenses.keys():
            amount = float(input(f"Введите сумму расходов для {name}: "))
            expenses[name]["Потрачено"] = round(amount, 2)
        print("Расходы были успешно учтены.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Обработчик команды /calculate
def calculate():
    try:
        # Создание таблицы с информацией о затратах
        df = pd.DataFrame(expenses.items(), columns=["Человек", "Информация"])
        df["Потрачено"] = df["Информация"].apply(lambda x: round(x.get("Потрачено", 0), 2))
        total_expenses = df["Потрачено"].sum()

        num_people = len(expenses)  # Количество людей

        for i, row in df.iterrows():
            name = row["Человек"]
            spent = row["Потрачено"]
            df.at[i, "Должен"] = round(total_expenses / num_people - spent, 2)
            if name in expenses:
                df.at[i, "Должен"] += spent

            for j, other_row in df.iterrows():
                if i != j:
                    other_name = other_row["Человек"]
                    df.at[i, other_name] = round(spent / num_people, 2)

        total_row = {
            "Человек": "Всего",
            "Потрачено": round(total_expenses, 2),
            "Должен": round(df["Должен"].sum(), 2),
            **{name: 0 for name in expenses.keys()}
        }
        df = pd.concat([df, pd.DataFrame(total_row, index=[0])], ignore_index=True)

        df = df.replace(np.nan, "-")
        df = df.drop(columns=["Информация"])  # Удаление столбца "Информация"

        table_text = df.to_string(index=False)
        print(table_text)
        print("\n")
        print("Долги:")
        for i, row in df.iterrows():
            name = row["Человек"]
            for other_name in expenses.keys():
                if name != "Всего":
                    amount = row[other_name]
                    if isinstance(amount, float) and amount > 0:
                        print(f"{name} должен(а) {amount} {other_name}")
                    elif isinstance(amount, float) and amount < 0:
                        print(f"{other_name} должен(а) {-amount} {name}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Основная функция для запуска бота
def main():
    try:
        start()
        handle_names()
        handle_expenses()
        calculate()
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Запуск бота
if __name__ == "__main__":
    main()