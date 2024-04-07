# log_queue.py
import threading
import tkinter as tk
import queue
from datetime import datetime


class LogQueue:
    def __init__(self):
        # Créez une file pour stocker les messages de log pour les messages
        self.log_queue_messages = queue.Queue()
        # Créez une file pour stocker les messages d'erreurs'
        self.log_queue_errors = queue.Queue()


class LogManager:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.queue_logs = ff_plotter_gui.queue_logs
        self.lists = ff_plotter_gui.lists
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.none_false_variable = ff_plotter_gui.none_false_variable
        self.static_method = ff_plotter_gui.static_method
        self.interface = ff_plotter_gui.interface

        # Si self.plotter_gui.logs_status est True, activez la journalisation dans un fichier
        if self.plotter_gui.logs_status == "on":
            self.static_method.configure_logging(filename="FF_Plot_log")

        # Démarrage des threads de journalisation
        self.start_log_threads()
        self.start_error_threads()

    def start_log_threads(self):
        # Créez et démarrez des threads pour la journalisation de l'interface
        log_thread_messages = threading.Thread(target=self.log_message)
        log_thread_messages.daemon = True
        log_thread_messages.start()

    def start_error_threads(self):
        # Créez et démarrez des threads pour la journalisation des erreurs
        log_thread_errors = threading.Thread(target=self.log_errors_messages)
        log_thread_errors.daemon = True
        log_thread_errors.start()

    def read_stdout(self, stdout):
        # Lit la sortie standard de plotter et affiche les messages dans le journal
        for line in stdout:
            self.log_plotter_message(line)
            # Ajoutez la ligne à la file d'attente log_progress_messages
            self.log_progress_messages(line)

    def read_stderr(self, stderr):
        # Lit la sortie d'erreur de plotter et affiche les messages dans le journal
        for line in stderr:
            # Ajoutez la ligne à la file d'attente log_queue_errors
            self.queue_logs.log_queue_errors.put(line)

    def log_errors_messages(self):
        while True:
            message = self.queue_logs.log_queue_errors.get()
            if message == "STOP":
                break
            timestamp = datetime.now().strftime("%H:%M")
            self.interface.errors_text.insert(tk.END, f"[{timestamp}]", "timestamp")
            self.interface.errors_text.insert(tk.END, f" {message}", "error")
            self.interface.errors_text.insert(tk.END, "\n")
            self.interface.errors_text.see(tk.END)
            self.plotter_gui.update_idletasks()

    def log_message(self):
        while True:
            message, style = self.queue_logs.log_queue_messages.get()
            timestamp = datetime.now().strftime("%H:%M")

            # Vérifie si le style est défini, sinon utilisez un style par défaut
            if style:
                self.interface.log_text.insert(tk.END, f"[{timestamp}]", "timestamp")
                self.interface.log_text.insert(tk.END, f" {message}", style)
            else:
                self.interface.log_text.insert(tk.END, f"[{timestamp}]", "timestamp")
                self.interface.log_text.insert(tk.END, f" {message}")

            self.interface.log_text.insert(tk.END, "\n")
            self.interface.log_text.see(tk.END)
            self.plotter_gui.update_idletasks()

    def log_plotter_message(self, message):
        # Affiche un message de plotter dans le journal de plotter
        timestamp = datetime.now().strftime("%H:%M")
        # Ajoutez le timestamp avec le tag "timestamp"
        self.interface.log_blade.insert(tk.END, f"[{timestamp}]", "timestamp")
        self.interface.log_blade.insert(tk.END, f" {message}", "message")
        self.interface.log_blade.see(tk.END)
        self.plotter_gui.update_idletasks()

    def log_progress_messages(self, message):
        # Stockez la ligne dans la liste
        self.lists.output_lines.append(message.strip())
