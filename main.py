import tkinter as tk
from tkinter import ttk, messagebox
import requests

# Список монет для отображения (id из CoinGecko)
CRYPTO_COINS = [
    ("Bitcoin", "bitcoin"),
    ("Ethereum", "ethereum"),
    ("Solana", "solana"),
    ("Cardano", "cardano"),
    ("Dogecoin", "dogecoin")
]

def fetch_prices():
    """Получает цены через CoinGecko API"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coin[1] for coin in CRYPTO_COINS),
        "vs_currencies": "usd"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        return None

def on_refresh():
    # Блокируем кнопку во время загрузки (чтобы не нажимали много раз)
    btn_refresh.config(state="disabled")
    lbl_updated.config(text="Загрузка...")

    data = fetch_prices()

    if data is None:
        messagebox.showerror("Ошибка", "Не удалось получить курсы.\nПроверьте интернет или попробуйте позже.")
        lbl_updated.config(text="Обновлено: —")
        btn_refresh.config(state="normal")
        return

    # Очищаем и заполняем таблицу
    for widget in frame_table.winfo_children():
        widget.destroy()

    # Заголовки таблицы
    ttk.Label(frame_table, text="Криптовалюта", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10)
    ttk.Label(frame_table, text="Цена (USD)", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="e", padx=10)

    row = 1
    for name, coin_id in CRYPTO_COINS:
        price = data.get(coin_id, {}).get("usd")
        if price is not None:
            # Форматируем цену: 2 знака после запятой, с разделителями тысяч
            price_str = f"{price:,.2f}"
            ttk.Label(frame_table, text=name).grid(row=row, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(frame_table, text=price_str).grid(row=row, column=1, sticky="e", padx=10, pady=5)
        else:
            ttk.Label(frame_table, text=name, foreground="gray").grid(row=row, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(frame_table, text="Нет данных", foreground="gray").grid(row=row, column=1, sticky="e", padx=10, pady=5)
        row += 1

    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")
    lbl_updated.config(text=f"Обновлено: {now}")
    btn_refresh.config(state="normal")
# Автообновление раз в 2 минуты
    root.after(120000, on_refresh)

# Создаём главное окно
root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("450x400")

# Заголовок
lbl_title = ttk.Label(root, text="Курсы криптовалют", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

# Место под таблицу курсов
frame_table = ttk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=5)

# Кнопка «Обновить курсы»
btn_refresh = ttk.Button(root, text="Обновить курсы", command=on_refresh)
btn_refresh.pack(pady=10)

# Подпись «Обновлено: ...»
lbl_updated = ttk.Label(root, text="Обновлено: —", foreground="gray")
lbl_updated.pack(side="bottom", pady=10)
# Первое обновление сразу при старте
root.after(0, on_refresh)
# Запускаем цикл обработки событий
root.mainloop()