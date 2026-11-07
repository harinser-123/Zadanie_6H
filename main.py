import tkinter as tk
from tkinter import ttk, messagebox

def on_refresh():
    # Сюда позже добавим запрос к CoinGecko
    messagebox.showinfo("Инфо", "Кнопка «Обновить курсы» нажата!\nЗдесь будет загрузка данных.")

# Создаём главное окно
root = tk.Tk()
root.title("Курсы криптовалют")
root.geometry("400x300")

# Заголовок
lbl_title = ttk.Label(root, text="Курсы криптовалют", font=("Arial", 16, "bold"))
lbl_title.pack(pady=20)

# Место под таблицу курсов (пока просто рамка)
frame_table = ttk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=5)

# Кнопка «Обновить курсы»
btn_refresh = ttk.Button(root, text="Обновить курсы", command=on_refresh)
btn_refresh.pack(pady=10)

# Подпись «Обновлено: ...»
lbl_updated = ttk.Label(root, text="Обновлено: —", foreground="gray")
lbl_updated.pack(side="bottom", pady=10)

# Запускаем цикл обработки событий
root.mainloop()