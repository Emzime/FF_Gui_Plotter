import logging
import os
import platform
import sys

import psutil
import queue
import re
import shutil
import signal
import subprocess
import threading
import time
import math
import tkinter as tk
import tkinter.messagebox
from datetime import datetime
from tkinter import ttk, filedialog, Frame
from ttkthemes.themed_style import ThemedStyle


class Welcome:
    def __init__(self, ff_plotter_gui):
        self.config_manager = ff_plotter_gui.config_manager
        self.queue_logs = ff_plotter_gui.queue_logs
        self.log_manager = ff_plotter_gui.log_manager

    def show_message(self):
        # Message de premier lancement et création du fichier de configuration avec les valeurs par défaut
        if not os.path.exists(self.config_manager.config_file):
            self.queue_logs.log_queue_messages.put((
                "Hello French Farmer's,\n"
                "C'est la première fois que tu lance l'application.\n"
                "Tu dois renseigner les champs sur la gauche puis cliquer sur 'Lancer la création'.\n\n"
                f"Un fichier de configuration portant le nom de '{self.config_manager.config_file}' sera enregistré dans le même répertoire que ce script "
                "et sera sauvegardé à chaque modification que tu feras.\n\n", None))
        else:
            self.queue_logs.log_queue_messages.put(("Content de te revoir, prêt à plotter ?", None))


class Lists:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.interface = ff_plotter_gui.interface
        self.config_manager = ff_plotter_gui.config_manager

        plotter = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")

        # Initialisation de la liste des messages de progression
        self.output_lines = []

        # Liste des étapes de progression à rechercher
        if plotter == "bladebit_cuda":
            self.progress_steps = [
                "Generating plot",
                "Generating F1",
                "Finished F1 in",
                "Table 2 completed in",
                "Table 3 completed in",
                "Table 4 completed in",
                "Table 5 completed in",
                "Table 6 completed in",
                "Table 7 completed in",
                "Finalizing Table 7",
                "Finalized Table 7 in",
                "Completed Phase 1 in",
                "Marked Table 6 in",
                "Marked Table 5 in",
                "Marked Table 4 in",
                "Marked Table 3 in",
                "Completed Phase 2 in",
                "Compressing Table 2 and 3...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Completed table 2 in",
                "Compressing tables 3 and 4...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 3 in",
                "Compressing tables 4 and 5...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 4 in",
                "Compressing tables 5 and 6...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 5 in",
                "Compressing tables 6 and 7...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 6 in",
                "Completed Phase 3 in",
                "Completed Plot",
                "Completed writing plot in"
            ]
        else:
            self.progress_steps = [
                "[P1] Setup took",
                "[P1] Table 1 took",
                "[P1] Table 2 took",
                "[P1] Table 3 took",
                "[P1] Table 4 took",
                "[P1] Table 5 took",
                "[P1] Table 6 took",
                "[P1] Table 7 took",
                "Phase 1 took",
                "Phase 2 took",
                "[P3] Setup took",
                "Phase 3 took",
                "[P4] Setup took",
                "Phase 4 took",
                "Total plot creation time was"
            ]

        # Désactiver tous les éléments de l'interface pendant la création
        self.check_plot_elements_disable = [
            self.interface.check_plot_value_combobox,
            self.interface.check_threshold_value_combobox,
            self.interface.compression_combobox,
            self.interface.ram_qty_combobox,
            self.interface.contract_entry,
            self.interface.farmer_key_entry,
            self.interface.ssd_temp_entry,
            self.interface.ssd_temp_button,
            self.interface.ssd_temp2move_entry,
            self.interface.ssd_temp2move_button,
            self.interface.plotter_path_combobox,
            self.interface.hdd_dir_listbox,
            self.interface.add_hdd_dir_button,
            self.interface.remove_hdd_dir_button
        ]


class ConfigManager:
    # Nom du fichier de configuration
    config_file = "config.txt"
    config_stats = "stats.txt"

    # Chemin du répertoire où est situé le script
    directory_path = os.path.dirname(__file__)
    plotter_directory = os.path.join(directory_path, "Plotter")

    def __init__(self):
        # Configuration par défaut
        self.defaults = {
            "compression": "5",
            "ram_qty": "128",
            "plotter_executable": "",
            "plotter_path": self.plotter_directory,
            "ssd_temp": "",
            "ssd_temp2move": "",
            "hdd_dir": "",
            "contract": "",
            "farmer_key": "",
            "logs_status": "off",
            "progress_status": "on",
            "check_plot_status": "off",
            "check_plot_value": "30",
            "check_threshold_value": "80"
        }

        self.stats = {
            "total_plot_created": "0",
            "bad_plot_number": "0",
            "deleted_plot_number": "0"
        }

        # Si le fichier de configuration n'existe pas, on le crée avec les valeurs par défauts
        if not os.path.exists(self.config_file):
            self.create_config(self.config_file)

        if not os.path.exists(self.config_stats):
            self.create_config(self.config_stats)

    def create_config(self, file=None):
        config_data = self.defaults if file is None or file == self.config_file else self.stats
        file_path = os.path.join(os.getcwd(), self.config_file) if file is None or file == self.config_file else os.path.join(os.getcwd(), self.config_stats)

        with open(file_path, "w") as f:
            for key, value in config_data.items():
                f.write(f"{key}={value}\n")

    def read_config(self, file=None):
        config_data = {}
        file_path = self.config_file if file is None or file == self.config_file else self.config_stats

        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()  # Supprime les espaces et les caractères de nouvelle ligne
                if not line:
                    continue  # Ignore les lignes vides
                key, value = line.split("=")
                config_data[key] = value

        return config_data

    def update_config(self, new_config, file=None):
        # Choisissez le dictionnaire des valeurs par défaut approprié en fonction du fichier
        default_values = self.defaults if file is None or file == self.config_file else self.stats

        # Construisez le chemin du fichier en fonction de la valeur de file
        file_path = os.path.join(os.getcwd(), self.config_file) if file is None or file == self.config_file else os.path.join(os.getcwd(), self.config_stats)

        # Lire les données de configuration actuelles à partir du fichier
        current_config = {}
        with open(file_path, "r") as f:
            for line in f:
                key, value = line.strip().split("=")
                current_config[key] = value

        # Mettre à jour le dictionnaire actuel avec les nouvelles valeurs
        current_config.update(new_config)

        # Compléter le dictionnaire avec les valeurs par défaut pour les clés manquantes
        for key, value in default_values.items():
            if key not in current_config:
                current_config[key] = value

        # Écrire tout le contenu du dictionnaire mis à jour dans le fichier approprié
        with open(file_path, "w") as f:
            for key, value in current_config.items():
                f.write(f"{key}={value}\n")


class NoneFalseVariables:
    def __init__(self):
        # DEBUG
        self.debug = False
        # Initialisez la variable
        self.process = None
        # Initialisez la variable
        self.plotter_pid = None
        # Initialisez la variable
        self.plotter_process = None
        # Indicateur de création en cours
        self.plot_creation_in_progress = False
        # Drapeau pour contrôler l'arrêt de la création
        self.stop_creation = False
        # Variable pour suivre si current_bad_proof_match a déjà été trouvé
        self.bad_proof_found = False

        self.bad_plot_messages = False
        self.total_plot_created_messages = False

        self.delOldPlots = False


class InitializeVariables:
    def __init__(self):
        # Taille d'un plot par compression
        self.plotSizes = {
            0: 109000000000,
            1: 90409061581,
            2: 88691074663,
            3: 86973087744,
            4: 85255100826,
            5: 83537113908,
            6: 81819126989,
            7: 80101140071,
            8: 76557792052,
            9: 73121818215,
            11: 92019674317,
            12: 88583700480,
            13: 84718229914,
            14: 80208514253,
            15: 76879914599,
            16: 69578470196,
            17: 67645734912,
            18: 64102386893,
            19: 60559038874,
            20: 57015690855,
            29: 51539607552,
            30: 46493020980,
            31: 41446434407,
            32: 36399847834,
            33: 31245887079
        }

        # Initialiser les variables de progressions
        self.max_plots_on_selected_hdd = 0
        self.current_plot_number = 0
        self.current_step = 0
        self.requested_proof = 0
        self.percent_proof = 0


class Pattern:
    def __init__(self):
        # Format des anciens plots
        self.plotFormatPattern = re.compile(r'plot-k3[2-5]-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-[0-9a-fA-F]{32}.*\.plot')

        # N° du plot en cours
        self.currentPlotPattern = re.compile(r'Generating plot (\d+)')

        # Paterne de suppression
        self.currentBadProofPattern = re.compile(r'WARNING: Deleting plot')

        # Paterne de création ne correspondant pas aux preuves demandées
        self.currentBadPercentPattern = re.compile(r'Proofs requested/fetched: (\d+) / (\d+) \( (\d+\.\d+%) \)')

        # Paterne de création réussi
        self.currentCompletedPlot = re.compile(r'Completed writing plot in')


