# interface.py
import os
import platform
import tkinter as tk
from tkinter import ttk, Frame, Label

import GPUtil
from ttkthemes.themed_style import ThemedStyle

from Files.translation import Lang
from Files.version import CheckVersion
from Files.discord_news import Discord


class Interface:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.static_method = ff_plotter_gui.static_method
        self.updateValues = UpdateValues(self.plotter_gui)
        self.buttonSwitch = ButtonSwitch(self.plotter_gui)
        self.onMouseEnter = OnMouseEnter(self.plotter_gui)
        self.onMouseLeave = OnMouseLeave(self.plotter_gui)
        self.newVersion = CheckVersion()
        self.discord = Discord()

        directory_path = os.path.dirname(os.path.dirname(__file__))
        # Récupère la valeur dans la configuration
        plotter_directory = self.config_manager.plotter_directory

        # Récupère le nom du plotter utilisé
        current_plotter = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")
        if current_plotter is not None:
            current_plotter_name = os.path.splitext(current_plotter)[0]
        else:
            # Faites quelque chose au cas où la valeur est None
            current_plotter_name = "Unknown"

        # Initialisation des éléments de l'interface
        self.root = tk.Tk()
        # Déterminer le système d'exploitation en cours d'exécution
        system = platform.system()
        # Liste pour stocker les exécutables disponibles
        available_executables = []
        # Initialiser gpu_connected comme une liste vide
        self.gpu_connected = []

        # Parcourir les fichiers dans le répertoire "Plotter" et normaliser les chemins
        for file_name in os.listdir(plotter_directory):
            file_path = os.path.join(plotter_directory, file_name)
            normalized_file_path = os.path.normpath(file_path)  # Normaliser le chemin
            # Vérifier si le fichier est un exécutable et s'il est exécutable sur le système en cours
            if os.path.isfile(normalized_file_path) and os.access(normalized_file_path, os.X_OK):
                # Filtrer les exécutables compatibles avec le système en cours
                if system == "Windows" and file_name.endswith(".exe"):
                    available_executables.append(file_name)
                elif system != "Windows" and not file_name.endswith(".exe"):
                    available_executables.append(file_name)
        # Stylisation avec ttk
        style = ThemedStyle(self.root)
        style.theme_use("clam")
        style.configure("Custom.TLabel", background="#1C1C1C", foreground="#0792ea")
        style.configure("TButton")
        style.configure("Custom.Horizontal.TProgressbar", troughcolor="#1C1C1C", background="#00DF03", thickness=10)
        style.configure('CustomSend.TButton', background='#9C9C9C')

        # Ajouter le message de version à la fenêtre principale
        self.current_version, self.latest_version = self.newVersion.check_new_package_version()
        new_message = Lang.translate("newVersionAvailable").format(latest_version=self.latest_version)
        old_message = Lang.translate("currentVersion").format(current_version=self.current_version)

        if self.latest_version is not None and self.current_version < self.latest_version:
            self.root.title(Lang.translate("guiName") + new_message)
            # Ajouter un label dans la barre de titre pour simuler un lien
            self.title_label = Label(self.root, text=new_message)
            self.title_label.configure(background="#0792ea", foreground="#FFFF00")
            self.title_label.bind("<Button-1>", lambda event: self.static_method.open_new_version_link)
            # Associer les fonctions aux événements de survol de la souris
            self.title_label.bind("<Enter>", self.onMouseEnter.new_version_link)
            self.title_label.bind("<Leave>", self.onMouseLeave.new_version_link)
            self.title_label.grid(row=0, column=0, padx=0, pady=0)
        else:
            self.root.title(Lang.translate("guiName") + old_message)

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
        top_left_column.grid(row=0, column=0, padx=(10, 5), pady=(0, 0), sticky="nsew")

        # Ajoutez des poids pour centrer verticalement
        top_left_column.grid_rowconfigure(0, weight=1)

        # Ajoutez des poids pour partager la largeur
        top_left_column.grid_columnconfigure(0, weight=1)

        # Bouton pour activer/désactiver la journalisation (à droite)
        logging_frame = tk.Frame(top_left_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        logging_frame.grid(row=0, column=0, padx=0, pady=(10, 5), sticky="nsew")

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
        self.logging_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text=Lang.translate("logFile"))
        self.logging_label.grid(row=0, column=0, padx=(5, 5), pady=(0, 0), sticky="ew")

        self.logging_button = tk.Button(inner_frame, border=0, command=self.buttonSwitch.logs)
        self.logging_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.logging_button.grid(row=1, column=0, padx=(5, 5), pady=(5, 20), sticky="ew")
        self.logging_button.config(cursor="hand2", state="normal")

        # Associer les fonctions aux événements de survol de la souris
        self.logging_button.bind("<Enter>", self.onMouseEnter.logging_button)
        self.logging_button.bind("<Leave>", self.onMouseLeave.logging_button)

        # Chargez l'image dans une variable de classe spécifique pour le bouton de logging
        logging_button_off_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "off.png"))
        self.logging_button_off = tk.PhotoImage(file=logging_button_off_path)

        logging_button_on_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "on.png"))
        self.logging_button_on = tk.PhotoImage(file=logging_button_on_path)

        # Configurez le bouton de logging en fonction de la valeur de logs_status
        if self.plotter_gui.logs_status == Lang.translate("on"):
            self.logging_button.config(image=self.logging_button_on, background="#1C1C1C")
            self.logging_label.config(foreground="#00B34D")
            self.logging_label.grid_rowconfigure(0, weight=1)
        else:
            self.logging_button.config(image=self.logging_button_off, background="#1C1C1C")
            self.logging_label.config(foreground="#F10000")
            self.logging_label.grid_rowconfigure(0, weight=1)

        # Bouton on / off de plot check
        self.check_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text=Lang.translate("plotCheck"))
        self.check_label.grid(row=0, column=1, padx=(5, 5), pady=(0, 0), sticky="ew")

        self.check_button = tk.Button(inner_frame, border=0, command=self.buttonSwitch.check)
        self.check_button.grid(row=1, column=1, padx=(5, 5), pady=(5, 20), sticky="ew")
        self.check_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.check_button.config(cursor="hand2")

        # Associer les fonctions aux événements de survol de la souris
        self.check_button.bind("<Enter>", self.onMouseEnter.check_button)
        self.check_button.bind("<Leave>", self.onMouseLeave.check_button)

        # Chargez l'image dans une variable de classe spécifique pour le bouton de check
        check_button_off_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "off.png"))
        self.check_button_off = tk.PhotoImage(file=check_button_off_path)

        check_button_on_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "on.png"))
        self.check_button_on = tk.PhotoImage(file=check_button_on_path)

        if current_plotter_name.startswith("bladebit"):
            # Configurez le bouton de check en fonction de la valeur de check_plot_status
            if self.plotter_gui.check_plot_status == Lang.translate("on"):
                self.check_button.config(image=self.check_button_on, background="#1C1C1C")
                self.check_label.config(foreground="#00B34D")
                self.plotter_gui.check_plot_status = Lang.translate("on")
                # Ajoutez des poids pour partager la hauteur
                self.check_label.grid_rowconfigure(0, weight=1)
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("on")}, self.config_manager.config_file)
            else:
                self.check_button.config(image=self.check_button_off, background="#1C1C1C")
                self.check_label.config(foreground="#F10000")
                self.plotter_gui.check_plot_status = Lang.translate("off")
                # Ajoutez des poids pour partager la hauteur
                self.check_label.grid_rowconfigure(0, weight=1)
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("off")}, self.config_manager.config_file)
        else:
            self.check_button.configure(state="disabled")
            self.check_button.config(image=self.check_button_off, background="#1C1C1C")
            self.check_label.config(foreground="#F10000")
            self.plotter_gui.check_plot_status = Lang.translate("off")
            # Ajoutez des poids pour partager la hauteur
            self.check_label.grid_rowconfigure(0, weight=1)
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("off")}, self.config_manager.config_file)

        # Bouton on / off de suppression des anciens plots
        self.delPlot_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text=Lang.translate("delPlot"))
        self.delPlot_label.grid(row=0, column=2, padx=(5, 5), pady=(0, 0), sticky="ew")
        # Ajoutez des poids pour partager la hauteur
        self.delPlot_label.grid_rowconfigure(0, weight=1)

        self.delPlot_button = tk.Button(inner_frame, border=0, command=self.buttonSwitch.del_plot)
        self.delPlot_button.grid(row=1, column=2, padx=(5, 5), pady=(5, 20), sticky="ew")
        self.delPlot_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.delPlot_button.config(cursor="hand2")

        # Chargez l'image dans une variable de classe spécifique pour le bouton de delPlot
        delPlot_button_off_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "off.png"))
        self.delPlot_button_off = tk.PhotoImage(file=delPlot_button_off_path)

        delPlot_button_on_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "on.png"))
        self.delPlot_button_on = tk.PhotoImage(file=delPlot_button_on_path)

        if self.plotter_gui.delCompressedPlot_status == Lang.translate("on"):
            self.delPlot_button.config(image=self.delPlot_button_on, background="#1C1C1C")
            self.delPlot_label.config(foreground="#00B34D")
            self.plotter_gui.delCompressedPlot_status = Lang.translate("on")
        else:
            self.delPlot_button.config(image=self.delPlot_button_off, background="#1C1C1C")
            self.delPlot_label.config(foreground="#F10000")
            self.plotter_gui.delCompressedPlot_status = Lang.translate("off")

        # Associer les fonctions aux événements de survol de la souris
        self.delPlot_button.bind("<Enter>", self.onMouseEnter.delPlot_button)
        self.delPlot_button.bind("<Leave>", self.onMouseLeave.delPlot_button)

        # Créez la Frame supérieure (top_column)
        top_right_column = tk.Frame(main_frame, bg="#1C1C1C")
        top_right_column.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="nsew")

        # Ajoutez des poids pour partager la hauteur
        top_right_column.grid_rowconfigure(0, weight=1)
        top_right_column.grid_rowconfigure(1, weight=1)
        # Ajoutez des poids pour partager la largeur
        top_right_column.grid_columnconfigure(0, weight=0)
        top_right_column.grid_columnconfigure(1, weight=1)

        # Crée une Frame pour la progression du plot (à gauche)
        progress_current_plot_frame = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        progress_current_plot_frame.grid(row=0, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
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
        self.total_plot_text = tk.Label(progress_current_plot_frame, text=Lang.translate("totalPlotsCreated"), bg="#1C1C1C", fg="#BFBFBF")
        self.total_plot_text.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre total de plots créés
        self.total_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("total_plot_created"), bg="#1C1C1C", fg="#BFBFBF")
        self.total_plot_number_label.grid(row=0, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le nombre d'anciens plots supprimés
        self.deleted_plot_text = tk.Label(progress_current_plot_frame, text=Lang.translate("totalOldPlotsDeleted"), bg="#1C1C1C", fg="#BFBFBF")
        self.deleted_plot_text.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre d'anciens plots supprimés
        self.deleted_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("deleted_plot_number"), bg="#1C1C1C", fg="#BFBFBF")
        self.deleted_plot_number_label.grid(row=1, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour le nombre de plots supprimés lors de la création
        self.bad_plot_text = tk.Label(progress_current_plot_frame, text=Lang.translate("totalNewPlotsDeleted"), bg="#1C1C1C", fg="#BFBFBF")
        self.bad_plot_text.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le nombre de plots supprimés lors de la création
        self.bad_plot_number_label = tk.Label(progress_current_plot_frame, text=self.config_manager.read_config(self.config_manager.config_stats).get("bad_plot_number"), bg="#1C1C1C", fg="#BFBFBF")
        self.bad_plot_number_label.grid(row=2, column=1, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le texte le numéro du plot en cours
        self.current_plot_max_label = tk.Label(progress_current_plot_frame, text=Lang.translate("plotsToCreate"), bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_max_label.grid(row=0, column=2, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.current_plot_max_text = tk.Label(progress_current_plot_frame, text=self.initialize_variables.max_plots_on_selected_hdd, bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_max_text.grid(row=0, column=3, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée un label pour afficher le texte le numéro du plot en cours
        self.current_plot_label = tk.Label(progress_current_plot_frame, text=Lang.translate("plotsCreated"), bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_label.grid(row=1, column=2, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.current_plot_text = tk.Label(progress_current_plot_frame, text=self.initialize_variables.current_plot_number, bg="#1C1C1C", fg="#BFBFBF")
        self.current_plot_text.grid(row=1, column=3, padx=(0, 10), pady=(0, 0), sticky="w")

        # Crée une barre de progression pour le plot
        self.progress_single_plot_bar = ttk.Progressbar(progress_current_plot_frame, orient="horizontal", mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_single_plot_bar.grid(row=2, column=2, padx=(14, 5), pady=(0, 0), sticky="ew")

        self.progress_label = tk.Label(progress_current_plot_frame, text="", anchor="center", bg="#1C1C1C", fg="#BFBFBF")
        self.progress_label.grid(row=2, column=3, padx=(0, 5), pady=(0, 0), sticky="ew")

        # Mise à jour de la barre
        self.progress_single_plot_bar["value"] = 0
        self.progress_label.config(text=f"0%")
        self.progress_single_plot_bar.update_idletasks()
        self.progress_label.update_idletasks()

        # Crée une Frame pour la progression du plot
        news_plot_frame = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        news_plot_frame.grid(row=0, column=1, padx=(5, 0), pady=(0, 0), sticky="nsew")

        # Ajoutez des poids pour partager la hauteur
        news_plot_frame.grid_rowconfigure(0, weight=1)
        news_plot_frame.grid_rowconfigure(1, weight=1)
        # Ajoutez des poids pour partager la largeur
        news_plot_frame.grid_columnconfigure(0, weight=1)

        # Créer une sous-frame pour le logo FF
        self.input_logo = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        self.input_logo.grid(row=0, column=2, padx=(5, 5), pady=(0, 0), sticky="nsew")

        # Chargez l'image dans une variable de classe
        self.logo_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "logo.png"))
        self.input_logo_img = tk.PhotoImage(file=self.logo_path).subsample(1)

        # Créez un label pour afficher l'image
        self.logo_label = ttk.Label(self.input_logo, image=self.input_logo_img, background="#1C1C1C", anchor="center")
        self.logo_label.grid(row=0, column=1, padx=(5, 5), pady=(7, 0), sticky="w")
        # Ajoutez des poids pour partager la hauteur
        self.logo_label.grid_rowconfigure(0, weight=1)

        # Assurez-vous que l'image ne soit pas collectée par le garbage collector
        self.logo_label.photo = self.input_logo_img
        # Associer la fonction au clic sur l'image
        self.logo_label.bind("<Button-1>", self.static_method.open_site_link)
        # Associer les fonctions aux événements de survol de la souris
        self.logo_label.bind("<Enter>", self.onMouseEnter.site_link)
        self.logo_label.bind("<Leave>", self.onMouseLeave.site_link)

        # Créer une sous-frame pour le logo discord
        self.input_logo_discord = tk.Frame(top_right_column, bg="#1C1C1C", highlightthickness=1, highlightbackground="#565656")
        self.input_logo_discord.grid(row=0, column=3, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Chargez l'image dans une variable de classe
        self.logo_path_discord = self.static_method.resource_path(os.path.join(directory_path, "Images", "discord.png"))
        self.input_logo_discord_img = tk.PhotoImage(file=self.logo_path_discord).subsample(1)

        # Créez un label pour afficher l'image
        self.logo_label_discord = ttk.Label(self.input_logo_discord, image=self.input_logo_discord_img, background="#1C1C1C", anchor="center")
        self.logo_label_discord.grid(row=0, column=1, padx=(5, 5), pady=(5, 5), sticky="w")
        # Ajoutez des poids pour partager la hauteur
        self.logo_label_discord.grid_rowconfigure(0, weight=1)

        # Assurez-vous que l'image ne soit pas collectée par le garbage collector
        self.logo_label_discord.photo = self.input_logo_discord_img
        # Associer la fonction au clic sur l'image
        self.logo_label_discord.bind("<Button-1>", self.static_method.open_discord_link)
        # Associer les fonctions aux événements de survol de la souris
        self.logo_label_discord.bind("<Enter>", self.onMouseEnter.discord_link)
        self.logo_label_discord.bind("<Leave>", self.onMouseLeave.discord_link)

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

        # Créer une sous-frame pour plotter_path
        self.input_subframe_1 = tk.Frame(input_frame, bg="#1C1C1C")
        self.input_subframe_1.grid(row=1, column=0, columnspan=4, padx=(0, 0), pady=(15, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_1.columnconfigure(0, weight=1)

        # Ligne 5 : Chemin vers l'exécutable de plotter
        self.plotter_path_label = tk.Label(self.input_subframe_1, text=Lang.translate("selectPlotter"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.plotter_path_label.grid(row=0, column=0, pady=(0, 1), padx=4, sticky="nsew", columnspan=2)

        # Créer une liste déroulante avec les exécutables disponibles
        self.plotter_path_combobox = ttk.Combobox(self.input_subframe_1, values=available_executables, state="readonly")
        self.plotter_path_combobox.grid(row=1, column=0, pady=(0, 0), padx=4, sticky="nsew", columnspan=2)
        self.plotter_path_combobox.bind("<<ComboboxSelected>>", self.plotter_gui.on_combobox_selected)
        # Associer les fonctions aux événements de survol de la souris
        self.plotter_path_combobox.bind("<Enter>", self.onMouseEnter.plotter_path_combobox)
        self.plotter_path_combobox.bind("<Leave>", self.onMouseLeave.plotter_path_combobox)
        self.plotter_path_combobox.set(current_plotter)

        # Créer une sous-frame pour check_plot
        self.input_subframe_2 = tk.Frame(self.input_subframe_1, bg="#1C1C1C")
        self.input_subframe_2.grid(row=2, column=0, columnspan=4, padx=(0, 0), pady=(10, 10), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_2.columnconfigure(0, weight=1)
        self.input_subframe_2.columnconfigure(1, weight=1)

        # Ligne 3 : check_plot
        self.check_plot_value_label = tk.Label(self.input_subframe_2, text=Lang.translate("numberOfCheck"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.check_plot_value_label.grid(row=0, column=0, pady=(0, 1), padx=(5, 5), sticky="nsew")

        check_plot_value = self.config_manager.read_config(self.config_manager.config_file).get("check_plot_value")
        self.check_plot_value_var = tk.StringVar(value=check_plot_value)

        self.check_plot_value_combobox = ttk.Combobox(self.input_subframe_2, textvariable=self.check_plot_value_var, state="readonly")
        self.check_plot_value_combobox.grid(row=1, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_plot_value_combobox['values'] = ["30", "60", "100", "300", "500", "700", "1000"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_plot_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.check_plot_value_config())
        # Associer les fonctions aux événements de survol de la souris
        self.check_plot_value_combobox.bind("<Enter>", self.onMouseEnter.check_plot_value_combobox)
        self.check_plot_value_combobox.bind("<Leave>", self.onMouseLeave.check_plot_value_combobox)

        # Ligne 4 : check_threshold
        self.check_threshold_value_label = tk.Label(self.input_subframe_2, text=Lang.translate("proofRateInPercent"), background="#1C1C1C", foreground="#0792ea")
        self.check_threshold_value_label.grid(row=0, column=1, pady=(0, 1), padx=(5, 5), sticky="nsew")

        check_threshold_value = self.config_manager.read_config(self.config_manager.config_file).get("check_threshold_value")
        self.check_threshold_value_var = tk.StringVar(value=check_threshold_value)
        self.check_threshold_value_combobox = ttk.Combobox(self.input_subframe_2, textvariable=self.check_threshold_value_var, state="readonly")
        self.check_threshold_value_combobox.grid(row=1, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_threshold_value_combobox['values'] = ["80", "85", "90", "95", "100"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_threshold_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.check_threshold_config())
        # Associer les fonctions aux événements de survol de la souris
        self.check_threshold_value_combobox.bind("<Enter>", self.onMouseEnter.check_threshold_value_combobox)
        self.check_threshold_value_combobox.bind("<Leave>", self.onMouseLeave.check_threshold_value_combobox)

        if current_plotter_name.startswith("bladebit"):
            # Configurez le combobox de check en fonction de la valeur de check_plot_status
            if self.plotter_gui.check_plot_status == Lang.translate("on"):
                # Activer la Combobox
                self.check_plot_value_combobox.configure(state="normal")
                self.check_threshold_value_combobox.configure(state="normal")
            else:
                # Désactiver la Combobox
                self.check_plot_value_combobox.configure(state="disabled")
                self.check_threshold_value_combobox.configure(state="disabled")
        else:
            self.check_plot_value_combobox.configure(state="disabled")
            self.check_threshold_value_combobox.configure(state="disabled")

        # Créer une sous-frame
        self.input_subframe_3: Frame = tk.Frame(self.input_subframe_2, bg="#1C1C1C")
        self.input_subframe_3.grid(row=3, column=0, columnspan=4, padx=(0, 0), pady=(10, 10), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_3.columnconfigure(0, weight=1)
        self.input_subframe_3.columnconfigure(1, weight=1)

        # Ligne 1 : Taux de compression du plot
        self.compression_label = tk.Label(self.input_subframe_3, text=Lang.translate("compressionRate"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.compression_label.grid(row=0, column=0, pady=(0, 1), padx=(5, 5), sticky="nsew")

        # Récupérez les valeurs de compression à partir de InitializeVariables.plotSizes
        current_compression = self.config_manager.read_config(self.config_manager.config_file).get("compression")
        current_ram_qty = self.config_manager.read_config(self.config_manager.config_file).get("ram_qty")

        if current_plotter_name.startswith("bladebit"):
            # Si le plotter est bladebit, n'afficher que les compressions de 1 à 7
            compression_values = [str(compression) for compression in range(1, 8)]
            # Si la compression est supérieure à 7, assigner 5 par défaut
            compression = int(current_compression) if int(current_compression) <= 7 else 5
            ram_qty_values = ["16", "128", "256"]
        elif current_plotter_name.startswith("cuda_plot_k32_"):
            # Si le plotter est cuda_plot_k32, n'afficher que les compressions de 29 à 33
            compression_values = [str(compression) for compression in range(29, 34)]
            compression = int(current_compression)
            ram_qty_values = ["16", "32", "64", "128", "256", "512"]
        else:
            # Si le plotter est un autre, n'afficher que les compressions de 1 à 9 et de 11 à 20
            compression_values = [str(compression) for compression in range(1, 21)]
            # Retirer la valeur 10 de la liste des compressions si elle est présente
            if '10' in compression_values:
                compression_values.remove('10')
            compression = int(current_compression)
            ram_qty_values = ["16", "32", "64", "128", "256", "512"]

        # Créer une variable pour la valeur de compression
        self.compression_var = tk.StringVar(value=str(compression))
        self.compression_combobox = ttk.Combobox(self.input_subframe_3, textvariable=self.compression_var, state="readonly")
        self.compression_combobox.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.compression_combobox['values'] = compression_values
        # Associer la fonction à l'événement de changement de la combobox
        self.compression_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.compression_config())
        # Associer les fonctions aux événements de survol de la souris
        self.compression_combobox.bind("<Enter>", self.onMouseEnter.compression_combobox)
        self.compression_combobox.bind("<Leave>", self.onMouseLeave.compression_combobox)

        # Ligne 2 : Quantité de RAM
        self.ram_qty_label = tk.Label(self.input_subframe_3, text=Lang.translate("ramQuantity"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.ram_qty_label.grid(row=0, column=1, pady=(0, 1), padx=(5, 5), sticky="nsew")
        # Créer une variable pour la valeur de RAM
        self.ram_qty_var = tk.StringVar(value=current_ram_qty)
        self.ram_qty_combobox = ttk.Combobox(self.input_subframe_3, textvariable=self.ram_qty_var, values=ram_qty_values, state="readonly", background="#1C1C1C")
        self.ram_qty_combobox.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")
        # Associer la fonction à l'événement de changement de la combobox
        self.ram_qty_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.ram_config())
        # Associer les fonctions aux événements de survol de la souris
        self.ram_qty_combobox.bind("<Enter>", self.onMouseEnter.ram_qty_combobox)
        self.ram_qty_combobox.bind("<Leave>", self.onMouseLeave.ram_qty_combobox)

        # Créer une sous-frame pour compression_label, ram_qty_label
        self.input_subframe_4 = tk.Frame(self.input_subframe_3, bg="#1C1C1C")
        self.input_subframe_4.grid(row=4, column=0, columnspan=4, padx=(0, 0), pady=(10, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_4.columnconfigure(0, weight=1)
        self.input_subframe_4.columnconfigure(1, weight=1)

        # Ligne 3 : Pool contract
        self.contract_label = tk.Label(self.input_subframe_4, text=Lang.translate("poolContract"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.contract_label.grid(row=0, column=0, pady=(0, 1), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle du contrat de pool
        current_contract_key = self.config_manager.read_config(self.config_manager.config_file).get("contract")
        self.contract_var = tk.StringVar(value=current_contract_key)
        self.contract_entry = ttk.Entry(self.input_subframe_4, background="#cccccc", textvariable=self.contract_var)
        self.contract_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.contract_entry.bind("<FocusOut>", lambda event=None: self.updateValues.contract_config())
        # Associer les fonctions aux événements de survol de la souris
        self.contract_entry.bind("<Enter>", self.onMouseEnter.contract_entry)
        self.contract_entry.bind("<Leave>", self.onMouseLeave.contract_entry)

        # Ligne 4 : Farmer public key
        self.farmer_key_label = tk.Label(self.input_subframe_4, text=Lang.translate("farmerPublicKey"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.farmer_key_label.grid(row=0, column=1, pady=(0, 1), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle de la clé du fermier
        current_farmer_key = self.config_manager.read_config(self.config_manager.config_file).get("farmer_key")
        self.farmer_key_var = tk.StringVar(value=current_farmer_key)
        self.farmer_key_entry = ttk.Entry(self.input_subframe_4, background="#cccccc", textvariable=self.farmer_key_var)
        self.farmer_key_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew", columnspan=2)

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.farmer_key_entry.bind("<FocusOut>", lambda event=None: self.updateValues.farmer_key_config())
        # Associer les fonctions aux événements de survol de la souris
        self.farmer_key_entry.bind("<Enter>", self.onMouseEnter.farmer_key_entry)
        self.farmer_key_entry.bind("<Leave>", self.onMouseLeave.farmer_key_entry)

        # Créer une sous-frame pour ssd_temp et ssd_temp2move
        self.input_subframe_5 = tk.Frame(self.input_subframe_2, bg="#1C1C1C")
        self.input_subframe_5.grid(row=5, column=0, columnspan=4, padx=(0, 0), pady=(0, 10), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_5.columnconfigure(0, weight=1)
        self.input_subframe_5.columnconfigure(1, weight=1)

        # Ligne 6 : Disque temporaire -t1 (nvme/ssd)
        self.ssd_temp_label = tk.Label(self.input_subframe_5, text=Lang.translate("temporaryDisk_t"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.ssd_temp_label.grid(row=0, column=0, pady=(0, 1), padx=(5, 5), sticky="nsew")

        self.ssd_temp_entry = ttk.Entry(self.input_subframe_5, background="#cccccc")
        self.ssd_temp_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp")
        if ssd_temp_value is None or ssd_temp_value == "":
            ssd_temp_value = self.config_manager.defaults["ssd_temp"]

        self.ssd_temp_entry.insert(0, ssd_temp_value)
        # Associer les fonctions aux événements de survol de la souris
        self.ssd_temp_entry.bind("<Enter>", self.onMouseEnter.ssd_temp_entry)
        self.ssd_temp_entry.bind("<Leave>", self.onMouseLeave.ssd_temp_entry)

        self.ssd_temp_button = ttk.Button(self.input_subframe_5, text=Lang.translate("browse"), command=self.plotter_gui.browse_ssd_temp)
        self.ssd_temp_button.grid(row=2, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp_button.config(cursor="hand2")

        # Ligne 7 : Disque temporaire 2
        temp2move_text = ""
        if current_plotter_name.startswith("cuda_plot"):
            if int(current_ram_qty) == 128:
                temp2move_text = Lang.translate("temporaryDisk_2")
            elif int(current_ram_qty) < 128:
                temp2move_text = Lang.translate("temporaryDisk_3")
        elif current_plotter_name.startswith("bladebit"):
            temp2move_text = Lang.translate("temporaryDisk_2")
        else:
            temp2move_text = Lang.translate("temporaryDisk_2")

        self.ssd_temp2move_label = tk.Label(self.input_subframe_5, text=temp2move_text, anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.ssd_temp2move_label.grid(row=0, column=1, pady=(0, 1), padx=(5, 5), sticky="nsew")

        self.ssd_temp2move_entry = ttk.Entry(self.input_subframe_5, background="#cccccc")
        self.ssd_temp2move_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp2move_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move")
        if not ssd_temp2move_value:
            ssd_temp2move_value = self.config_manager.defaults["ssd_temp2move"]

        self.ssd_temp2move_entry.insert(0, ssd_temp2move_value)
        # Associer les fonctions aux événements de survol de la souris
        self.ssd_temp2move_entry.bind("<Enter>", self.onMouseEnter.ssd_temp2move_entry)
        self.ssd_temp2move_entry.bind("<Leave>", self.onMouseLeave.ssd_temp2move_entry)

        self.ssd_temp2move_button = ttk.Button(self.input_subframe_5, text=Lang.translate("browse"), command=self.plotter_gui.browse_ssd_temp2move)
        self.ssd_temp2move_button.grid(row=2, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp2move_button.config(cursor="hand2")
        if int(current_ram_qty) >= 256:
            self.ssd_temp2move_button.configure(state="disabled")

        # Créer une sous-frame pour hdd_dir
        self.input_subframe_6 = tk.Frame(self.input_subframe_5, bg="#1C1C1C")
        self.input_subframe_6.grid(row=6, column=0, columnspan=2, padx=0, pady=(10, 10), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_6.columnconfigure(0, weight=1)
        self.input_subframe_6.columnconfigure(1, weight=1)

        # Ligne 8 : Dossier de destination -d
        self.hdd_dir_label = tk.Label(self.input_subframe_6, text=Lang.translate("destinationDisks_d"), anchor="center", background="#1C1C1C", foreground="#0792ea")
        self.hdd_dir_label.grid(row=0, column=0, pady=(0, 1), padx=5, sticky="nsew", columnspan=2)

        self.hdd_dir_listbox = tk.Listbox(self.input_subframe_6, selectmode=tk.MULTIPLE, height=4, bg="#cccccc")
        self.hdd_dir_listbox.grid(row=1, column=0, pady=(0, 0), padx=5, sticky="nsew", columnspan=2)
        # Associer les fonctions aux événements de survol de la souris
        self.hdd_dir_listbox.bind("<Enter>", self.onMouseEnter.hdd_dir_listbox)
        self.hdd_dir_listbox.bind("<Leave>", self.onMouseLeave.hdd_dir_listbox)

        hdd_dir_value = self.config_manager.read_config(self.config_manager.config_file).get("hdd_dir", "")
        hdd_dirs = hdd_dir_value.split(",")
        for directory in hdd_dirs:
            self.hdd_dir_listbox.insert(tk.END, directory)

        # Utiliser une Frame pour les boutons Ajouter et Supprimer
        button_frame = tk.Frame(self.input_subframe_6, bg="#1C1C1C")
        button_frame.grid(row=2, column=0, columnspan=2, pady=0, padx=5, sticky="nsew")

        # Ajouter des poids pour partager la largeur entre les boutons
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.add_hdd_dir_button = ttk.Button(button_frame, text=Lang.translate("add"), command=self.plotter_gui.add_hdd_dir)
        self.add_hdd_dir_button.grid(row=0, column=0, pady=0, padx=(0, 2), sticky="nsew")
        self.add_hdd_dir_button.config(cursor="hand2")

        self.remove_hdd_dir_button = ttk.Button(button_frame, text=Lang.translate("remove"), command=self.plotter_gui.remove_hdd_dir)
        self.remove_hdd_dir_button.grid(row=0, column=1, pady=0, padx=(2, 0), sticky="nsew")
        self.remove_hdd_dir_button.config(cursor="hand2")

        # Créer une sous-frame pour carte graphique
        self.input_subframe_7 = tk.Frame(self.input_subframe_6, bg="#1C1C1C")
        self.input_subframe_7.grid(row=7, column=0, columnspan=3, padx=(0, 0), pady=(10, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_7.columnconfigure(0, weight=1)
        self.input_subframe_7.columnconfigure(1, weight=1)
        self.input_subframe_7.columnconfigure(2, weight=1)

        # Ligne 10 : GPU 1
        # Récupération des valeurs des GPU depuis la configuration
        gpu_1_value = str(self.config_manager.read_config(self.config_manager.config_file).get("gpu_1", ""))
        gpu_2_value = str(self.config_manager.read_config(self.config_manager.config_file).get("gpu_2", ""))
        waitforcopy_value = str(self.config_manager.read_config(self.config_manager.config_file).get("waitforcopy", ""))

        self.gpu_1_label = ttk.Label(self.input_subframe_7, style="Custom.TLabel", text=Lang.translate("gpuOne"), anchor="center")
        self.gpu_1_label.grid(row=1, column=0, padx=(0, 0), pady=(5, 0), sticky="n")
        self.gpu_1_value_var = tk.StringVar(value=gpu_1_value)

        # Ajout d'un champ vide au début de la liste
        gpu_values = [""]

        # Liste des valeurs pour le combobox
        self.gpu_1_combobox = ttk.Combobox(self.input_subframe_7, textvariable=self.gpu_1_value_var, values=gpu_values, width=5, state="readonly", background="#cccccc")
        self.gpu_1_combobox.grid(row=2, column=0, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.gpu_1_value_var.set(gpu_1_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.gpu_1_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.gpu_1_config())
        # Associer les fonctions aux événements de survol de la souris
        self.gpu_1_combobox.bind("<Enter>", self.onMouseEnter.gpu_1_info)
        self.gpu_1_combobox.bind("<Leave>", self.onMouseLeave.gpu_1_info)

        # Ligne 10 : GPU 2
        self.gpu_2_label = ttk.Label(self.input_subframe_7, style="Custom.TLabel", text=Lang.translate("gpuTwo"), anchor="center")
        self.gpu_2_label.grid(row=1, column=1, padx=(0, 0), pady=(5, 0), sticky="n")
        self.gpu_2_value_var = tk.StringVar(value=gpu_2_value)

        self.gpu_2_combobox = ttk.Combobox(self.input_subframe_7, textvariable=self.gpu_2_value_var, width=5, state="readonly")
        self.gpu_2_combobox.grid(row=2, column=1, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.gpu_2_value_var.set(gpu_2_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.gpu_2_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.gpu_2_config())
        # Associer les fonctions aux événements de survol de la souris
        self.gpu_2_combobox.bind("<Enter>", self.onMouseEnter.gpu_2_info)
        self.gpu_2_combobox.bind("<Leave>", self.onMouseLeave.gpu_2_info)

        # Ligne 11 : Max number of plots to cache in tmpdir -Q
        self.waitforcopy_label = ttk.Label(self.input_subframe_7, style="Custom.TLabel", text=Lang.translate("w_Flag"), anchor="center")
        self.waitforcopy_label.grid(row=1, column=2, padx=(0, 0), pady=(5, 0), sticky="n")
        self.waitforcopy_var = tk.StringVar(value=waitforcopy_value)

        # Liste des valeurs pour le combobox
        waitforcopy_values = [Lang.translate("on"), Lang.translate("off")]

        self.waitforcopy_combobox = ttk.Combobox(self.input_subframe_7, textvariable=self.waitforcopy_var, values=waitforcopy_values, width=5, state="readonly")
        self.waitforcopy_combobox.grid(row=2, column=2, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.waitforcopy_var.set(waitforcopy_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.waitforcopy_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.waitforcopy_config())
        # Associer les fonctions aux événements de survol de la souris
        self.waitforcopy_combobox.bind("<Enter>", self.onMouseEnter.waitforcopy_info)
        self.waitforcopy_combobox.bind("<Leave>", self.onMouseLeave.waitforcopy_info)

        # Créer une sous-frame pour carte graphique
        self.input_subframe_8 = tk.Frame(self.input_subframe_7, bg="#1C1C1C")
        self.input_subframe_8.grid(row=7, column=0, columnspan=3, padx=0, pady=(0, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        self.input_subframe_8.columnconfigure(0, weight=1)
        self.input_subframe_8.columnconfigure(1, weight=1)
        self.input_subframe_8.columnconfigure(2, weight=1)

        # Récupération des valeurs depuis la configuration
        maxtmp_value = str(self.config_manager.read_config(self.config_manager.config_file).get("maxtmp", ""))
        copylimit_value = str(self.config_manager.read_config(self.config_manager.config_file).get("copylimit", ""))
        maxcopy_value = str(self.config_manager.read_config(self.config_manager.config_file).get("maxcopy", ""))

        # Ligne 11 : Max number of plots to cache in tmpdir -Q
        self.maxtmp_label = ttk.Label(self.input_subframe_8, style="Custom.TLabel", text=Lang.translate("Q_Flag"), anchor="center")
        self.maxtmp_label.grid(row=0, column=0, padx=(0, 0), pady=(5, 0), sticky="n")
        self.maxtmp_var = tk.StringVar(value=maxtmp_value)

        # Liste des valeurs pour le combobox
        maxtmp_values = ["-1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.maxtmp_combobox = ttk.Combobox(self.input_subframe_8, textvariable=self.maxtmp_var, values=maxtmp_values, width=5, state="readonly")
        self.maxtmp_combobox.grid(row=1, column=0, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.maxtmp_var.set(maxtmp_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.maxtmp_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.maxtmp_config())
        # Associer les fonctions aux événements de survol de la souris
        self.maxtmp_combobox.bind("<Enter>", self.onMouseEnter.maxtmp_info)
        self.maxtmp_combobox.bind("<Leave>", self.onMouseLeave.maxtmp_info)

        # Ligne 12 : Max number of parallel copies in total -A
        self.copylimit_label = ttk.Label(self.input_subframe_8, style="Custom.TLabel", text=Lang.translate("A_Flag"), anchor="center")
        self.copylimit_label.grid(row=0, column=1, padx=(0, 0), pady=(5, 0), sticky="n")
        self.copylimit_var = tk.StringVar(value=copylimit_value)

        # Liste des valeurs pour le combobox
        copylimit_values = ["-1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.copylimit_combobox = ttk.Combobox(self.input_subframe_8, textvariable=self.copylimit_var, values=copylimit_values, width=5, state="readonly")
        self.copylimit_combobox.grid(row=1, column=1, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.copylimit_var.set(copylimit_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.copylimit_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.copylimit_config())
        # Associer les fonctions aux événements de survol de la souris
        self.copylimit_combobox.bind("<Enter>", self.onMouseEnter.copylimit_info)
        self.copylimit_combobox.bind("<Leave>", self.onMouseLeave.copylimit_info)

        # Ligne 13 : Max number of parallel copies to same HDD -W
        self.maxcopy_label = ttk.Label(self.input_subframe_8, style="Custom.TLabel", text=Lang.translate("W_Flag"), anchor="center")
        self.maxcopy_label.grid(row=0, column=2, padx=(0, 0), pady=(5, 0), sticky="n")
        self.maxcopy_var = tk.StringVar(value=maxcopy_value)

        # Liste des valeurs pour le combobox
        maxcopy_values = ["-1", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        self.maxcopy_combobox = ttk.Combobox(self.input_subframe_8, textvariable=self.maxcopy_var, values=maxcopy_values, width=5, state="readonly")
        self.maxcopy_combobox.grid(row=1, column=2, padx=(0, 0), pady=(0, 5), sticky="n")
        # Assignation des valeurs corrigées aux combobox
        self.maxcopy_var.set(maxcopy_value)
        # Associez la fonction à l'événement de changement de la combobox
        self.maxcopy_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.updateValues.maxcopy_config())
        # Associer les fonctions aux événements de survol de la souris
        self.maxcopy_combobox.bind("<Enter>", self.onMouseEnter.maxcopy_info)
        self.maxcopy_combobox.bind("<Leave>", self.onMouseLeave.maxcopy_info)

        # Créer une étiquette pour afficher le message
        self.info_label = tk.Label(self.input_subframe_7, text=Lang.translate("advancedOptions"), highlightthickness=1, background="#FF9B00", foreground="#000000")
        self.info_label.grid(row=0, column=0, columnspan=4, padx=(5, 5), pady=(15, 5), sticky="nsew")

        # Mettre à jour les valeurs des combobox des GPU connectés
        self.gpu_combobox_values()

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
        self.start_button = ttk.Button(button_frame, text=Lang.translate("launchCreation"), command=self.plotter_gui.start_plotting, cursor="hand2")
        self.start_button.grid(row=0, column=0, pady=15, padx=5, sticky="nsew")
        self.start_button.configure(style="CustomSend.TButton")

        # Ligne 10 : Bouton Arrêter
        self.stop_button = ttk.Button(button_frame, text=Lang.translate("closeWindow"), command=self.plotter_gui.stop_or_close, cursor="hand2")
        self.stop_button.grid(row=0, column=1, pady=15, padx=5, sticky="nsew")
        self.stop_button.configure(style="CustomSend.TButton")

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

        # Créer un widget pour afficher les messages
        self.message_label = tk.Label(news_plot_frame, text=self.discord.news(), background="#1C1C1C", foreground="#ffffff")
        self.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

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
        error_label = ttk.Label(log_frame, style="Custom.TLabel", text=Lang.translate("errorLogs"), anchor="nw")
        error_label.grid(row=1, column=0, pady=(10, 1), padx=15, sticky="nw")
        error_label.configure(background="#1C1C1C", foreground="#F10000")

        self.errors_text = tk.Text(log_frame, wrap=tk.WORD, height=2, highlightthickness=1, highlightbackground="#565656")
        self.errors_text.grid(row=2, column=0, pady=(0, 5), padx=(15, 0), sticky="nsew")
        self.errors_text.configure(bg="#2C2C2C", fg="#F10000")

        errors_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.errors_text.yview)
        errors_scrollbar.grid(row=2, column=1, pady=(0, 5), padx=(0, 15), sticky="ns")
        self.errors_text["yscrollcommand"] = errors_scrollbar.set
        self.errors_text.tag_configure("timestamp", foreground="#FFFFFF")
        self.errors_text.tag_configure("error", foreground="#F10000")
        self.errors_text.tag_configure("warning", foreground="#FF9B00")
        self.errors_text.tag_configure("info", foreground="#0792ea")

        # Ligne 12 : Journal de l'application
        log_label = ttk.Label(log_frame, style="Custom.TLabel", text=Lang.translate("applicationLogs"), anchor="nw")
        log_label.grid(row=3, column=0, pady=(10, 1), padx=15, sticky="nw")
        log_label.configure(background="#1C1C1C", foreground="#0792ea")

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=13, highlightthickness=1, highlightbackground="#565656")
        self.log_text.grid(row=4, column=0, pady=(0, 5), padx=(15, 0), sticky="nsew")
        self.log_text.configure(bg="#2C2C2C", fg="#00DF03")
        self.log_text.tag_configure("timestamp", foreground="#FFFFFF")
        self.log_text.tag_configure("error", foreground="#F10000")
        self.log_text.tag_configure("warning", foreground="#FF9B00")
        self.log_text.tag_configure("info", foreground="#0792ea")
        self.log_text.tag_configure("welcome", foreground="#FFFFFF")

        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=4, column=1, pady=(0, 5), padx=(0, 15), sticky="ns")
        self.log_text["yscrollcommand"] = log_scrollbar.set

        # Ligne 13 : Journal du plotter
        log_blade_label = ttk.Label(log_frame, style="Custom.TLabel", text=Lang.translate("plotterLogs"), anchor="nw")
        log_blade_label.grid(row=5, column=0, pady=(10, 1), padx=15, sticky="nw")
        log_blade_label.configure(background="#1C1C1C", foreground="#BFBFBF")

        self.log_blade = tk.Text(log_frame, wrap=tk.WORD, height=10, highlightthickness=1, highlightbackground="#565656")
        self.log_blade.grid(row=6, column=0, pady=(0, 15), padx=(15, 0), sticky="nsew")
        self.log_blade.configure(bg="#2C2C2C", fg="#BFBFBF")
        self.log_blade.tag_configure("timestamp", foreground="#FFFFFF")
        self.log_blade.tag_configure("error", foreground="#F10000")
        self.log_blade.tag_configure("warning", foreground="#FF9B00")
        self.log_blade.tag_configure("info", foreground="#0792ea")

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

    def gpu_combobox_values(self):
        # Récupérer les GPUs disponibles sur le système
        available_gpus = GPUtil.getGPUs()

        # Créer une liste pour stocker les valeurs des GPUs connectés
        connected_gpus = []

        # Ajouter les GPUs connectés à la liste
        for gpu in available_gpus:
            connected_gpus.append(str(gpu.id))

        # Mettre à jour les valeurs des combobox avec les GPUs connectés
        self.gpu_1_combobox['values'] = connected_gpus
        self.gpu_2_combobox['values'] = connected_gpus
        self.gpu_connected = connected_gpus

        # Désactiver le combobox GPU 2 si moins de deux GPUs sont connectés
        if len(connected_gpus) < 2:
            self.gpu_2_combobox.configure(state="disabled")
            # Réinitialiser la valeur sélectionnée du deuxième GPU
            self.gpu_2_value_var.set("")
        else:
            self.gpu_2_combobox.configure(state="normal")


class UpdateValues:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.static_method = ff_plotter_gui.static_method

    def contract_config(self):
        selected_contract = self.plotter_gui.interface.contract_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"contract": selected_contract}, self.plotter_gui.interface.config_manager.config_file)

    def farmer_key_config(self):
        selected_farmer_key = self.plotter_gui.interface.farmer_key_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"farmer_key": selected_farmer_key}, self.plotter_gui.interface.config_manager.config_file)

    def compression_config(self):
        selected_compression = self.plotter_gui.interface.compression_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"compression": selected_compression}, self.plotter_gui.interface.config_manager.config_file)

    def gpu_1_config(self):
        selected_gpu_1 = self.plotter_gui.interface.gpu_1_value_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"gpu_1": selected_gpu_1}, self.plotter_gui.interface.config_manager.config_file)

    def gpu_2_config(self):
        selected_gpu_2 = self.plotter_gui.interface.gpu_2_value_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"gpu_2": selected_gpu_2}, self.plotter_gui.interface.config_manager.config_file)

    def waitforcopy_config(self):
        waitforcopy = self.plotter_gui.interface.waitforcopy_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"waitforcopy": waitforcopy}, self.plotter_gui.interface.config_manager.config_file)

    def maxtmp_config(self):
        maxtmp = self.plotter_gui.interface.maxtmp_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"maxtmp": maxtmp}, self.plotter_gui.interface.config_manager.config_file)

    def copylimit_config(self):
        copylimit = self.plotter_gui.interface.copylimit_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"copylimit": copylimit}, self.plotter_gui.interface.config_manager.config_file)

    def maxcopy_config(self):
        maxcopy = self.plotter_gui.interface.maxcopy_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"maxcopy": maxcopy}, self.plotter_gui.interface.config_manager.config_file)

    def ram_config(self):
        selected_ram_qty = self.plotter_gui.interface.ram_qty_var.get()
        # Récupère les variables depuis le fichier de configuration
        plotter_executable = self.plotter_gui.interface.config_manager.read_config(self.plotter_gui.interface.config_manager.config_file).get("plotter_executable")
        # Récupérer le nom sans extension
        plotter_name = os.path.splitext(plotter_executable)[0]

        # Si la mémoire sélectionnée est supérieure ou égale à 256Go, on grise le bouton du disque temporaire 2
        if int(selected_ram_qty) >= 256:
            self.plotter_gui.interface.ssd_temp2move_button.configure(state="disabled")
        else:
            self.plotter_gui.interface.ssd_temp2move_button.configure(state="normal")

        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"ram_qty": selected_ram_qty}, self.plotter_gui.interface.config_manager.config_file)

        # Disque temporaire 2 par défaut
        label_text = Lang.translate("temporaryDisk_2")

        # Modifier le texte du label selon la quantité de RAM sélectionnée
        if plotter_name.startswith("cuda_plot"):
            if int(selected_ram_qty) == 128:
                label_text = Lang.translate("temporaryDisk_2")
            elif int(selected_ram_qty) < 128:
                label_text = Lang.translate("temporaryDisk_3")
        else:
            label_text = Lang.translate("temporaryDisk_2")

        # Mise à jour du texte du label
        self.plotter_gui.interface.ssd_temp2move_label.config(text=label_text)

    def check_plot_value_config(self):
        selected_check_plot_value = self.plotter_gui.interface.check_plot_value_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"check_plot_value": selected_check_plot_value}, self.plotter_gui.interface.config_manager.config_file)

    def check_threshold_config(self):
        selected_check_threshold_value = self.plotter_gui.interface.check_threshold_value_var.get()
        # Mise à jour du fichier de configuration
        self.plotter_gui.interface.config_manager.update_config({"check_threshold_value": selected_check_threshold_value}, self.plotter_gui.interface.config_manager.config_file)


class ButtonSwitch:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.static_method = ff_plotter_gui.static_method

    # Define our switch function
    def logs(self):
        # Determine si l'état est "on" ou "off"
        if self.plotter_gui.logs_status == Lang.translate("on"):
            self.plotter_gui.interface.logging_button.config(image=self.plotter_gui.interface.logging_button_off, background="#1C1C1C")
            self.plotter_gui.interface.logging_label.config(foreground="#F10000")
            self.plotter_gui.logs_status = Lang.translate("off")
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": Lang.translate("off")}, self.plotter_gui.interface.config_manager.config_file)
        else:
            self.plotter_gui.interface.logging_button.config(image=self.plotter_gui.interface.logging_button_on, background="#1C1C1C")
            self.plotter_gui.interface.logging_label.config(foreground="#00DF03")
            self.plotter_gui.logs_status = Lang.translate("on")
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": Lang.translate("on")}, self.plotter_gui.interface.config_manager.config_file)

    # Define our switch function
    def check(self):
        # Récupère le nom du plotter utilisé
        current_plotter = self.plotter_gui.interface.config_manager.read_config(self.plotter_gui.interface.config_manager.config_file).get("plotter_executable")

        if current_plotter is not None:
            current_plotter = os.path.splitext(current_plotter)[0]
        else:
            current_plotter = "unknown"

        if current_plotter.startswith("bladebit"):
            # Determine si l'état est "on" ou "off"
            if self.plotter_gui.check_plot_status == Lang.translate("on"):
                self.plotter_gui.interface.check_button.config(image=self.plotter_gui.interface.check_button_off, background="#1C1C1C")
                self.plotter_gui.interface.check_label.config(foreground="#F10000")
                self.plotter_gui.check_plot_status = Lang.translate("off")
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("off")}, self.plotter_gui.interface.config_manager.config_file)
                # Désactiver la Combobox
                self.plotter_gui.interface.check_button.configure(state="normal")
                self.plotter_gui.interface.check_plot_value_combobox.configure(state="disabled")
                self.plotter_gui.interface.check_threshold_value_combobox.configure(state="disabled")
            else:
                self.plotter_gui.interface.check_button.config(image=self.plotter_gui.interface.check_button_on, background="#1C1C1C")
                self.plotter_gui.interface.check_label.config(foreground="#00DF03")
                self.plotter_gui.check_plot_status = Lang.translate("on")
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("on")}, self.plotter_gui.interface.config_manager.config_file)
                # Activer la Combobox
                self.plotter_gui.interface.check_button.configure(state="normal")
                self.plotter_gui.interface.check_plot_value_combobox.configure(state="normal")
                self.plotter_gui.interface.check_threshold_value_combobox.configure(state="normal")
        else:
            self.plotter_gui.interface.check_button.configure(state="disabled")
            self.plotter_gui.interface.check_plot_value_combobox.configure(state="disabled")
            self.plotter_gui.interface.check_threshold_value_combobox.configure(state="disabled")
            self.plotter_gui.interface.check_button.config(image=self.plotter_gui.interface.check_button_off, background="#1C1C1C")
            self.plotter_gui.interface.check_label.config(foreground="#F10000")
            self.plotter_gui.check_plot_status = Lang.translate("off")
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": Lang.translate("off")}, self.plotter_gui.interface.config_manager.config_file)

    # Define our switch function
    def del_plot(self):
        # Determine si l'état est "on" ou "off"
        if self.plotter_gui.delCompressedPlot_status == Lang.translate("on"):
            self.plotter_gui.interface.delPlot_label.config(foreground="#F10000")
            self.plotter_gui.interface.delPlot_button.config(image=self.plotter_gui.interface.delPlot_button_off, background="#1C1C1C")
            self.plotter_gui.delCompressedPlot_status = Lang.translate("off")
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"delCompressedPlot_status": Lang.translate("off")}, self.plotter_gui.interface.config_manager.config_file)
        else:
            self.plotter_gui.interface.delPlot_button.config(image=self.plotter_gui.interface.delPlot_button_on, background="#1C1C1C")
            self.plotter_gui.interface.delPlot_label.config(foreground="#00DF03")
            self.plotter_gui.delCompressedPlot_status = Lang.translate("on")
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"delCompressedPlot_status": Lang.translate("on")}, self.plotter_gui.interface.config_manager.config_file)


class OnMouseEnter:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.static_method = ff_plotter_gui.static_method

    def maxcopy_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.maxcopy_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.maxcopy_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("numberHddCopy_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def copylimit_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.copylimit_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.copylimit_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("numberParallelCopy_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def maxtmp_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.maxtmp_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.maxtmp_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("numberCachePlots_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def waitforcopy_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.waitforcopy_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.waitforcopy_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("waitForCopy_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def gpu_2_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.gpu_2_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.gpu_2_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("secondGpuID_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def gpu_1_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.gpu_1_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.gpu_1_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("firstGpuID_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def hdd_dir_listbox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.hdd_dir_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.hdd_dir_listbox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("hddDir_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def ssd_temp2move_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.ssd_temp2move_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.ssd_temp2move_entry.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("temp2move_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def ssd_temp_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.ssd_temp_label.configure(foreground="#00DF03")
        self.plotter_gui.interface.ssd_temp_entry.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("temp_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def new_version_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("downloadNewVersion"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def site_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        directory_path = os.path.dirname(os.path.dirname(__file__))
        # Charger une nouvelle image pour le survol de la souris
        hover_logo_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "logo_hover.png"))
        hover_logo_img = tk.PhotoImage(file=hover_logo_path).subsample(1)
        # Assigner l'image de survol au label
        self.plotter_gui.interface.logo_label.configure(image=hover_logo_img)
        # Garder une référence à l'image pour éviter la suppression par le garbage collector
        self.plotter_gui.interface.logo_label.hover_image = hover_logo_img
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.logo_label.configure(background="#1C1C1C", foreground="#0792ea", cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("joinWebsite_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def discord_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        directory_path = os.path.dirname(os.path.dirname(__file__))
        # Charger une nouvelle image pour le survol de la souris
        hover_logo_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "discord_hover.png"))
        hover_logo_img = tk.PhotoImage(file=hover_logo_path).subsample(1)
        # Assigner l'image de survol au label
        self.plotter_gui.interface.logo_label_discord.configure(image=hover_logo_img)
        # Garder une référence à l'image pour éviter la suppression par le garbage collector
        self.plotter_gui.interface.logo_label_discord.hover_image = hover_logo_img
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.logo_label_discord.configure(background="#1C1C1C", foreground="#0792ea", cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("joinDiscord_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def check_threshold_value_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.check_threshold_value_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.check_threshold_value_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("threshold_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def farmer_key_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.farmer_key_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.farmer_key_entry.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("farmerKey_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def contract_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.contract_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.contract_entry.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("contract_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def ram_qty_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.ram_qty_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.ram_qty_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("ram_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def compression_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.compression_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.compression_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("compression_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def check_plot_value_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.check_plot_value_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.check_plot_value_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("checkPlot_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def plotter_path_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.plotter_path_label.configure(cursor="hand2", foreground="#00DF03")
        self.plotter_gui.interface.plotter_path_combobox.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("plotter_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def logging_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.logging_label.configure(cursor="hand2", foreground="#0792ea")
        self.plotter_gui.interface.logging_button.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("logging_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def check_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.check_label.configure(cursor="hand2", foreground="#0792ea")
        self.plotter_gui.interface.check_button.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("checkButton_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")

    def delPlot_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Affiche une main quand on passe la souris sur le lien
        self.plotter_gui.interface.delPlot_label.configure(cursor="hand2", foreground="#0792ea")
        self.plotter_gui.interface.delPlot_button.configure(cursor="hand2")
        # Affiche le message en haut au centre
        self.plotter_gui.interface.message_label.configure(text=Lang.translate("delPlotsButton_help"), highlightthickness=1, background="#0792ea", foreground="#000000")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=0, pady=0, sticky="nsew")


class OnMouseLeave:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.static_method = ff_plotter_gui.static_method
        self.discord = Discord()

    def maxcopy_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.maxcopy_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.maxcopy_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def copylimit_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.copylimit_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.copylimit_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def maxtmp_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.maxtmp_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.maxtmp_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def waitforcopy_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.waitforcopy_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.waitforcopy_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def gpu_2_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.gpu_2_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.gpu_2_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def gpu_1_info(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.gpu_1_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.gpu_1_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def hdd_dir_listbox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.hdd_dir_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.hdd_dir_listbox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def ssd_temp2move_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.ssd_temp2move_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.ssd_temp2move_entry.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def ssd_temp_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.ssd_temp_label.configure(foreground="#0792ea", cursor="arrow")
        self.plotter_gui.interface.ssd_temp_entry.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def new_version_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        self.plotter_gui.interface.title_label.configure(text=Lang.translate("newVersionAvailable").format(latest_version=self.plotter_gui.interface.latest_version), background="#00B34D", foreground="#000000", highlightthickness=0, cursor="arrow")

    def site_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Réaffecter l'image d'origine
        self.plotter_gui.interface.logo_label.configure(image=self.plotter_gui.interface.input_logo_img)
        # Changer les autres propriétés du label après avoir quitté le survol de la souris
        self.plotter_gui.interface.logo_label.configure(background="#1C1C1C", foreground="#BFBFBF", cursor="arrow")
        # Réinitialisation
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def discord_link(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)
        # Réaffecter l'image d'origine
        self.plotter_gui.interface.logo_label_discord.configure(image=self.plotter_gui.interface.input_logo_discord_img)
        # Réinitialisation
        self.plotter_gui.interface.logo_label_discord.configure(background="#1C1C1C", foreground="#BFBFBF", cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def check_threshold_value_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.check_threshold_value_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.check_threshold_value_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def farmer_key_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.farmer_key_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.farmer_key_entry.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def contract_entry(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.contract_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.contract_entry.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def ram_qty_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.ram_qty_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.ram_qty_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def compression_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.compression_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.compression_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def check_plot_value_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.check_plot_value_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.check_plot_value_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def plotter_path_combobox(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        self.plotter_gui.interface.plotter_path_label.config(cursor="arrow", background="#1C1C1C", foreground="#0792ea")
        self.plotter_gui.interface.plotter_path_combobox.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def logging_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        if self.plotter_gui.logs_status == Lang.translate("on"):
            self.plotter_gui.interface.logging_label.config(cursor="arrow", foreground="#00DF03")
        else:
            self.plotter_gui.interface.logging_label.config(cursor="arrow", foreground="#F10000")

        self.plotter_gui.interface.logging_button.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def check_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        if self.plotter_gui.check_plot_status == Lang.translate("on"):
            self.plotter_gui.interface.check_label.config(cursor="arrow", foreground="#00DF03")
        else:
            self.plotter_gui.interface.check_label.config(cursor="arrow", foreground="#F10000")

        self.plotter_gui.interface.check_button.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")

    def delPlot_button(self, event):
        # Accéder aux informations sur l'événement si nécessaire
        print(event)

        # Réinitialisation
        if self.plotter_gui.delCompressedPlot_status == Lang.translate("on"):
            self.plotter_gui.interface.delPlot_label.config(cursor="arrow", foreground="#00DF03")
        else:
            self.plotter_gui.interface.delPlot_label.config(cursor="arrow", foreground="#F10000")

        self.plotter_gui.interface.delPlot_button.configure(cursor="arrow")
        self.plotter_gui.interface.message_label.configure(text=self.discord.news(), highlightthickness=0, background="#1C1C1C", foreground="#ffffff")
        self.plotter_gui.interface.message_label.grid(row=0, column=0, rowspan=3, padx=(5, 5), pady=(5, 5), sticky="nw")
