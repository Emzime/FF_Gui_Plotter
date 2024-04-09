# main.py
import logging
import math
import os
import platform
import signal
import subprocess
import threading
import time
import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog

import psutil

from Files.config_manager import ConfigManager
from Files.find_method import FindMethod
from Files.initialize_variables import InitializeVariables
from Files.interface import Interface
from Files.lists import Lists
from Files.log_queue import LogQueue, LogManager
from Files.none_false_variables import NoneFalseVariables
from Files.pattern import Pattern
from Files.progress_bar import ProgressBar
from Files.static_method import StaticMethod
from Files.welcome import Welcome


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
        self.log_manager = LogManager(self)
        self.progress_bar = ProgressBar(self)
        self.welcome = Welcome(self)
        self.welcome.show_message()

        # Chemin du répertoire où est situé le script
        temp_path = os.path.dirname(os.path.abspath(__file__))
        plotter_temp_path = os.path.join(temp_path, "Plotter")

        if os.path.exists(self.config_manager.config_file):
            self.config_manager.update_config({"plotter_path": plotter_temp_path}, self.config_manager.config_file)

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

            # Mettre à jour le titre de la fenêtre avec le nom du plotter sélectionné
            plotter_name = os.path.splitext(selected_executable)[0]  # Récupérer le nom sans extension
            self.interface.root.title(f"French Farmer Gui plotter {plotter_name}")

            # Mise à jour des valeurs de la combobox ram_qty en fonction du plotter
            if plotter_name.startswith("bladebit"):
                # Activer check_plot
                self.interface.check_button.configure(state="normal")
                self.interface.check_button.config(image=self.interface.logging_button_on, background="#1C1C1C")
                self.interface.check_label.config(foreground="#0792ea")
                self.interface.check_plot_status = "on"

                # Mise à jour de l'interface
                self.interface.ssd_temp2move_label.config(text="Disque temporaire -2")
                self.interface.check_plot_value_combobox.configure(state="normal")
                self.interface.check_threshold_value_combobox.configure(state="normal")

                # Mise à jour du fichier de configuration
                self.interface.plotter_gui.config_manager.update_config({"check_plot_status": "on"}, self.config_manager.config_file)

                # Change les listes déroulantes
                compression = [str(compression) for compression in range(1, 8)]
                ram_qty_values = ["16", "128", "256"]
            else:
                # Désactiver check_plot
                self.interface.check_button.configure(state="disabled")
                self.interface.check_button.config(image=self.interface.logging_button_off, background="#1C1C1C")
                self.interface.check_label.config(foreground="red")
                self.interface.check_plot_status = "off"

                # Récupère la quantité de mémoire
                current_ram_qty = self.config_manager.read_config(self.config_manager.config_file).get("ram_qty")

                # Mise à jour de l'interface
                if int(current_ram_qty) == 128:
                    self.interface.ssd_temp2move_label.config(text="Disque temporaire -2")
                elif int(current_ram_qty) < 128:
                    self.interface.ssd_temp2move_label.config(text="Disque temporaire -3")

                self.interface.check_plot_value_combobox.configure(state="disabled")
                self.interface.check_threshold_value_combobox.configure(state="disabled")

                # Mise à jour du fichier de configuration
                self.interface.plotter_gui.config_manager.update_config({"check_plot_status": "off"}, self.config_manager.config_file)

                # Change les listes déroulantes
                if plotter_name == "cuda_plot_k32":
                    # Générer la liste des compressions de 1 à 20
                    compression = [str(compression) for compression in range(1, 21)]
                    # Retirer la valeur 10 de la liste des compressions si elle est présente
                    if '10' in compression:
                        compression.remove('10')
                    ram_qty_values = ["16", "32", "64", "128", "256", "512"]
                else:
                    # Si le plotter est bladebit, n'afficher que les compressions de 29 à 33
                    compression = [str(compression) for compression in range(29, 34)]
                    ram_qty_values = ["16", "32", "64", "128", "256", "512"]

            # Assigne la liste de la combobox ram_qty en fonction du plotter sélectionné
            self.interface.compression_combobox['values'] = compression

            # Assigne la liste de la combobox compression en fonction du plotter sélectionné
            self.interface.ram_qty_combobox['values'] = ram_qty_values

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

        # Construire la commande de création de plot pour bladebit cuda
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
        # Récupérer le nom sans extension
        plotter_name = os.path.splitext(plotter_executable)[0]
        plotter_path = self.config_manager.read_config(self.config_manager.config_file).get("plotter_path")
        ssd_temp = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp")
        ssd_temp2 = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move")
        ram_qty_gb = float(self.config_manager.read_config(self.config_manager.config_file).get("ram_qty"))
        gpu_1_value = str(self.config_manager.read_config(self.config_manager.config_file).get("gpu_1", "0"))
        gpu_2_value = str(self.config_manager.read_config(self.config_manager.config_file).get("gpu_2", ""))
        maxtmp_value = str(self.config_manager.read_config(self.config_manager.config_file).get("maxtmp", ""))
        copylimit_value = str(self.config_manager.read_config(self.config_manager.config_file).get("copylimit", ""))
        maxcopy_value = str(self.config_manager.read_config(self.config_manager.config_file).get("maxcopy", ""))
        waitforcopy_value = str(self.config_manager.read_config(self.config_manager.config_file).get("waitforcopy", ""))

        # Construit le chemin complet de l'exécutable
        plotter_path_join = os.path.join(plotter_path, plotter_executable)

        # Ajouter un trailing slash s'il n'y en a pas déjà un à -t
        if not ssd_temp.endswith(os.path.sep):
            ssd_temp += os.path.sep

        # Ajouter un trailing slash s'il n'y en a pas déjà un à -2
        if not ssd_temp2.endswith(os.path.sep):
            ssd_temp2 += os.path.sep

        # Ajouter un trailing slash s'il n'y en a pas déjà un à -d
        if not selected_hdd.endswith(os.path.sep):
            selected_hdd += os.path.sep

        # Construire la commande de création de plot pour gigaHorse
        command = [
            plotter_path_join,
            "-c", self.config_manager.read_config(self.config_manager.config_file).get("contract"),
            "-f", self.config_manager.read_config(self.config_manager.config_file).get("farmer_key"),
            "-n", str(self.initialize_variables.max_plots_on_selected_hdd),
            "-C", self.config_manager.read_config(self.config_manager.config_file).get("compression"),
        ]

        # Ajoute les arguments liés au GPU 1
        if gpu_1_value:
            command.extend([
                "-g", gpu_1_value,
            ])

        # Ajoute les arguments liés au GPU 2
        if gpu_2_value:
            command.extend([
                "-g", gpu_2_value,
            ])

        # Ajoute les arguments liés -Q
        if maxtmp_value:
            command.extend([
                "-Q", maxtmp_value,
            ])

        # Ajoute les arguments liés -A
        if copylimit_value:
            command.extend([
                "-A", copylimit_value,
            ])

        # Ajoute les arguments liés -W
        if maxcopy_value:
            command.extend([
                "-W", maxcopy_value,
            ])

        # Ajoute les arguments liés -w
        if waitforcopy_value == "on":
            command.extend([
                "-w", waitforcopy_value,
            ])

        # Ajoute les arguments liés au disque temporaire
        command.extend([
            "-t", ssd_temp,
        ])

        # Si le système est windows
        if system == "Windows":
            # Convertir de Go en GiB
            ram_qty_gib = ram_qty_gb * 0.93132
            # Diviser par 2 pour windows
            ram_qty_gib_divided = math.floor(ram_qty_gib / 2)
            # Défini la variable pour la ram
            ramQty = ram_qty_gib_divided

            # Ajoute les arguments liés à la ram pour windows
            # if ram_qty_gb == 128:
            command.extend([
                "-M", str(int(ramQty)),
            ])

        # Ajoute les arguments liés au disque temporaire 2
        if ssd_temp2 != "":
            # Modifier le disque temporaire utilisé selon la quantité de RAM sélectionnée
            if plotter_name.startswith("cuda_plot_"):
                if ram_qty_gb == 128:
                    # ajoute le champ à la commande
                    command.extend([
                        "-2", ssd_temp2,
                    ])
                elif ram_qty_gb < 128:
                    # Ajoute le champ à la commande
                    command.extend([
                        "-3", ssd_temp2,
                    ])
            elif plotter_name.startswith("bladebit"):
                # ajoute le champ à la commande
                command.extend([
                    "-2", ssd_temp2,
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
                plotter_name = os.path.splitext(plotter_executable)[0]

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
                if plotter_name == "bladebit_cuda" or plotter_name.startswith("bladebit-cuda"):
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

                    # Désactiver le combobox GPU 2 si moins de deux GPUs sont connectés
                    if len(self.interface.gpu_connected) < 2:
                        self.interface.gpu_2_combobox.configure(state="disabled")
                        # Réinitialiser la valeur sélectionnée du deuxième GPU
                        self.interface.gpu_2_value_var.set("")

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
