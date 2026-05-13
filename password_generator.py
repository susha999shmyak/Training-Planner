#!/usr/bin/env python3
"""
Random Password Generator - GUI приложение для генерации безопасных паролей
Автор: Иван Петров
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
from datetime import datetime
import os

class PasswordGenerator:
    """Класс генератора паролей"""

    def __init__(self):
        # Настройки по умолчанию
        self.length = 12
        self.use_digits = True
        self.use_letters = True
        self.use_special = True
        self.history_file = "history.json"
        self.history = []
        self.load_history()

    def generate(self) -> str:
        """Генерация пароля на основе текущих настроек"""
        char_pools = []

        if self.use_letters:
            char_pools.append(string.ascii_letters)
        if self.use_digits:
            char_pools.append(string.digits)
        if self.use_special:
            char_pools.append("!@#$%^&*()_+-=[]{}|;:,.<>?")

        # Если не выбран ни один тип символов
        if not char_pools:
            raise ValueError("Выберите хотя бы один тип символов")

        all_chars = ''.join(char_pools)

        # Генерация пароля
        password = ''.join(random.choice(all_chars) for _ in range(self.length))

        # Перемешивание для лучшей случайности
        password_list = list(password)
        random.shuffle(password_list)

        return ''.join(password_list)

    def save_to_history(self, password: str) -> None:
        """Сохранение пароля в историю"""
        record = {
            "password": password,
            "length": self.length,
            "use_digits": self.use_digits,
            "use_letters": self.use_letters,
            "use_special": self.use_special,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        self.history.insert(0, record)  # Новые записи в начало
        # Ограничиваем историю 50 записями
        if len(self.history) > 50:
            self.history = self.history[:50]

        self.save_history()

    def load_history(self) -> None:
        """Загрузка истории из JSON файла"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except (json.JSONDecodeError, IOError):
            self.history = []

    def save_history(self) -> None:
        """Сохранение истории в JSON файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except IOError:
            messagebox.showerror("Ошибка", "Не удалось сохранить историю")

    def clear_history(self) -> None:
        """Очистка истории"""
        self.history = []
        self.save_history()


class PasswordGeneratorGUI:
    """GUI приложение для генерации паролей"""

    def __init__(self):
        self.root = tk.Tk()
        self.generator = PasswordGenerator()

        self.setup_window()
        self.create_widgets()
        self.update_history_table()

    def setup_window(self):
        """Настройка главного окна"""
        self.root.title("Генератор случайных паролей")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Установка иконки (опционально)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Центрирование окна
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Создание всех виджетов интерфейса"""

        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)  # Для таблицы истории

        # ===== ЗАГОЛОВОК =====
        title_label = ttk.Label(main_frame, text="🔐 Генератор случайных паролей",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=10)

        # ===== НАСТРОЙКА ДЛИНЫ =====
        length_frame = ttk.LabelFrame(main_frame, text="Длина пароля", padding="10")
        length_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        length_frame.columnconfigure(1, weight=1)

        ttk.Label(length_frame, text="Длина:").grid(row=0, column=0, padx=5)

        # Ползунок длины
        self.length_var = tk.IntVar(value=self.generator.length)
        self.length_slider = ttk.Scale(length_frame, from_=4, to=32,
                                       orient=tk.HORIZONTAL,
                                       variable=self.length_var,
                                       command=self.on_length_change)
        self.length_slider.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)

        # Отображение текущей длины
        self.length_label = ttk.Label(length_frame, text=f"{self.generator.length} символов")
        self.length_label.grid(row=0, column=2, padx=5)

        # ===== ВЫБОР СИМВОЛОВ =====
        chars_frame = ttk.LabelFrame(main_frame, text="Типы символов", padding="10")
        chars_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)

        # Чекбоксы
        self.letters_var = tk.BooleanVar(value=self.generator.use_letters)
        self.digits_var = tk.BooleanVar(value=self.generator.use_digits)
        self.special_var = tk.BooleanVar(value=self.generator.use_special)

        ttk.Checkbutton(chars_frame, text="Буквы (A-Z, a-z)",
                       variable=self.letters_var,
                       command=self.update_generator_settings).grid(row=0, column=0, sticky=tk.W)

        ttk.Checkbutton(chars_frame, text="Цифры (0-9)",
                       variable=self.digits_var,
                       command=self.update_generator_settings).grid(row=1, column=0, sticky=tk.W)

        ttk.Checkbutton(chars_frame, text="Специальные символы (!@#$%^&*)",
                       variable=self.special_var,
                       command=self.update_generator_settings).grid(row=2, column=0, sticky=tk.W)

        # ===== КНОПКИ =====
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=3, column=0, pady=10)

        self.generate_btn = ttk.Button(buttons_frame, text="🎲 Сгенерировать пароль",
                                       command=self.generate_password)
        self.generate_btn.grid(row=0, column=0, padx=5)

        self.copy_btn = ttk.Button(buttons_frame, text="📋 Копировать",
                                   command=self.copy_to_clipboard, state='disabled')
        self.copy_btn.grid(row=0, column=1, padx=5)

        self.clear_btn = ttk.Button(buttons_frame, text="🗑️ Очистить историю",
                                   command=self.clear_history)
        self.clear_btn.grid(row=0, column=2, padx=5)

        # ===== ОТОБРАЖЕНИЕ ПАРОЛЯ =====
        password_frame = ttk.LabelFrame(main_frame, text="Сгенерированный пароль", padding="10")
        password_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        password_frame.columnconfigure(0, weight=1)

        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var,
                                        font=('Courier', 12), state='readonly')
        self.password_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)

        # ===== ИСТОРИЯ =====
        history_frame = ttk.LabelFrame(main_frame, text="История паролей", padding="10")
        history_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(0, weight=1)

        # Создание таблицы истории
        columns = ('password', 'length', 'chars', 'created_at')
        self.history_table = ttk.Treeview(history_frame, columns=columns, show='headings')

        # Настройка заголовков
        self.history_table.heading('password', text='Пароль')
        self.history_table.heading('length', text='Длина')
        self.history_table.heading('chars', text='Типы символов')
        self.history_table.heading('created_at', text='Дата создания')

        # Настройка ширины колонок
        self.history_table.column('password', width=200)
        self.history_table.column('length', width=60)
        self.history_table.column('chars', width=200)
        self.history_table.column('created_at', width=150)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL,
                                  command=self.history_table.yview)
        self.history_table.configure(yscrollcommand=scrollbar.set)

        self.history_table.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Контекстное меню для копирования из истории
        self.setup_context_menu()

        # Статусбар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var,
                               relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=5)

    def setup_context_menu(self):
        """Создание контекстного меню для таблицы истории"""
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать пароль",
                                     command=self.copy_selected_password)
        self.context_menu.add_command(label="Копировать все",
                                     command=self.copy_all_passwords)

        self.history_table.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Отображение контекстного меню"""
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_password(self):
        """Копирование выбранного пароля в буфер обмена"""
        selection = self.history_table.selection()
        if selection:
            item = self.history_table.item(selection[0])
            password = item['values'][0]
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.status_var.set("✅ Пароль скопирован в буфер обмена")
            self.root.after(2000, lambda: self.status_var.set("Готов к работе"))

    def copy_all_passwords(self):
        """Копирование всех паролей в буфер обмена"""
        passwords = [self.history_table.item(item)['values'][0]
                    for item in self.history_table.get_children()]
        if passwords:
            all_passwords = "\n".join(passwords)
            self.root.clipboard_clear()
            self.root.clipboard_append(all_passwords)
            self.status_var.set(f"✅ Скопировано {len(passwords)} паролей")
            self.root.after(2000, lambda: self.status_var.set("Готов к работе"))

    def on_length_change(self, value):
        """Обработчик изменения длины пароля"""
        length = int(float(value))
        self.generator.length = length
        self.length_label.config(text=f"{length} символов")
        self.update_generator_settings()

    def update_generator_settings(self):
        """Обновление настроек генератора"""
        self.generator.use_letters = self.letters_var.get()
        self.generator.use_digits = self.digits_var.get()
        self.generator.use_special = self.special_var.get()

        # Проверка выбора
        if not any([self.generator.use_letters,
                   self.generator.use_digits,
                   self.generator.use_special]):
            self.generate_btn.config(state='disabled')
            self.status_var.set("⚠️ Выберите хотя бы один тип символов")
        else:
            self.generate_btn.config(state='normal')
            self.status_var.set("Готов к работе")

    def generate_password(self):
        """Генерация и отображение пароля"""
        try:
            # Проверка корректности длины
            if self.generator.length < 4:
                self.generator.length = 4
                self.length_var.set(4)
                self.length_label.config(text="4 символов")

            if self.generator.length > 32:
                self.generator.length = 32
                self.length_var.set(32)
                self.length_label.config(text="32 символов")

            # Генерация пароля
            password = self.generator.generate()

            # Отображение пароля
            self.password_var.set(password)
            self.copy_btn.config(state='normal')

            # Сохранение в историю
            self.generator.save_to_history(password)

            # Обновление таблицы истории
            self.update_history_table()

            self.status_var.set("✅ Пароль успешно сгенерирован")
            self.root.after(2000, lambda: self.status_var.set("Готов к работе"))

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать пароль: {e}")

    def update_history_table(self):
        """Обновление таблицы истории"""
        # Очистка таблицы
        for item in self.history_table.get_children():
            self.history_table.delete(item)

        # Добавление записей
        for record in self.generator.history:
            # Формирование строки с типами символов
            char_types = []
            if record.get('use_letters', True):
                char_types.append("буквы")
            if record.get('use_digits', True):
                char_types.append("цифры")
            if record.get('use_special', True):
                char_types.append("спецсимволы")

            chars_str = ", ".join(char_types) if char_types else "не выбрано"

            self.history_table.insert('', 0, values=(
                record['password'],
                record['length'],
                chars_str,
                record['created_at']
            ))

    def copy_to_clipboard(self):
        """Копирование текущего пароля в буфер обмена"""
        password = self.password_var.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.status_var.set("✅ Пароль скопирован в буфер обмена")
            self.root.after(2000, lambda: self.status_var.set("Готов к работе"))

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение",
                               "Вы уверены, что хотите очистить всю историю паролей?"):
            self.generator.clear_history()
            self.update_history_table()
            self.status_var.set("🗑️ История очищена")
            self.root.after(2000, lambda: self.status_var.set("Готов к работе"))

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


def main():
    """Главная функция запуска приложения"""
    try:
        app = PasswordGeneratorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Критическая ошибка", f"Не удалось запустить приложение: {e}")


if __name__ == "__main__":
    main()