class ProgressBar:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.none_false_variable = ff_plotter_gui.none_false_variable
        self.static_method = ff_plotter_gui.static_method
        self.lists = ff_plotter_gui.lists
        self.pattern = ff_plotter_gui.pattern
        self.queue_logs = ff_plotter_gui.queue_logs
        self.interface = ff_plotter_gui.interface

    def plots_progress(self):
        try:
            # Calcul le nombre d'étapes
            total_steps = len(self.lists.progress_steps)

            while not self.none_false_variable.stop_creation:
                # Boucle sur les lignes de logs
                for line in self.lists.output_lines:
                    # Détection du début d'un nouveau plot
                    current_plot_pattern_match = self.pattern.currentPlotPattern.search(line)
                    if current_plot_pattern_match:
                        requested_pattern_match = current_plot_pattern_match.group(1)
                        if requested_pattern_match is not None:
                            new_plot_number = int(requested_pattern_match)
                            if new_plot_number > self.initialize_variables.current_plot_number:
                                self.initialize_variables.current_plot_number = new_plot_number

                    # Détection du pourcentage de preuves du plot créé
                    current_bad_percent_match = self.pattern.currentBadPercentPattern.search(line)
                    if current_bad_percent_match:
                        requested_proof = current_bad_percent_match.group(1)
                        if requested_proof is not None:
                            # Met à jour la variable
                            self.initialize_variables.requested_proof = int(requested_proof)

                        # Extraction du pourcentage
                        bad_percent_match = re.search(r'(\d+(\.\d+)?)%', current_bad_percent_match.group(3))
                        if bad_percent_match:
                            # Convertit en entier
                            bad_percent = int(float(bad_percent_match.group(1)))
                            # Met à jour la variable
                            self.initialize_variables.percent_proof = bad_percent

                    # Détection de la suppression d'un plot n'ayant pas le pourcentage de preuves voulues
                    current_bad_proof_match = self.pattern.currentBadProofPattern.search(line)
                    #
                    if current_bad_proof_match and self.config_manager.read_config(self.config_manager.config_stats).get("check_plot_status") == "on":
                        # Récupère la valeur du fichier de configuration
                        current_bad_plot_number = self.config_manager.read_config(self.config_manager.config_stats).get("bad_plot_number")
                        current_bad_plot_number = int(current_bad_plot_number) if current_bad_plot_number is not None else 0
                        # Ajoute 1 au total de plot supprimé
                        new_bad_plot_number = current_bad_plot_number + 1
                        # Mise à jour de l'interface graphique
                        self.interface.bad_plot_number_label.config(text=f"{new_bad_plot_number}")
                        # Mise à jour du fichier de configuration
                        self.config_manager.update_config({"bad_plot_number": new_bad_plot_number}, self.config_manager.config_stats)
                        # Initialisation de la variable de message
                        self.none_false_variable.bad_plot_messages = True
                        # Affichez le message
                        self.progress_messages()
                        # Réinitialisation de la progression
                        self.progress_reset()
                        # Relance la création parce que le plot n'a pas le nombre de preuves suffisant
                        self.none_false_variable.bad_proof_found = True

                    # Détection de la création réussie d'un plot
                    current_completed_plot_match = self.pattern.currentCompletedPlot.search(line)
                    if current_completed_plot_match:
                        if not self.none_false_variable.bad_proof_found:
                            # Récupère la valeur du fichier de configuration
                            current_total_plot_created = self.config_manager.read_config(self.config_manager.config_stats).get("total_plot_created")
                            current_total_plot_created = int(current_total_plot_created) if current_total_plot_created is not None else 0
                            # Ajoute 1 au total de plot créé
                            new_total_plot_created = current_total_plot_created + 1
                            # Mise à jour de l'interface graphique
                            self.interface.current_plot_text.config(text=f"{self.initialize_variables.current_plot_number}")
                            self.interface.total_plot_number_label.config(text=f"{new_total_plot_created}")
                            # Mise à jour du fichier de configuration
                            self.config_manager.update_config({"total_plot_created": new_total_plot_created}, self.config_manager.config_stats)
                            # Initialisation de la variable de message
                            self.none_false_variable.total_plot_created_messages = True
                            # Affichez le message
                            self.progress_messages()
                            # Réinitialisation de la progression
                            self.progress_reset()
                            # Réinitialisation de la variable
                            self.none_false_variable.bad_proof_found = False

                    if self.initialize_variables.current_step < len(self.lists.progress_steps):
                        step = self.lists.progress_steps[self.initialize_variables.current_step]
                        if step in line:
                            self.initialize_variables.current_step += 1
                            progress_percentage = (self.initialize_variables.current_step / total_steps) * 100

                            if progress_percentage > 0:
                                # Mise à jour de la barre de progression
                                self.interface.progress_single_plot_bar["value"] = progress_percentage
                                self.interface.progress_label.config(text=f"{progress_percentage:.2f}%")

                            # Mise à jour de l'interface graphique
                            self.plotter_gui.update_idletasks()

                # Pause pour éviter une utilisation excessive du CPU
                time.sleep(0.8)

        except Exception as e:
            self.queue_logs.log_queue_errors.put(f"Erreur lors de la surveillance de la progression: {str(e)}")

    def progress_reset(self):
        self.interface.progress_single_plot_bar["value"] = 0
        self.interface.progress_label.config(text="0%")
        self.initialize_variables.current_step = 0
        self.initialize_variables.requested_proof = 0
        self.none_false_variable.bad_plot_messages = False
        self.none_false_variable.total_plot_created_messages = False
        self.plotter_gui.update_idletasks()

    def progress_messages(self):
        if self.none_false_variable.bad_plot_messages:
            self.lists.output_lines.clear()
            # Affichez le message
            self.queue_logs.log_queue_messages.put((f"Le plot vient d'être supprimé car il n'avait que {self.initialize_variables.requested_proof}%", "warning"))
            self.none_false_variable.bad_plot_messages = False

        if self.none_false_variable.total_plot_created_messages:
            self.lists.output_lines.clear()
            # Affichez le message
            self.queue_logs.log_queue_messages.put((f"Pourcentage de preuves du dernier plot créé: {self.initialize_variables.percent_proof}%", "info"))
            self.none_false_variable.total_plot_created_messages = False


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


