import customtkinter as ctk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import time

# Настройка темы (можно изменить на 'light')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class BotManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Minecraft Bot Manager 24/7")
        self.geometry("600x500")
        self.resizable(False, False)

        self.process = None
        self.is_running = False
        self.worker_thread = None

        self._create_widgets()

    def _create_widgets(self):
        # Фрейм для настроек
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(padx=20, pady=20, fill="x")

        # IP и Порт
        ctk.CTkLabel(settings_frame, text="IP:PORT Сервера:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.ip_entry = ctk.CTkEntry(settings_frame, width=250, placeholder_text="localhost:25565")
        self.ip_entry.grid(row=0, column=1, padx=10, pady=10)
        self.ip_entry.insert(0, "localhost:25565")

        # Никнейм
        ctk.CTkLabel(settings_frame, text="Никнейм бота:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.nick_entry = ctk.CTkEntry(settings_frame, width=250, placeholder_text="Bot_Nickname")
        self.nick_entry.grid(row=1, column=1, padx=10, pady=10)

        # Пароль
        ctk.CTkLabel(settings_frame, text="Пароль (опционально):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.pass_entry = ctk.CTkEntry(settings_frame, width=250, placeholder_text="********", show="*")
        self.pass_entry.grid(row=2, column=1, padx=10, pady=10)

        # Кнопки управления
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        self.start_btn = ctk.CTkButton(btn_frame, text="▶ Запустить бота", command=self.start_bot, fg_color="green", hover_color="darkgreen", width=150)
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(btn_frame, text="⏹ Остановить", command=self.stop_bot, fg_color="red", hover_color="darkred", width=150, state="disabled")
        self.stop_btn.pack(side="left", padx=10)

        # Консоль вывода
        self.log_area = scrolledtext.ScrolledText(self, wrap="word", bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 10), state="disabled")
        self.log_area.pack(padx=20, pady=10, fill="both", expand=True)

    def log(self, message):
        """Безопасный вывод текста в консоль из любого потока"""
        self.log_area.config(state="normal")
        self.log_area.insert("end", message + "\n")
        self.log_area.see("end")
        self.log_area.config(state="disabled")

    def start_bot(self):
        ip = self.ip_entry.get().strip()
        nick = self.nick_entry.get().strip()
        pwd = self.pass_entry.get().strip()

        if not ip or not nick:
            messagebox.showerror("Ошибка", "IP и Никнейм обязательны для заполнения!")
            return

        # Определяем путь к NodeJS скрипту относительно текущего файла
        base_dir = os.path.dirname(os.path.abspath(__file__))
        node_dir = os.path.join(base_dir, "..", "NodeJS")
        script_path = os.path.join(node_dir, "index.js")

        if not os.path.exists(script_path):
            messagebox.showerror("Ошибка", f"Не найден файл:\n{script_path}")
            return

        # Формируем команду
        cmd = ["node", script_path, ip, nick]
        if pwd:
            cmd.append(pwd)

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.log(">>> Запуск бота...")

        # Запускаем в отдельном потоке, чтобы GUI не зависал
        self.worker_thread = threading.Thread(target=self._run_process_loop, args=(cmd, node_dir), daemon=True)
        self.worker_thread.start()

    def _run_process_loop(self, cmd, cwd):
        """Цикл, который держит бота 24/7 и переподключает при падении"""
        while self.is_running:
            # errors='replace' спасет от краша, если Node.js выведет странные символы
            self.process = subprocess.Popen(
                cmd, 
                cwd=cwd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                encoding='utf-8', 
                errors='replace'
            )
            
            # Читаем вывод Node.js
            for line in self.process.stdout:
                if not self.is_running:
                    break
                # Вызываем log через after, чтобы обновить GUI из главного потока
                self.after(0, self.log, line.strip())

            self.process.wait()
            
            if self.is_running:
                self.after(0, self.log, ">>> Бот отключился. Переподключение через 5 секунд...")
                time.sleep(5)

    def stop_bot(self):
        self.is_running = False
        if self.process:
            self.process.terminate()
            self.process = None
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.after(0, self.log, ">>> Бот остановлен пользователем.")

if __name__ == "__main__":
    app = BotManagerApp()
    app.mainloop()