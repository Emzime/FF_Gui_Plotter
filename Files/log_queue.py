# log_queue.py
import os
import threading
import tkinter as tk
import queue
import datetime
from Files.translation import Lang


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
        if self.plotter_gui.logs_status == Lang.translate("on"):
            # Ajout de la date et l'heure au nom de fichier
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            # Chemin du répertoire où est situé le script
            directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            # Chemin du répertoire des logs
            logFileName = f"{self.config_manager.log_name}{current_datetime}.log"
            self.log_path = os.path.join(directory_path, "Logs", logFileName)
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            self.static_method.configure_logging(filename=self.log_path)

            # Chemin du répertoire des logs d'erreurs
            logFileNameError = f"{self.config_manager.log_error_name}{current_datetime}.log"
            self.log_error_path = os.path.join(directory_path, "Logs", logFileNameError)
            os.makedirs(os.path.dirname(self.log_error_path), exist_ok=True)
            self.static_method.configure_error_logging(filename=self.log_error_path)

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
        # Si logs_status est actif, activez la journalisation dans un fichier
        if self.plotter_gui.logs_status == Lang.translate("on"):
            # Ouvrir le fichier de journal en mode ajout
            with open(self.log_path, "a") as log_file:
                # Parcourir chaque ligne de la sortie standard
                for line in stdout:
                    # Afficher la ligne dans l'interface utilisateur
                    self.log_plotter_message(line)
                    # Ajouter la ligne à la file d'attente log_progress_messages
                    self.log_progress_messages(line)
                    # Écrire la ligne dans le fichier de journal
                    log_file.write(line)
        else:
            # Si la journalisation dans un fichier est désactivée, affichez simplement les messages dans l'interface utilisateur
            for line in stdout:
                # Afficher la ligne dans l'interface utilisateur
                self.log_plotter_message(line)
                # Ajouter la ligne à la file d'attente log_progress_messages
                self.log_progress_messages(line)

    def read_stderr(self, stderr):
        # Si logs_status est actif, activez la journalisation des erreurs dans un fichier
        if self.plotter_gui.logs_status == Lang.translate("on"):
            # Ouvrir le fichier de journal en mode ajout
            with open(self.log_error_path, "a") as log_error_file:
                # Parcourir chaque ligne de la sortie standard
                for line in stderr:
                    # Ajoutez la ligne à la file d'attente des erreurs de journal
                    self.queue_logs.log_queue_errors.put(line)
                    # Écrire la ligne dans le fichier de journal
                    log_error_file.write(line)
        else:
            # Lit la sortie d'erreur de plotter et affiche les messages dans le journal
            for line in stderr:
                # Ajoutez la ligne à la file d'attente des erreurs de journal
                self.queue_logs.log_queue_errors.put(line)

    def log_errors_messages(self):
        while True:
            # Récupérer le message de la file d'attente des erreurs de journal
            message = self.queue_logs.log_queue_errors.get()
            if message == "STOP":
                break

            # Ajoutez le timestamp
            timestamp = datetime.datetime.now().strftime("%Hh%M")

            # Affiche un message d'erreur dans le journal
            self.interface.errors_text.insert(tk.END, f"[{timestamp}]", "timestamp")
            self.interface.errors_text.insert(tk.END, f" {message}", "error")
            self.interface.errors_text.insert(tk.END, "\n")
            self.interface.errors_text.see(tk.END)
            self.plotter_gui.update_idletasks()

    def log_message(self):
        while True:
            message, style = self.queue_logs.log_queue_messages.get()

            # Ajoutez le timestamp
            timestamp = datetime.datetime.now().strftime("%Hh%M")

            # Affiche un message de plotter dans le journal de plotter
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
        # Ajoutez le timestamp
        timestamp = datetime.datetime.now().strftime("%Hh%M")

        # Affiche un message de plotter dans le journal de plotter
        self.interface.log_blade.insert(tk.END, f"[{timestamp}]", "timestamp")
        self.interface.log_blade.insert(tk.END, f" {message}", "message")
        self.interface.log_blade.see(tk.END)
        self.plotter_gui.update_idletasks()

    def log_progress_messages(self, message):
        # Stockez la ligne dans la liste
        self.lists.output_lines.append(message.strip())