class Interface:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.static_method = ff_plotter_gui.static_method

        # Initialisation des éléments de l'interface
        self.root = tk.Tk()

        # Liste pour stocker les exécutables disponibles
        available_executables = []

        # Parcourir les fichiers dans le répertoire "Plotter" et normaliser les chemins
        for file_name in os.listdir(self.config_manager.plotter_directory):
            file_path = os.path.join(self.config_manager.plotter_directory, file_name)
            normalized_file_path = os.path.normpath(file_path)
            if os.path.isfile(normalized_file_path) and os.access(normalized_file_path, os.X_OK):
                available_executables.append(file_name)

        # Récupération de la correspondance
        if self.config_manager.defaults["plotter_executable"]:
            plotter_name = self.config_manager.defaults["plotter_executable"]
            self.root.title(f"French Farmer Gui plotter {plotter_name}")
        else:
            self.root.title("French Farmer Gui plotter")

        # Stylisation avec ttk
        style = ThemedStyle(self.root)
        style.theme_use("clam")
        style.configure("Custom.TLabel", background="#1C1C1C", foreground="#BFBFBF", font=("Helvetica Sans MS", 10))
        style.configure("TButton", font=("Helvetica", 9))
        style.configure("Custom.Horizontal.TProgressbar", troughcolor="#1C1C1C", background="green", thickness=10)

        # Créer une Frame globale
        main_frame = tk.Frame(self.root, bg="#2C2C2C")
        main_frame.grid(row=1, column=0, sticky="nsew")

        # Ajouter la gestion de poids pour ligne 0 de main_frame (redimensionnement vertical)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)

        # Ajoutez des poids pour partager la largeur
        main_frame.grid_columnconfigure(1, weight=1)

        # Créez la Frame supérieure (top_column)
        top_left_column = tk.Frame(main_frame, bg="#2C2C2C")
        top_left_column.grid(row=0, column=0, padx=(10, 5), pady=(5, 0), sticky="nsew")

        # Ajoutez des poids pour centrer verticalement
        top_left_column.grid_rowconfigure(0, weight=1)

        # Ajoutez des poids pour partager la largeur
        top_left_column.grid_columnconfigure(0, weight=1)

        # Bouton pour activer/désactiver la journalisation (à droite)
        logging_frame = tk.Frame(top_left_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        logging_frame.grid(row=0, column=0, padx=0, pady=(10, 10), sticky="nsew")

        # Ajoutez des poids pour partager la largeur
        logging_frame.grid_columnconfigure(0, weight=1)

        # Ajoutez des poids pour centrer verticalement dans logging_frame
        logging_frame.grid_rowconfigure(0, weight=1)

        # Créez un cadre pour partager la largeur entre logging_label et logging_button
        inner_frame = tk.Frame(logging_frame, bg="#1C1C1C")
        inner_frame.grid(row=1, column=0, padx=10, pady=0, sticky="nsew")

        # Ajoutez des poids pour partager la largeur
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=1)

        # Ajoutez des poids pour centrer verticalement dans inner_frame
        inner_frame.grid_rowconfigure(0, weight=1)

        # Bouton on / off des fichiers de logs
        self.logging_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text="Fichier de log")
        self.logging_label.grid(row=0, column=0, padx=(0, 0), pady=(10, 5), sticky="n")

        self.logging_button = tk.Button(inner_frame, border=0, command=self.logs_button_switch)
        self.logging_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.logging_button.grid(row=1, column=0, padx=(0, 0), pady=(5, 10), sticky="n")
        self.logging_button.config(cursor="hand2", state="disabled")

        # Chargez l'image dans une variable de classe spécifique pour le bouton de logging
        logging_button_off_path = self.static_method.resource_path("images/off.png")
        self.logging_button_off = tk.PhotoImage(file=logging_button_off_path)

        logging_button_on_path = self.static_method.resource_path("images/on.png")
        self.logging_button_on = tk.PhotoImage(file=logging_button_on_path)

        # Configurez le bouton de logging en fonction de la valeur de logs_status
        if self.plotter_gui.logs_status == "on":
            self.logging_button.config(image=self.logging_button_on)
            self.logging_label.config(foreground="#00B34D")
            self.logging_label.grid_rowconfigure(0, weight=1)
        else:
            self.logging_button.config(image=self.logging_button_off)
            self.logging_label.config(foreground="#FF2E2E")
            self.logging_label.grid_rowconfigure(0, weight=1)

        # Bouton on / off de plot check
        self.check_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text="Plot Check")
        self.check_label.grid(row=0, column=1, padx=(0, 0), pady=(10, 5), sticky="n")

        self.check_button = tk.Button(inner_frame, border=0, command=self.check_button_switch)
        self.check_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.check_button.grid(row=1, column=1, padx=(0, 0), pady=(5, 10), sticky="n")
        self.check_button.config(cursor="hand2")

        # Chargez l'image dans une variable de classe spécifique pour le bouton de check
        check_button_off_path = self.static_method.resource_path("images/off.png")
        self.check_button_off = tk.PhotoImage(file=check_button_off_path)

        check_button_on_path = self.static_method.resource_path("images/on.png")
        self.check_button_on = tk.PhotoImage(file=check_button_on_path)

        # Configurez le bouton de check en fonction de la valeur de check_plot_status
        if self.plotter_gui.check_plot_status == "on":
            self.check_button.config(image=self.check_button_on)
            self.check_label.config(foreground="#00B34D")
            # Ajoutez des poids pour partager la hauteur
            self.check_label.grid_rowconfigure(0, weight=1)
        else:
            self.check_button.config(image=self.check_button_off)
            self.check_label.config(foreground="#FF2E2E")
            # Ajoutez des poids pour partager la hauteur
            self.check_label.grid_rowconfigure(0, weight=1)

        # Créez la Frame supérieure (top_column)
        top_right_column = tk.Frame(main_frame, bg="#2C2C2C")
        top_right_column.grid(row=0, column=1, padx=(5, 10), pady=(10, 0), sticky="nsew")

        # Ajoutez des poids pour partager la hauteur
        top_right_column.grid_rowconfigure(0, weight=1)
        top_right_column.grid_rowconfigure(1, weight=1)
        # Ajoutez des poids pour partager la largeur
        top_right_column.grid_columnconfigure(0, weight=0)
        top_right_column.grid_columnconfigure(1, weight=1)

        # Crée une Frame pour la progression du plot (à gauche)
        progress_current_plot_frame = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        progress_current_plot_frame.grid(row=0, column=0, padx=(0, 5), pady=(5, 5), sticky="nsew")
        # Ajoutez des poids pour partager la hauteur
        progress_current_plot_frame.grid_rowconfigure(0, weight=1)
        progress_current_plot_frame.grid_rowconfigure(1, weight=1)
        progress_current_plot_frame.grid_rowconfigure(2, weight=1)
        progress_current_plot_frame.grid_rowconfigure(3, weight=1)
        # Ajoutez des poids pour partager la largeur
        progress_current_plot_frame.grid_columnconfigure(0, weight=0)
        progress_current_plot_frame.grid_columnconfigure(1, weight=1)
        progress_current_plot_frame.grid_columnconfigure(2, weight=0)
        progress_current_plot_frame.grid_columnconfigure(3, weight=1)

        # Crée un label pour afficher le nombre total de plots créés
        self.total_plot_text = tk.Label(progress_current_plot_frame, text="Total de plots créés :", bg="#1C1C1C", fg="#BFBFBF")
        self.total_plot_text.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre total de plots créés
        self.total_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("total_plot_created"), bg="#1C1C1C", fg="#BFBFBF")
        self.total_plot_number_label.grid(row=0, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le nombre d'anciens plots supprimés
        self.deleted_plot_text = tk.Label(progress_current_plot_frame, text="Total d'anciens plots supprimés :", bg="#1C1C1C", fg="#BFBFBF")
        self.deleted_plot_text.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre d'anciens plots supprimés
        self.deleted_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("deleted_plot_number"), bg="#1C1C1C", fg="#BFBFBF")
        self.deleted_plot_number_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour le nombre de plots supprimés lors de la création
        self.bad_plot_text = tk.Label(progress_current_plot_frame, text="Total de nouveaux plots supprimés :", bg="#1C1C1C", fg="#BFBFBF")
        self.bad_plot_text.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre de plots supprimés lors de la création
        self.bad_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("bad_plot_number"), bg="#1C1C1C", fg="#BFBFBF")
        self.bad_plot_number_label.grid(row=2, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le texte le numéro du plot en cours
        self.current_plot_max_label = tk.Label(progress_current_plot_frame, text="Plots à créer :", bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_max_label.grid(row=0, column=2, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.current_plot_max_text = tk.Label(progress_current_plot_frame, text=self.initialize_variables.max_plots_on_selected_hdd, bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_max_text.grid(row=0, column=3, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le texte le numéro du plot en cours
        self.current_plot_label = tk.Label(progress_current_plot_frame, text="Plots créés :", bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_label.grid(row=1, column=2, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.current_plot_text = tk.Label(progress_current_plot_frame, text=self.initialize_variables.current_plot_number, bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_text.grid(row=1, column=3, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée une barre de progression pour le plot
        self.progress_single_plot_bar = ttk.Progressbar(progress_current_plot_frame, orient="horizontal", mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_single_plot_bar.grid(row=2, column=2, pady=(0, 0), padx=(14, 5), sticky="ew")

        self.progress_label = tk.Label(progress_current_plot_frame, text="", anchor="center", bg="#1C1C1C", fg="#BFBFBF")
        self.progress_label.grid(row=2, column=3, pady=(0, 0), padx=(0, 5), sticky="ew")

        # Mise à jour de la barre
        self.progress_single_plot_bar["value"] = 0
        self.progress_label.config(text=f"0%")
        self.progress_single_plot_bar.update_idletasks()
        self.progress_label.update_idletasks()

        # Crée une Frame pour la progression du plot
        news_plot_frame = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        news_plot_frame.grid(row=0, column=1, padx=(5, 0), pady=(5, 5), sticky="nsew")

        # Crée un label pour afficher le texte le numéro du plot en cours
        self.news_plot_label = tk.Label(news_plot_frame, text="", bg="#1C1C1C", fg="#BFBFBF")
        self.news_plot_label.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.news_plot_text = tk.Label(news_plot_frame, text=" ", bg="#1C1C1C", fg="#BFBFBF")
        self.news_plot_text.grid(row=0, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Ajoutez des poids pour partager la hauteur
        self.news_plot_label.grid_rowconfigure(0, weight=1)
        self.news_plot_label.grid_rowconfigure(1, weight=1)
        # Ajoutez des poids pour partager la largeur
        self.news_plot_label.grid_columnconfigure(0, weight=0)
        self.news_plot_label.grid_columnconfigure(1, weight=1)

        # Créez la première colonne avec 12 lignes et 2 colonnes
        left_column = tk.Frame(main_frame, bg="#565656", highlightthickness=1, highlightbackground="#565656")
        left_column.grid(row=1, column=0, padx=(10, 5), pady=(0, 10), sticky="nsew")

        # Ajoutez des poids pour partager la hauteur
        left_column.grid_rowconfigure(0, weight=1)

        # Créez une Frame pour les labels et les entrées
        input_frame = tk.Frame(left_column, bg="#1C1C1C")
        input_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Configurez le padding autour du texte dans le widget Text
        padding = 10
        input_frame.configure(padx=padding)

        # Créer une sous-frame pour compression_label, ram_qty_label, et le reste
        input_logo = tk.Frame(input_frame, bg="#1C1C1C")
        input_logo.grid(row=1, column=0, columnspan=2, padx=(0, 0), pady=(20, 20), sticky="nsew")

        # Chargez l'image dans une variable de classe
        logo_path = self.static_method.resource_path("images/logo.png")
        input_logo_img = tk.PhotoImage(file=logo_path)

        # Créez un label pour afficher l'image
        logo_label = ttk.Label(input_logo, image=input_logo_img, background="#1C1C1C", anchor="center")
        logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), padx=(0, 0), sticky="n")
        # Ajoutez des poids pour partager la hauteur
        logo_label.grid_rowconfigure(0, weight=1)

        # Assurez-vous que l'image ne soit pas collectée par le garbage collector
        logo_label.photo = input_logo_img

        # Créer une sous-frame pour check_plot
        input_subframe_1 = tk.Frame(input_logo, bg="#1C1C1C")
        input_subframe_1.grid(row=1, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="n")

        # Ajouter des poids pour partager la largeur
        input_subframe_1.columnconfigure(0, weight=1)
        input_subframe_1.columnconfigure(1, weight=1)

        # Ligne 3 : check_plot
        self.check_plot_value_label = ttk.Label(input_subframe_1, style="Custom.TLabel", text="Nombre de contrôles", anchor="center")
        self.check_plot_value_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        check_plot_value = self.config_manager.read_config(self.config_manager.config_file).get("check_plot_value")
        self.check_plot_value_var = tk.StringVar(value=check_plot_value)

        self.check_plot_value_combobox = ttk.Combobox(input_subframe_1, textvariable=self.check_plot_value_var)
        self.check_plot_value_combobox.grid(row=1, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_plot_value_combobox['values'] = ["30", "60", "100", "300", "500", "700", "1000"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_plot_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_check_plot_value_config())

        # Ligne 4 : check_threshold
        self.check_threshold_value_label = ttk.Label(input_subframe_1, style="Custom.TLabel", text="Taux de preuve en %", anchor="center")
        self.check_threshold_value_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        check_threshold_value = self.config_manager.read_config(self.config_manager.config_file).get("check_threshold_value")
        self.check_threshold_value_var = tk.StringVar(value=check_threshold_value)
        self.check_threshold_value_combobox = ttk.Combobox(input_subframe_1, textvariable=self.check_threshold_value_var)
        self.check_threshold_value_combobox.grid(row=1, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_threshold_value_combobox['values'] = ["80", "85", "90", "95", "100"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_threshold_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_check_threshold_config())

        # Configurez le combobox de check en fonction de la valeur de check_plot_status
        if self.plotter_gui.check_plot_status == "on":
            # Activer la Combobox
            self.check_plot_value_combobox.configure(state="normal")
            self.check_threshold_value_combobox.configure(state="normal")
        else:
            # Désactiver la Combobox
            self.check_plot_value_combobox.configure(state="disabled")
            self.check_threshold_value_combobox.configure(state="disabled")

        # Créer une sous-frame pour compression_label, ram_qty_label, et le reste
        input_subframe_2: Frame = tk.Frame(input_subframe_1, bg="#1C1C1C")
        input_subframe_2.grid(row=2, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="n")

        # Ajouter des poids pour partager la largeur
        input_subframe_2.columnconfigure(0, weight=1)
        input_subframe_2.columnconfigure(1, weight=1)

        # Ligne 1 : Taux de compression du plot
        self.compression_label = ttk.Label(input_subframe_2, style="Custom.TLabel", text="Taux de compression", anchor="center")
        self.compression_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Récupérez les valeurs de compression à partir de InitializeVariables.plotSizes
        compression_values = [str(compression) for compression in InitializeVariables().plotSizes.keys()]
        compression = self.config_manager.read_config(self.config_manager.config_file).get("compression")
        self.compression_var = tk.StringVar(value=compression)
        self.compression_combobox = ttk.Combobox(input_subframe_2, textvariable=self.compression_var)
        self.compression_combobox.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.compression_combobox['values'] = compression_values
        # Associez la fonction à l'événement de changement de la combobox
        self.compression_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_compression_config())

        # Ligne 2 : Quantité de RAM
        self.ram_qty_label = ttk.Label(input_subframe_2, style="Custom.TLabel", text="Quantité de RAM", anchor="center")
        self.ram_qty_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        ram_qty_var = self.config_manager.read_config(self.config_manager.config_file).get("ram_qty")
        self.ram_qty_var = tk.StringVar(value=ram_qty_var)

        self.ram_qty_combobox = ttk.Combobox(input_subframe_2, textvariable=self.ram_qty_var, values=["16", "32", "64", "128", "256", "512"])
        self.ram_qty_combobox.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")

        # Associez la fonction à l'événement de changement de la combobox
        self.ram_qty_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_ram_config())

        # Créer une sous-frame pour compression_label, ram_qty_label
        input_subframe_3 = tk.Frame(input_subframe_2, bg="#1C1C1C")
        input_subframe_3.grid(row=3, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_3.columnconfigure(0, weight=1)
        input_subframe_3.columnconfigure(1, weight=1)

        # Ligne 3 : Pool contract
        self.contract_label = ttk.Label(input_subframe_3, style="Custom.TLabel", text="Pool contract", anchor="center")
        self.contract_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle du contrat de pool
        current_contract_key = self.config_manager.read_config(self.config_manager.config_file).get("contract")
        self.contract_var = tk.StringVar(value=current_contract_key)
        self.contract_entry = ttk.Entry(input_subframe_3, textvariable=self.contract_var)
        self.contract_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.contract_entry.bind("<FocusOut>", lambda event=None: self.update_contract_config())

        # Ligne 4 : Farmer public key
        self.farmer_key_label = ttk.Label(input_subframe_3, style="Custom.TLabel", text="Farmer public key", anchor="center")
        self.farmer_key_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle de la clé du fermier
        current_farmer_key = self.config_manager.read_config(self.config_manager.config_file).get("farmer_key")
        self.farmer_key_var = tk.StringVar(value=current_farmer_key)
        self.farmer_key_entry = ttk.Entry(input_subframe_3, textvariable=self.farmer_key_var)
        self.farmer_key_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew", columnspan=2)

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.farmer_key_entry.bind("<FocusOut>", lambda event=None: self.update_farmer_key_config())

        # Créer une sous-frame pour ssd_temp et ssd_temp2move
        input_subframe_4 = tk.Frame(input_subframe_3, bg="#1C1C1C")
        input_subframe_4.grid(row=4, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_4.columnconfigure(0, weight=1)
        input_subframe_4.columnconfigure(1, weight=1)

        # Ligne 6 : Disque temporaire -t1 (nvme/ssd)
        self.ssd_temp_label = ttk.Label(input_subframe_4, style="Custom.TLabel", text="Disque temporaire -t1", anchor="center")
        self.ssd_temp_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        self.ssd_temp_entry = ttk.Entry(input_subframe_4)
        self.ssd_temp_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp")
        if ssd_temp_value is None or ssd_temp_value == "":
            ssd_temp_value = self.config_manager.defaults["ssd_temp"]

        self.ssd_temp_entry.insert(0, ssd_temp_value)

        self.ssd_temp_button = ttk.Button(input_subframe_4, text="Parcourir", command=self.plotter_gui.browse_ssd_temp)
        self.ssd_temp_button.grid(row=2, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp_button.config(cursor="hand2")

        # Ligne 7 : Disque temporaire 2 -t2 (nvme/ssd/hdd - Non obligatoire)
        self.ssd_temp2move_label = ttk.Label(input_subframe_4, style="Custom.TLabel", text="Disque temporaire -t2", anchor="center")
        self.ssd_temp2move_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        self.ssd_temp2move_entry = ttk.Entry(input_subframe_4)
        self.ssd_temp2move_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp2move_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move")
        if not ssd_temp2move_value:
            ssd_temp2move_value = self.config_manager.defaults["ssd_temp2move"]

        self.ssd_temp2move_entry.insert(0, ssd_temp2move_value)

        self.ssd_temp2move_button = ttk.Button(input_subframe_4, text="Parcourir", command=self.plotter_gui.browse_ssd_temp2move)
        self.ssd_temp2move_button.grid(row=2, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp2move_button.config(cursor="hand2")

        # Créer une sous-frame pour plotter_path
        input_subframe_5 = tk.Frame(input_subframe_4, bg="#1C1C1C")
        input_subframe_5.grid(row=5, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_5.columnconfigure(0, weight=1)
        input_subframe_5.columnconfigure(1, weight=1)

        # Ligne 5 : Chemin vers l'exécutable de plotter
        self.plotter_path_label = ttk.Label(input_subframe_5, style="Custom.TLabel", text="Sélectionner le plotter", anchor="center")
        self.plotter_path_label.grid(row=0, column=0, pady=(0, 5), padx=4, sticky="nsew", columnspan=2)

        # Créer une liste déroulante avec les exécutables disponibles
        self.plotter_path_combobox = ttk.Combobox(input_subframe_5, values=available_executables)
        self.plotter_path_combobox.grid(row=1, column=0, pady=(0, 0), padx=4, sticky="nsew", columnspan=2)
        self.plotter_path_combobox.bind("<<ComboboxSelected>>", self.plotter_gui.on_combobox_selected)

        # Défini la valeur initiale de la liste déroulante
        existing_plotter = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")
        self.plotter_path_combobox.set(existing_plotter)

        # Créer une sous-frame pour hdd_dir
        input_subframe_6 = tk.Frame(input_subframe_5, bg="#1C1C1C")
        input_subframe_6.grid(row=6, column=0, columnspan=2, padx=0, pady=(20, 30), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_6.columnconfigure(0, weight=1)
        input_subframe_6.columnconfigure(1, weight=1)

        # Ligne 8 : Dossier de destination -d
        self.hdd_dir_label = ttk.Label(input_subframe_6, style="Custom.TLabel", text="Dossier de destination -d", anchor="center")
        self.hdd_dir_label.grid(row=0, column=0, pady=(0, 5), padx=5, sticky="nsew", columnspan=2)

        self.hdd_dir_listbox = tk.Listbox(input_subframe_6, selectmode=tk.MULTIPLE, height=4)
        self.hdd_dir_listbox.grid(row=1, column=0, pady=(0, 0), padx=5, sticky="nsew", columnspan=2)

        hdd_dir_value = self.config_manager.read_config(self.config_manager.config_file).get("hdd_dir", "")
        hdd_dirs = hdd_dir_value.split(",")
        for directory in hdd_dirs:
            self.hdd_dir_listbox.insert(tk.END, directory)

        # Utiliser une Frame pour les boutons Ajouter et Supprimer
        button_frame = tk.Frame(input_subframe_6, bg="#1C1C1C")
        button_frame.grid(row=2, column=0, columnspan=2, pady=0, padx=5, sticky="nsew")

        # Ajouter des poids pour partager la largeur entre les boutons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.add_hdd_dir_button = ttk.Button(button_frame, text="Ajouter", command=self.plotter_gui.add_hdd_dir)
        self.add_hdd_dir_button.grid(row=0, column=0, pady=0, padx=(0, 2), sticky="nsew")
        self.add_hdd_dir_button.config(cursor="hand2")

        self.remove_hdd_dir_button = ttk.Button(button_frame, text="Supprimer", command=self.plotter_gui.remove_hdd_dir)
        self.remove_hdd_dir_button.grid(row=0, column=1, pady=0, padx=(2, 0), sticky="nsew")
        self.remove_hdd_dir_button.config(cursor="hand2")

        # Créer une Frame pour les boutons sous la configuration
        button_frame = tk.Frame(left_column, bg="#1C1C1C")
        button_frame.grid(row=12, column=0, columnspan=2, padx=0, pady=(2, 0), sticky="nsew")

        # Configurez le padding autour du texte dans le widget Text
        padding = 10
        button_frame.configure(padx=padding)

        # Centrer horizontalement les boutons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Ligne 9 : Bouton Démarrer
        self.start_button = ttk.Button(button_frame, text="Lancer la création", command=self.plotter_gui.start_plotting, cursor="hand2")
        self.start_button.grid(row=0, column=0, pady=15, padx=5, sticky="nsew")

        # Ligne 10 : Bouton Arrêter
        self.stop_button = ttk.Button(button_frame, text="Fermer la fenêtre", command=self.plotter_gui.stop_or_close, cursor="hand2")
        self.stop_button.grid(row=0, column=1, pady=15, padx=5, sticky="nsew")

        # Créer la deuxième colonne avec 12 lignes et 1 colonne
        right_column = tk.Frame(main_frame, bg="#565656", highlightthickness=1, highlightbackground="#565656")
        right_column.grid(row=1, column=1, padx=(5, 10), pady=(0, 10), sticky="nsew")

        # Ajoutez des poids pour partager la hauteur
        right_column.grid_rowconfigure(0, weight=0)
        right_column.grid_rowconfigure(1, weight=1)

        # Ajoutez des poids pour partager la largeur
        right_column.grid_columnconfigure(0, weight=1)

        # Créer une Frame pour les journaux
        log_frame = tk.Frame(right_column, bg="#1C1C1C")
        log_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")

        # Ajoutez des poids pour partager la largeur
        log_frame.grid_columnconfigure(0, weight=1)

        # Ajoutez des poids pour partager la hauteur
        log_frame.grid_rowconfigure(0, weight=0)
        log_frame.grid_rowconfigure(1, weight=0)
        log_frame.grid_rowconfigure(2, weight=0)
        log_frame.grid_rowconfigure(3, weight=0)
        log_frame.grid_rowconfigure(4, weight=0)
        log_frame.grid_rowconfigure(5, weight=0)
        log_frame.grid_rowconfigure(6, weight=1)

        # Ligne 11 : Journal des Erreurs
        error_label = ttk.Label(log_frame, style="Custom.TLabel", text="Journal des erreurs:", anchor="nw")
        error_label.grid(row=1, column=0, pady=(10, 1), padx=15, sticky="nw")
        error_label.configure(background="#1C1C1C", foreground="#FF2E2E")

        self.errors_text = tk.Text(log_frame, wrap=tk.WORD, height=5, highlightthickness=1, highlightbackground="#565656")
        self.errors_text.grid(row=2, column=0, pady=(0, 5), padx=(15, 0), sticky="nsew")
        self.errors_text.configure(bg="#2C2C2C", fg="#FF2E2E")

        errors_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.errors_text.yview)
        errors_scrollbar.grid(row=2, column=1, pady=(0, 5), padx=(0, 15), sticky="ns")
        self.errors_text["yscrollcommand"] = errors_scrollbar.set
        self.errors_text.tag_configure("timestamp", foreground="#CCCCCC")
        self.errors_text.tag_configure("error", foreground="#FF2E2E")
        self.errors_text.tag_configure("warning", foreground="#FF8300")
        self.errors_text.tag_configure("info", foreground="#0093FF")

        # Ligne 12 : Journal de l'application
        log_label = ttk.Label(log_frame, style="Custom.TLabel", text="Journal de l'application:", anchor="nw")
        log_label.grid(row=3, column=0, pady=(10, 1), padx=15, sticky="nw")
        log_label.configure(background="#1C1C1C", foreground="#00B34D")

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10, highlightthickness=1, highlightbackground="#565656")
        self.log_text.grid(row=4, column=0, pady=(0, 5), padx=(15, 0), sticky="nsew")
        self.log_text.configure(bg="#2C2C2C", fg="#00B34D")
        self.log_text.tag_configure("timestamp", foreground="#CCCCCC")
        self.log_text.tag_configure("error", foreground="#FF2E2E")
        self.log_text.tag_configure("warning", foreground="#FF8300")
        self.log_text.tag_configure("info", foreground="#0093FF")

        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=4, column=1, pady=(0, 5), padx=(0, 15), sticky="ns")
        self.log_text["yscrollcommand"] = log_scrollbar.set

        # Ligne 13 : Journal de plotter
        log_blade_label = ttk.Label(log_frame, style="Custom.TLabel", text="Journal de plotter:", anchor="nw")
        log_blade_label.grid(row=5, column=0, pady=(10, 1), padx=15, sticky="nw")
        log_blade_label.configure(background="#1C1C1C", foreground="#BFBFBF")

        self.log_blade = tk.Text(log_frame, wrap=tk.WORD, height=10, highlightthickness=1, highlightbackground="#565656")
        self.log_blade.grid(row=6, column=0, pady=(0, 15), padx=(15, 0), sticky="nsew")
        self.log_blade.configure(bg="#2C2C2C", fg="#BFBFBF")
        self.log_blade.tag_configure("timestamp", foreground="#BFBFBF")
        self.log_blade.tag_configure("error", foreground="#FF2E2E")
        self.log_blade.tag_configure("warning", foreground="#FF8300")
        self.log_blade.tag_configure("info", foreground="#0093FF")

        log_blade_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_blade.yview)
        log_blade_scrollbar.grid(row=6, column=1, pady=(0, 15), padx=(0, 15), sticky="ns")
        self.log_blade["yscrollcommand"] = log_blade_scrollbar.set

        # Configurez le padding autour du texte dans le widget Text
        padding = 10
        self.errors_text.configure(padx=padding, pady=padding)
        self.log_text.configure(padx=padding, pady=padding)
        self.log_blade.configure(padx=padding, pady=padding)

        # Attachement de la méthode self.close_window à l'événement de fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.plotter_gui.stop_or_close)

        # Ajoutez des poids pour partager la largeur
        self.root.grid_columnconfigure(0, weight=1)

        # Ajoutez des poids pour partager la hauteur
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

        # Récupérer les dimensions de l'écran
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculer la largeur souhaitée pour la fenêtre (3/4 de la largeur de l'écran)
        desired_width = screen_width * 3 // 4
        # Calculer la hauteur souhaitée pour la fenêtre (par exemple, 3/4 de la hauteur de l'écran)
        desired_height = screen_height * 3 // 4 - 30

        # Définir la hauteur de la fenêtre à la hauteur souhaitée
        self.root.geometry(f"{desired_width}x{desired_height}+{screen_width // 8}+{screen_height // 8}")

        # Actualise l'interface
        self.root.update()

    def update_contract_config(self):
        selected_contract = self.contract_var.get()
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"contract": selected_contract}, self.config_manager.config_file)

    def update_farmer_key_config(self):
        selected_farmer_key = self.farmer_key_var.get()
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"farmer_key": selected_farmer_key}, self.config_manager.config_file)

    def update_compression_config(self):
        selected_compression = self.compression_var.get()
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"compression": selected_compression}, self.config_manager.config_file)

    def update_ram_config(self):
        selected_ram_qty = self.ram_qty_var.get()
        self.config_manager.update_config({"ram_qty": selected_ram_qty}, self.config_manager.config_file)

    def update_check_plot_value_config(self):
        selected_check_plot_value = self.check_plot_value_var.get()
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"check_plot_value": selected_check_plot_value}, self.config_manager.config_file)

    def update_check_threshold_config(self):
        selected_check_threshold_value = self.check_threshold_value_var.get()
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"check_threshold_value": selected_check_threshold_value}, self.config_manager.config_file)

    # Define our switch function
    def logs_button_switch(self):
        # Determine si l'état est "on" ou "off"
        if self.plotter_gui.logs_status == "on":
            # Désactiver tous les niveaux de journalisation
            self.plotter_gui.logger.setLevel(logging.CRITICAL + 1)

            self.logging_button.config(image=self.logging_button_off)
            self.logging_label.config(foreground="red")
            self.plotter_gui.logs_status = "off"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": "off"}, self.config_manager.config_file)
        else:
            # Activer la journalisation à un niveau spécifique (par exemple, INFO)
            self.plotter_gui.logger.setLevel(logging.INFO)

            self.logging_button.config(image=self.logging_button_on)
            self.logging_label.config(foreground="green")
            self.plotter_gui.logs_status = "on"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": "on"}, self.config_manager.config_file)

    # Define our switch function
    def check_button_switch(self):
        # Determine si l'état est "on" ou "off"
        if self.plotter_gui.check_plot_status == "on":
            self.check_button.config(image=self.logging_button_off)
            self.check_label.config(foreground="red")
            self.plotter_gui.check_plot_status = "off"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": "off"}, self.config_manager.config_file)
            # Désactiver la Combobox
            self.check_plot_value_combobox.configure(state="disabled")
            self.check_threshold_value_combobox.configure(state="disabled")
        else:
            self.check_button.config(image=self.logging_button_on)
            self.check_label.config(foreground="green")
            self.plotter_gui.check_plot_status = "on"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": "on"}, self.config_manager.config_file)
            # Activer la Combobox
            self.check_plot_value_combobox.configure(state="normal")
            self.check_threshold_value_combobox.configure(state="normal")


class StaticMethod:
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    @staticmethod
    def configure_logging(filename):
        # Nom du fichier de log
        log_filename = f"{filename}.log"
        logging.basicConfig(filename=log_filename, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    @staticmethod
    def is_plotter_valid(plotter_path):
        # Vérifie si l'emplacement de l'exécutable plotter est valide
        return os.path.isfile(plotter_path)

    @staticmethod
    def is_ssd_temp_valid(ssd_temp):
        # Vérifie si l'emplacement du disque temporaire -t1 est valide
        return os.path.exists(ssd_temp)

    @staticmethod
    def is_hdd_dir_valid(hdd_dir):
        # Vérifie si l'emplacement du dossier de destination -d est valide
        if hdd_dir is not None:
            return os.path.exists(hdd_dir)
        else:
            return False


class FindMethod:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.config_manager = ff_plotter_gui.config_manager
        self.queue_logs = ff_plotter_gui.queue_logs

    def find_pid_by_name(self, process_name):
        for processus in psutil.process_iter(attrs=['pid', 'name']):
            try:
                process_info = processus.as_dict(attrs=['pid', 'name'])
                if process_info['name'] == process_name:
                    return process_info['pid']
            except Exception as e:
                self.queue_logs.log_queue_errors.put(f"Récupération de l'identifiant du processus {process_name}: {str(e)}")

        # Si le processus n'a pas été trouvé, retourne None
        return None

    def find_plotter_executable(self):
        # Récupère le nom du plotter utilisé
        plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")

        # Récupère le chemin du plotter stocké dans le fichier de configuration
        plotter_path = self.config_manager.read_config(self.config_manager.config_file).get("plotter_path")

        # Construit le chemin complet de l'exécutable et normalise le chemin du fichier
        plotter_path_join = os.path.normpath(os.path.join(plotter_path, plotter_executable))

        # Utilise shutil pour rechercher l'exécutable dans le PATH
        system = platform.system()
        if system == "Windows":
            executable_name = f"{plotter_executable}.exe"
        else:
            executable_name = plotter_executable

        # Initialise la variable
        found_path = shutil.which(executable_name)

        # Si le chemin est trouvé, on vérifie s'il est exécutable
        if found_path and os.access(found_path, os.X_OK):
            return found_path
        else:
            return plotter_path_join


class FFPlotterGUI:
    def __init__(self):
        # Création des instances
        self.config_manager = ConfigManager()

        # Récupère les valeurs depuis le fichier de configuration
        self.config_progress_status = self.config_manager.read_config(self.config_manager.config_file).get("progress_status")
        self.check_plot_status = self.config_manager.read_config(self.config_manager.config_file).get("check_plot_status")
        self.logs_status = self.config_manager.read_config(self.config_manager.config_file).get("logs_status")
        self.queue_logs = LogQueue()
        self.initialize_variables = InitializeVariables()
        self.none_false_variable = NoneFalseVariables()
        self.pattern = Pattern()
        self.static_method = StaticMethod()
        self.find_method = FindMethod(self)
        self.interface = Interface(self)
        self.lists = Lists(self)
        self.logger = logging.getLogger(__name__)
        self.progress_bar = ProgressBar(self)
        self.log_manager = LogManager(self)
        self.welcome = Welcome(self)
        self.welcome.show_message()

        # Recherche automatique et mise à jour du fichier de configuration uniquement si la valeur est vide
        if not self.config_manager.read_config(self.config_manager.config_file).get("plotter_path"):
            plotter_path = self.find_method.find_plotter_executable()
            if plotter_path:
                # Normalise le chemin du fichier
                normalized_plotter_path = os.path.normpath(plotter_path)
                # Mise à jour du fichier de configuration
                self.config_manager.update_config({"plotter_path": normalized_plotter_path}, self.config_manager.config_file)

        # Mise à jour de l'interface graphique
        self.update_idletasks()

    def on_combobox_selected(self, event):
        # Mise à jour du fichier de configuration uniquement si la valeur est vide
        selected_executable = self.interface.plotter_path_combobox.get()
        if selected_executable:
            self.interface.plotter_path_combobox.delete(0, tk.END)
            self.interface.plotter_path_combobox.insert(0, selected_executable)
            # Mise à jour du fichier de configuration
            self.config_manager.update_config({"plotter_executable": selected_executable}, self.config_manager.config_file)

        # Recherche automatique et mise à jour du fichier de configuration uniquement si la valeur est vide
        if not self.config_manager.read_config(self.config_manager.config_file).get("plotter_path"):
            # Normalise le chemin du répertoire
            normalized_plotter_path = os.path.normpath(self.config_manager.plotter_directory)
            # Mise à jour du fichier de configuration
            self.config_manager.update_config({"plotter_path": normalized_plotter_path}, self.config_manager.config_file)

    # Menu parcourir du disque temporaire 1
    def browse_ssd_temp(self):
        # Ouvre une boîte de dialogue pour sélectionner le disque temporaire -t1 (NVME/SSD)
        ssd_temp = filedialog.askdirectory(title="Sélectionnez le disque temporaire -t1 (NVME/SSD)")
        if ssd_temp:
            # Normalise le chemin
            normalized_ssd_temp = os.path.normpath(ssd_temp)
            # Mise à jour de l'interface graphique
            self.interface.ssd_temp_entry.delete(0, tk.END)
            self.interface.ssd_temp_entry.insert(0, normalized_ssd_temp)
            # Mise à jour du fichier de configuration
            self.config_manager.update_config({"ssd_temp": normalized_ssd_temp}, self.config_manager.config_file)

    # Menu parcourir du disque temporaire 2
    def browse_ssd_temp2move(self):
        # Permettez à l'utilisateur de parcourir et de sélectionner le chemin du disque temporaire 2 -t2
        selected_ssd_temp2move = filedialog.askdirectory(title="Sélectionnez le disque temporaire 2 -t2")

        # Normalise le chemin
        normalized_ssd_temp2move = os.path.normpath(selected_ssd_temp2move)

        # Mise à jour de l'interface graphique
        self.interface.ssd_temp2move_entry.delete(0, tk.END)
        self.interface.ssd_temp2move_entry.insert(0, normalized_ssd_temp2move)

        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"ssd_temp2move": normalized_ssd_temp2move}, self.config_manager.config_file)

    # Ajout de disques de destination
    def add_hdd_dir(self):
        # Ouvre une boîte de dialogue pour ajouter un dossier de destination -d
        hdd_dir = filedialog.askdirectory(title="Sélectionnez un dossier de destination -d")
        if hdd_dir:
            # Lire la configuration actuelle
            current_config = self.config_manager.read_config(self.config_manager.config_file)

            # Récupérer la valeur actuelle de "hdd_dir" ou une chaîne vide si elle n'existe pas
            hdd_dir_str = current_config.get("hdd_dir", "")

            # Supprimer les barres obliques inversées et diviser la chaîne en une liste
            hdd_dir_list = [os.path.normpath(hdd_directory.strip()) for hdd_directory in hdd_dir_str.split(',') if hdd_directory.strip()]

            # Vérifier si le dossier est déjà dans la liste
            if os.path.normpath(hdd_dir) not in hdd_dir_list:
                # Ajouter le nouveau dossier à la liste
                hdd_dir_list.append(os.path.normpath(hdd_dir))

                # Joindre la liste mise à jour en une seule chaîne séparée par des virgules
                updated_hdd_dirs = ",".join(hdd_dir_list)

                # Récupère la nouvelle valeur
                current_config["hdd_dir"] = updated_hdd_dirs

                # Mise à jour du fichier de configuration
                self.config_manager.update_config(current_config)

                # Efface la liste actuelle
                self.interface.hdd_dir_listbox.delete(0, tk.END)

                # Mise à jour de l'interface graphique
                for hdd in hdd_dir_list:
                    self.interface.hdd_dir_listbox.insert(tk.END, hdd)

    # Suppression des disques de destination
    def remove_hdd_dir(self):
        # Supprime le dossier de destination -d sélectionné dans la liste
        selected_indices = self.interface.hdd_dir_listbox.curselection()
        hdd_dirs = self.config_manager.read_config(self.config_manager.config_file).get("hdd_dir", "").split(",")

        for index in reversed(selected_indices):
            if 0 <= index < len(hdd_dirs):
                del hdd_dirs[index]

        # Joindre la liste mise à jour en une seule chaîne séparée par des virgules
        updated_hdd_dirs_str = ",".join(hdd_dirs)

        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"hdd_dir": updated_hdd_dirs_str}, self.config_manager.config_file)

        # Efface la liste actuelle
        for index in reversed(selected_indices):
            self.interface.hdd_dir_listbox.delete(index)

    def validate_input_fields(self):
        # Valide les champs obligatoires de l'interface utilisateur
        if (
                self.interface.check_plot_value_var.get() == "" or
                self.interface.check_threshold_value_var.get() == "" or
                self.interface.compression_var.get() == "" or
                self.interface.ram_qty_var.get() == "" or
                self.interface.plotter_path_combobox.get() == "" or
                self.interface.ssd_temp_entry.get() == "" or
                self.interface.contract_entry.get() == "" or
                self.interface.farmer_key_entry.get() == "" or
                self.interface.hdd_dir_listbox.size() == 0
        ):
            return False
        return True

    def get_disk_size(self, path):
        # Récupère la taille du disque sélectionné
        try:
            disk = psutil.disk_usage(path)
            total = disk.total
            used = disk.used
            free = disk.free
            return total, used, free
        except Exception as e:
            self.queue_logs.log_queue_errors.put(f"Erreur lors de la récupération de la taille du disque: {e}")
            return 0, 0, 0

    def calculate_max_plots_on_disk(self, hdd, compression):
        # Calcul le nombre de plots sur le disque sélectionné
        total, used, free = self.get_disk_size(hdd)
        free_space_on_hdd = free
        return free_space_on_hdd // self.initialize_variables.plotSizes[int(compression)]

    def delete_plots(self, directory):
        # Méthode de suppression des anciens plots
        # Obtenez la liste des fichiers de plots dans le répertoire
        files = os.listdir(directory)

        # Filtrer les fichiers qui sont des plots et correspondent au modèle
        plots_to_delete = [file for file in files if file.endswith(".plot") and self.pattern.plotFormatPattern.match(file)]

        # Triez les plots par date de création (les plus anciens d'abord)
        plots_to_delete.sort(key=lambda x: os.path.getctime(os.path.join(directory, x)))

        return plots_to_delete

    def find_hdd_with_space(self, hdd_dirs, compression):
        # Recherche d'un disque ayant de l'espace disponible
        # Liste des disques de destination avec de l'espace
        hdd_dirs_with_space = [hdd for hdd in hdd_dirs if self.calculate_max_plots_on_disk(hdd, compression) > 0]

        # Si au moins un disque a suffisamment d'espace, sortir de la boucle récursive
        if hdd_dirs_with_space:
            return hdd_dirs_with_space[0]
        else:
            # Redirection vers log_queue_messages
            self.queue_logs.log_queue_messages.put((f"L'espace est plein, recherche d'un ancien plot à supprimer...", "warning"))
            time.sleep(0.8)

        # Si aucun disque n'a suffisamment d'espace, chercher un disque avec des anciens plots et supprimer un par un
        for hdd in hdd_dirs:
            # Vérifier si le disque contient des anciens plots
            if self.none_false_variable.delOldPlots is True:
                plots_to_delete = self.delete_plots(hdd)

                if plots_to_delete:
                    # Supprimer un ancien plot
                    plot_to_delete = plots_to_delete[0]
                    plot_path = os.path.join(hdd, plot_to_delete)

                    try:
                        # Redirection vers log_queue_messages
                        self.queue_logs.log_queue_messages.put((f"Ancien plot trouvé: {plot_path}", "warning"))
                        time.sleep(0.8)

                        # Redirection vers log_queue_messages
                        self.queue_logs.log_queue_messages.put((f"Suppression en cours...", "warning"))
                        time.sleep(0.8)

                        # Supprimer le plot
                        # os.remove(plot_path)
                        os.unlink(plot_path)

                        # Redirection vers log_queue_messages
                        self.queue_logs.log_queue_messages.put((f"Ancien plot supprimé avec succès", "warning"))
                        time.sleep(0.8)

                        # Récupère la valeur actuelle dans le fichier de configuration
                        current_deleted_plot_number = self.config_manager.read_config(self.config_manager.config_stats).get("deleted_plot_number")
                        # Incrémente la variable de plots supprimés
                        new_deleted_plot_number = int(current_deleted_plot_number)
                        new_deleted_plot_number = new_deleted_plot_number + 1
                        # Mise à jour de l'interface graphique
                        self.interface.deleted_plot_number_label.config(text=f"{new_deleted_plot_number}")
                        # Mise à jour du fichier de configuration
                        self.config_manager.update_config({"deleted_plot_number": new_deleted_plot_number}, self.config_manager.config_stats)

                        # Mettre à jour la liste des disques avec de l'espace
                        return self.find_hdd_with_space(hdd_dirs, compression)

                    except Exception as e:
                        # Redirection vers log_queue_messages en cas d'erreur
                        self.queue_logs.log_queue_errors.put(f"Erreur lors de la suppression du plot {plot_path}: {e}")

        # Si aucun disque n'a suffisamment d'espace, retourner None
        return None

    def start_plotting(self, show_dialog=True):
        # Si le processus plotter est en cours et show_dialog est True, demandez à l'utilisateur s'il souhaite le lancer
        if show_dialog and tkinter.messagebox.askokcancel("Lancement", "Voulez-vous lancer la création de plot ?"):
            show_dialog = False

        if show_dialog is False:
            # Si plotter_pid est trouvé et la variable de plots en cours de création est True
            if self.none_false_variable.plot_creation_in_progress is True:
                # On stoppe le script
                self.queue_logs.log_queue_errors.put("La création de plot est déjà en cours.")
                return

            # Vérifie si tous les champs obligatoires sont remplis
            if not self.validate_input_fields():
                self.queue_logs.log_queue_errors.put("Veuillez remplir tous les champs obligatoires.")
                return

            # Récupère les valeurs des champs depuis le fichier de configuration
            compression = self.config_manager.read_config(self.config_manager.config_file).get("compression", self.config_manager.defaults["compression"])
            plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable", self.config_manager.defaults["plotter_executable"])
            plotter_path = self.config_manager.read_config(self.config_manager.config_file).get("plotter_path", self.config_manager.defaults["plotter_path"])
            ssd_temp = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp", self.config_manager.defaults["ssd_temp"])
            ssd_temp2move = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move", self.config_manager.defaults["ssd_temp2move"])
            hdd_dirs = self.config_manager.read_config(self.config_manager.config_file).get("hdd_dir", "").split(",")

            # Construit le chemin complet du plotter
            plotter_path_join = os.path.join(plotter_path, plotter_executable)

            # Vérifie si l'emplacement de l'exécutable plotter est valide
            if not self.static_method.is_plotter_valid(plotter_path_join):
                self.queue_logs.log_queue_errors.put(f"L'emplacement de l'exécutable plotter n'est pas valide: {plotter_path_join}")
                return

            # Vérifie si l'emplacement du disque temporaire -t1 est valide
            if not self.static_method.is_ssd_temp_valid(ssd_temp):
                self.queue_logs.log_queue_errors.put(f"L'emplacement du disque temporaire -t1 n'est pas valide: {ssd_temp}")
                return

            # Vérifie si l'emplacement du disque temporaire 2 -t2 (s'il est spécifié) est valide
            if ssd_temp2move and not self.static_method.is_ssd_temp_valid(ssd_temp2move):
                self.queue_logs.log_queue_errors.put(f"L'emplacement du disque temporaire 2 -t2 n'est pas valide: {ssd_temp2move}")
                return

            # Message dans la file d'attente
            self.queue_logs.log_queue_messages.put(("Initialisation...", None))
            time.sleep(0.8)

            # Cherchez un disque avec suffisamment d'espace ou supprimez des anciens plots au besoin
            selected_hdd = self.find_hdd_with_space(hdd_dirs, compression)

            # Vérifie si le disque de destination est toujours disponible
            if not self.static_method.is_hdd_dir_valid(selected_hdd):
                self.queue_logs.log_queue_errors.put(f"Le disque de destination n'est plus disponible: {selected_hdd}")
                return

            # Créez et démarrez le thread de surveillance
            monitor_thread = threading.Thread(target=self.update_button_text)
            monitor_thread.daemon = True
            monitor_thread.start()

            # Calcul de la quantité de plots pouvant être créés sur le disque sélectionné
            self.initialize_variables.max_plots_on_selected_hdd = self.calculate_max_plots_on_disk(selected_hdd, compression)

            # Création d'un thread pour exécuter la boucle plots_progress
            if self.config_progress_status == "on":
                progress_thread = threading.Thread(target=self.progress_bar.plots_progress)
                progress_thread.daemon = True
                progress_thread.start()

            # Créez un thread séparé pour la création de plots avec les paramètres sélectionnés
            plotter_thread = threading.Thread(target=self.start_plotter_process, args=(selected_hdd,))
            plotter_thread.daemon = True
            plotter_thread.start()

    def build_bladebit_cuda_command(self, selected_hdd):
        # Construit le chemin complet du plotter
        plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable", self.config_manager.defaults["plotter_executable"])
        plotter_path = self.config_manager.read_config(self.config_manager.config_file).get("plotter_path", self.config_manager.defaults["plotter_path"])
        plotter_path_join = os.path.join(plotter_path, plotter_executable)
        ssd_temp = os.path.join(self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp"), "")

        # Calculez le nombre de cœurs à utiliser pour atteindre environ 80% d'utilisation
        cores_to_use = psutil.cpu_count(logical=False) - 1  # Utilisez tous les cœurs sauf le dernier

        # Construire la commande de création de plot pour bladebit_cuda
        command = [
            plotter_path_join,
            "-t", str(cores_to_use),
            "-c", self.config_manager.read_config(self.config_manager.config_file).get("contract"),
            "-f", self.config_manager.read_config(self.config_manager.config_file).get("farmer_key"),
            "-n", str(self.initialize_variables.max_plots_on_selected_hdd),
            "-z", self.config_manager.read_config(self.config_manager.config_file).get("compression"),
            "cudaplot",
        ]

        # Ajoute --check et --check-threshold si la vérification des plots est activée à la commande de création de plot
        if self.check_plot_status == "on":
            # Récupère les valeurs pour le check plot
            check_plot_value = str(int(self.config_manager.read_config(self.config_manager.config_file).get("check_plot_value")))
            check_threshold_value = str(int(self.config_manager.read_config(self.config_manager.config_file).get("check_threshold_value")) / 100)
            # Ajoute le plot check à la commande de création de plot
            command.extend(["--check", check_plot_value])
            command.extend(["--check-threshold", check_threshold_value])

        # Ajoute les arguments liés au disque temporaire et la quantité de mémoire utilisée à la commande de création de plot
        command.extend([
            "--disk-" + str(self.config_manager.read_config(self.config_manager.config_file).get("ram_qty")),
            "-t1", ssd_temp,
        ])

        # Ajoute le chemin du disque temporaire 2 si sélectionné à la commande de création de plot
        ssd_temp2 = os.path.join(self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move"), "")
        if ssd_temp2 != "":
            command.extend(["-t2", ssd_temp2])

        # Ajoute le chemin du disque de destination à la commande de création de plot
        command.append(selected_hdd)

        return command

    def build_gigahorse_command(self, selected_hdd):
        # Récupère le type de système
        system = platform.system()

        # Récupère les variables depuis le fichier de configuration
        plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")
        plotter_path = self.config_manager.read_config(self.config_manager.config_file).get("plotter_path")
        ssd_temp = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp")
        ssd_temp2 = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move")
        ram_qty_gb = float(self.config_manager.read_config(self.config_manager.config_file).get("ram_qty"))

        # Construit le chemin complet de l'exécutable
        plotter_path_join = os.path.join(plotter_path, plotter_executable)

        # Si le système est windows
        if system == "Windows":
            # Ajouter un trailing slash s'il n'y en a pas déjà un
            if not ssd_temp.endswith(os.path.sep):
                ssd_temp += os.path.sep

            # Ajouter un trailing slash s'il n'y en a pas déjà un
            if not ssd_temp2.endswith(os.path.sep):
                ssd_temp2 += os.path.sep

            # Ajouter un trailing slash s'il n'y en a pas déjà un
            if not selected_hdd.endswith(os.path.sep):
                selected_hdd += os.path.sep

            # Convertir de Go en GiB
            ram_qty_gib = ram_qty_gb * 0.93132
            # Diviser par 2 pour windows
            ram_qty_gib_divided = math.floor(ram_qty_gib / 2)
            # Défini la variable pour la ram
            ramQty = ram_qty_gib_divided

        # Sinon si le système est linux
        else:
            # Défini la variable pour la ram
            ramQty = ram_qty_gb

        # Construire la commande de création de plot pour gigaHorse
        command = [
            plotter_path_join,
            "-c", self.config_manager.read_config(self.config_manager.config_file).get("contract"),
            "-f", self.config_manager.read_config(self.config_manager.config_file).get("farmer_key"),
            "-n", str(self.initialize_variables.max_plots_on_selected_hdd),
            "-C", self.config_manager.read_config(self.config_manager.config_file).get("compression"),
        ]

        # Ajoute les arguments liés au disque temporaire
        command.extend([
            "-t", ssd_temp,
        ])

        # Ajoute les arguments liés à la ram
        command.extend([
            "-M", str(ramQty),
        ])

        # Ajoute les arguments liés au disque temporaire 2
        if ssd_temp2 != "":
            # ajoute le champ à la commande
            command.extend([
                "-2", ssd_temp2
            ])

        # Ajoute les arguments liés au disque de destination
        command.extend([
            "-d", selected_hdd
        ])

        return command

    def start_plotter_process(self, selected_hdd):
        # Si plotter_pid n'est pas trouvé et la variable de plots en cours de création est False
        if self.none_false_variable.plot_creation_in_progress is False:
            try:
                plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable", self.config_manager.defaults["plotter_executable"])

                # Vérifie si un disque est sélectionné
                if not selected_hdd:
                    # Tous les disques ont été utilisés, arrêtez la création de plots
                    self.queue_logs.log_queue_errors.put("Aucun disques de destinations n'a suffisamment d'espace pour créer un plot.")
                    time.sleep(0.8)
                    # Réinitialisation de la variable de plots en cours de création
                    self.none_false_variable.plot_creation_in_progress = False
                    return

                # Vérification de l'espace disponible
                total, used, free = self.get_disk_size(selected_hdd)
                free_space_on_hdd = free

                # Convertir en Mo, To, Go
                available_space_mb = free_space_on_hdd / (1024 ** 2)
                available_space_gb = free_space_on_hdd / (1024 ** 3)
                available_space_tb = free_space_on_hdd / (1024 ** 4)

                # Message dans la file d'attente
                self.queue_logs.log_queue_messages.put((f"Espace disponible: {available_space_mb:.2f} Mo | {available_space_gb:.2f} Go | {available_space_tb:.2f} To", None))
                time.sleep(0.8)

                # Message dans la file d'attente
                self.queue_logs.log_queue_messages.put((f"{self.initialize_variables.max_plots_on_selected_hdd} plots à créer dans {selected_hdd}", None))
                self.interface.current_plot_max_text.config(text=f"{self.initialize_variables.max_plots_on_selected_hdd}")
                time.sleep(0.8)

                # Appel de la commande en fonction du plotter
                if plotter_executable == "bladebit_cuda":
                    setCommand = self.build_bladebit_cuda_command(selected_hdd)
                else:
                    setCommand = self.build_gigahorse_command(selected_hdd)

                # Crée le processus en exécutant la commande
                system = platform.system()
                if system == "Windows":
                    plotter_process = subprocess.Popen(
                        setCommand,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=False,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                else:
                    plotter_process = subprocess.Popen(
                        setCommand,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        shell=False,
                    )

                # Assigne le processus à la variable
                self.none_false_variable.plotter_process = plotter_process

                # Assigne le PID de plotter à la variable
                self.none_false_variable.plotter_pid = plotter_process.pid

                # Met à jour la variable qui dit que la création est en cours
                self.none_false_variable.plot_creation_in_progress = True

                # Message dans la file d'attente
                plotter_executable = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")
                self.queue_logs.log_queue_messages.put((f"Lancement de {plotter_executable} avec le PID: {self.none_false_variable.plotter_pid}", None))
                time.sleep(0.8)

                # Message dans la file d'attente
                self.queue_logs.log_queue_messages.put((f"{' '.join(setCommand)}", None))
                time.sleep(0.8)

                # Démarre des threads pour surveiller la sortie standard de plotter
                stdout_thread = threading.Thread(target=self.log_manager.read_stdout, args=(plotter_process.stdout,))
                stdout_thread.daemon = True
                stdout_thread.start()

                # Démarre des threads pour surveiller la sortie d'erreur de plotter
                stderr_thread = threading.Thread(target=self.log_manager.read_stderr, args=(plotter_process.stderr,))
                stderr_thread.daemon = True
                stderr_thread.start()

                # Attend que plotter se termine
                return_code = self.none_false_variable.plotter_process.wait()

                # Vérifie si plotter s'est terminé normalement
                if return_code == 0:
                    # Message dans la file d'attente
                    self.queue_logs.log_queue_messages.put((f"Création des plots sur le disque {selected_hdd} terminée.", None))
                    # Réinitialise la variable de création en cours
                    self.none_false_variable.plot_creation_in_progress = False
                    # Réinitialise la variable du processus
                    self.none_false_variable.plotter_pid = None
                    # Réinitialise l'interface de progression
                    self.initialize_variables.current_plot_number = 0
                    self.interface.current_plot_text.config(text="0")
                    self.initialize_variables.max_plots_on_selected_hdd = 0
                    self.interface.current_plot_max_text.config(text="0")
                    self.initialize_variables.current_step = 0
                    self.interface.progress_single_plot_bar["value"] = 0
                    self.interface.progress_label.config(text="0%")
                    # On crée un temps d'attente
                    self.count_down(3)
                    # Relancer la création de plots
                    self.start_plotting(show_dialog=False)
                    return

            except FileNotFoundError as e:
                self.queue_logs.log_queue_errors.put(f"Fichier plotter introuvable : {e}")
            except PermissionError as e:
                self.queue_logs.log_queue_errors.put(f"Permission refusée : {e}")
            except Exception as e:
                self.queue_logs.log_queue_errors.put(f"Erreur lors du démarrage de plotter : {e}")
            finally:
                self.none_false_variable.plot_creation_in_progress = False

    def async_stop_plotter_process(self):
        try:
            # Si le process PID existe
            if self.none_false_variable.plotter_pid:
                # On termine le processus plotter
                os.kill(self.none_false_variable.plotter_pid, signal.SIGTERM)

                # Attendre que le processus plotter se termine proprement
                self.none_false_variable.plotter_process.wait()

                # Réinitialise la variable
                self.none_false_variable.plot_creation_in_progress = False

                # Initialise la variable pour change les boutons au moment où l'on stoppe la création
                self.none_false_variable.stop_creation = False

                # Réinitialise l'interface de progression
                self.initialize_variables.current_plot_number = 0
                self.interface.current_plot_text.config(text="0")
                self.initialize_variables.max_plots_on_selected_hdd = 0
                self.interface.current_plot_max_text.config(text="0")
                self.initialize_variables.current_step = 0
                self.interface.progress_single_plot_bar["value"] = 0
                self.interface.progress_label.config(text="0%")

                # Affiche un message
                self.queue_logs.log_queue_messages.put(("Arrêt du processus plotter effectué avec succès.", None))

                # Affiche un message
                self.log_manager.log_plotter_message("Création arrêtée.")

        except Exception as e:
            self.queue_logs.log_queue_errors.put(f"Erreur lors de l'arrêt du processus plotter: {e}")
            # Réinitialise la variable du processus
            self.none_false_variable.plotter_pid = None
            # Réinitialise la variable
            self.none_false_variable.plot_creation_in_progress = False
            # Initialise la variable pour change les boutons au moment où l'on stoppe la création
            self.none_false_variable.stop_creation = False
        finally:
            # Réinitialise la variable du processus
            self.none_false_variable.plotter_pid = None
            # Réinitialise la variable
            self.none_false_variable.plot_creation_in_progress = False
            # Initialise la variable pour change les boutons au moment où l'on stoppe la création
            self.none_false_variable.stop_creation = False

    def stop_or_close(self):
        # Si le processus est lancé
        if self.none_false_variable.plotter_pid:
            # Si le processus plotter est en cours, demandez à l'utilisateur s'il souhaite l'arrêter
            if tkinter.messagebox.askokcancel(
                    "Processus en cours",
                    "Le processus plotter est en cours.\n\n"
                    "Voulez-vous l'arrêter avant de fermer l'application ?"
            ):
                # Affiche un message
                self.queue_logs.log_queue_messages.put((f"Arrêt du processus plotter en cours...", None))

                # Initialise la variable pour change les boutons au moment où l'on stoppe la création
                self.none_false_variable.stop_creation = True

                # Démarrer le thread d'arrêt du processus plotter de manière asynchrone
                stop_thread = threading.Thread(target=self.async_stop_plotter_process)
                stop_thread.start()
        else:
            # Affiche un avertissement
            if tkinter.messagebox.askokcancel(
                    "Fermeture de l'application",
                    "Êtes-vous sûr de vouloir fermer l'application ?"
            ):
                # Fermer la fenêtre
                self.interface.root.destroy()

    # Mise à jour des boutons de l'interface utilisateur
    def update_button_text(self):
        while True:
            if self.none_false_variable.stop_creation:
                # Si la création est en cours d'arrêt, désactiver les boutons
                self.interface.start_button.config(state="disabled")
                self.interface.stop_button.config(state="disabled")
                for element in self.lists.check_plot_elements_disable:
                    element.config(state="disabled")
            else:
                if self.none_false_variable.plotter_pid:
                    # Si la création est en cours
                    self.interface.start_button.config(state="disabled")
                    self.interface.stop_button.config(text="Stopper la création", state="normal")
                    for element in self.lists.check_plot_elements_disable:
                        element.config(state="disabled")

                    # Vérifie le bouton check plot
                    if self.interface.plotter_gui.check_plot_status == "on":
                        self.interface.check_plot_value_combobox.configure(state="disabled")
                        self.interface.check_threshold_value_combobox.configure(state="disabled")

                else:
                    self.interface.stop_button.config(text="Fermer la fenêtre", state="normal")
                    self.interface.start_button.config(state="normal")
                    for element in self.lists.check_plot_elements_disable:
                        element.config(state="normal")

                    # Vérifie le bouton check plot
                    if self.interface.plotter_gui.check_plot_status == "off":
                        self.interface.check_plot_value_combobox.configure(state="disabled")
                        self.interface.check_threshold_value_combobox.configure(state="disabled")
                    else:
                        self.interface.check_plot_value_combobox.configure(state="normal")
                        self.interface.check_threshold_value_combobox.configure(state="normal")

            # Attendez quelques secondes avant de vérifier à nouveau
            time.sleep(1)

    # Mise à jour l'interface utilisateur
    def update_idletasks(self):
        self.interface.root.update_idletasks()

    # Fonction de décompte
    def count_down(self, seconds):
        for seconds_left in range(seconds, 0, -1):
            # Redirection vers log_queue_messages
            self.log_manager.log_plotter_message(f"Recherche d'espace disponible dans {seconds_left} secondes\n")
            # Attendre une seconde entre chaque itération pour obtenir un compte à rebours en temps réel
            time.sleep(1)

    def run(self):
        # Lance l'application
        self.interface.root.mainloop()


if __name__ == "__main__":
    app = FFPlotterGUI()
    app.run()
