import pandas as pd
import numpy as np


def generate_data(num_rows: int = 100) -> pd.DataFrame:
    np.random.seed(42)

    categories = ["Electronics", "Clothing", "Home", "Books", "Sports"]
    return_statuses = ["Returned", "Not Returned"]
    payment_methods = ["Card", "Cash", "Online"]

    data = {
        "order_id": np.arange(1, num_rows + 1),
        "date": pd.date_range(start="2024-01-01", periods=num_rows, freq="D"),
        "amount": np.round(np.random.uniform(10, 1000, num_rows), 2),
        "category": np.random.choice(categories, num_rows),
        "return_status": np.random.choice(return_statuses, num_rows, p=[0.2, 0.8]),
        "payment_method": np.random.choice(payment_methods, num_rows),
        "quantity": np.random.randint(1, 6, num_rows)
    }

    df = pd.DataFrame(data)
    return df


def main():
    df = generate_data()

    # Анализируем только реальные бизнес-метрики
    stats = df[["amount", "quantity"]].describe()

    # Дополнительная бизнес-метрика: средняя сумма заказа по категориям
    avg_by_category = df.groupby("category")["amount"].mean().round(2)

    with open("result.txt", "w", encoding="utf-8") as file:
        file.write("E-commerce Sales Analysis Report\n")
        file.write("=" * 40 + "\n\n")

        file.write("Generated dataset preview:\n")
        file.write(df.head().to_string(index=False))
        file.write("\n\n")

        file.write("Descriptive statistics for business metrics:\n")
        file.write(stats.to_string())
        file.write("\n\n")

        file.write("Average order amount by category:\n")
        file.write(avg_by_category.to_string())
        file.write("\n")

    with open("result.txt", "r", encoding="utf-8") as file:
        print(file.read())


if __name__ == "__main__":
    main()
