# interface.py
import logging
import os
import platform
import tkinter as tk
from tkinter import ttk, Frame

from ttkthemes.themed_style import ThemedStyle

from Files.initialize_variables import InitializeVariables


class HyperlinkLabel(tk.Label):
    def __init__(self, parent, text, url, *args, **kwargs):
        super().__init__(parent, text=text, *args, **kwargs)
        self.url = url
        self.bind("<Button-1>", self.open_link)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def open_link(self, event):
        import webbrowser
        webbrowser.open_new(self.url)

    def on_enter(self, event):
        self.configure(fg="#0792ea", cursor="hand2")

    def on_leave(self, event):
        self.configure(fg="#BFBFBF", cursor="arrow")


class Interface:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.static_method = ff_plotter_gui.static_method

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

        # Récupération de la correspondance
        if current_plotter_name:
            self.root.title(f"French Farmer Gui - {current_plotter_name}")
        else:
            self.root.title("French Farmer Gui")

        # Stylisation avec ttk
        style = ThemedStyle(self.root)
        style.theme_use("clam")
        style.configure("Custom.TLabel", background="#1C1C1C", foreground="#0792ea", font=("Helvetica Sans MS", 10))
        style.configure("TButton", font=("Helvetica", 9))
        style.configure("Custom.Horizontal.TProgressbar", troughcolor="#1C1C1C", background="#00DF03", thickness=10)
        style.configure('CustomSend.TButton', background='#9C9C9C')

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
        self.logging_button.config(cursor="hand2", state="normal")

        # Chargez l'image dans une variable de classe spécifique pour le bouton de logging
        logging_button_off_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "off.png"))
        self.logging_button_off = tk.PhotoImage(file=logging_button_off_path)

        logging_button_on_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "on.png"))
        self.logging_button_on = tk.PhotoImage(file=logging_button_on_path)

        # Configurez le bouton de logging en fonction de la valeur de logs_status
        if self.plotter_gui.logs_status == "on":
            self.logging_button.config(image=self.logging_button_on, background="#1C1C1C")
            self.logging_label.config(foreground="#00B34D")
            self.logging_label.grid_rowconfigure(0, weight=1)
        else:
            self.logging_button.config(image=self.logging_button_off, background="#1C1C1C")
            self.logging_label.config(foreground="#F10000")
            self.logging_label.grid_rowconfigure(0, weight=1)

        # Bouton on / off de plot check
        self.check_label = tk.Label(inner_frame, background="#1C1C1C", border=0, text="Plot Check")
        self.check_label.grid(row=0, column=1, padx=(0, 0), pady=(10, 5), sticky="n")

        self.check_button = tk.Button(inner_frame, border=0, command=self.check_button_switch)
        self.check_button.grid(row=1, column=1, padx=(0, 0), pady=(5, 10), sticky="n")
        self.check_button.configure(background="#1C1C1C", activebackground="#1C1C1C", border=0)
        self.check_button.config(cursor="hand2")

        # Chargez l'image dans une variable de classe spécifique pour le bouton de check
        check_button_off_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "off.png"))
        self.check_button_off = tk.PhotoImage(file=check_button_off_path)

        check_button_on_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "on.png"))
        self.check_button_on = tk.PhotoImage(file=check_button_on_path)

        if current_plotter_name == "bladebit_cuda" or current_plotter_name.startswith("bladebit-cuda"):
            # Configurez le bouton de check en fonction de la valeur de check_plot_status
            if self.plotter_gui.check_plot_status == "on":
                self.check_button.config(image=self.check_button_on, background="#1C1C1C")
                self.check_label.config(foreground="#00B34D")
                # Ajoutez des poids pour partager la hauteur
                self.check_label.grid_rowconfigure(0, weight=1)
            else:
                self.check_button.config(image=self.check_button_off, background="#1C1C1C")
                self.check_label.config(foreground="#F10000")
                # Ajoutez des poids pour partager la hauteur
                self.check_label.grid_rowconfigure(0, weight=1)
        else:
            self.check_button.configure(state="disabled")
            self.check_button.config(image=self.logging_button_off, background="#1C1C1C")
            self.check_label.config(foreground="red")
            self.plotter_gui.check_plot_status = "off"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": "off"}, self.config_manager.config_file)

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

        # Crée un label pour afficher le texte
        site_link_label = HyperlinkLabel(news_plot_frame, text="Site web: https://xch.ffarmers.eu", bg="#1C1C1C", fg="#BFBFBF", anchor="w", url="https://xch.ffarmers.eu")
        site_link_label.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        discord_link_label = HyperlinkLabel(news_plot_frame, text="Discord: https://discord.gg/xgGhcS2jyq", bg="#1C1C1C", fg="#BFBFBF", anchor="w", url="https://discord.gg/xgGhcS2jyq")
        discord_link_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 0), sticky="w")

        # Ajoutez le numéro du plot en cours
        self.news_text = tk.Label(news_plot_frame, text="     ", bg="#1C1C1C", fg="#1C1C1C")
        self.news_text.grid(row=2, column=0, padx=(10, 0), pady=(0, 0), sticky="w", columnspan=2)

        # Ajoutez des poids pour partager la hauteur
        news_plot_frame.grid_rowconfigure(0, weight=1)
        news_plot_frame.grid_rowconfigure(1, weight=1)
        # Ajoutez des poids pour partager la largeur
        news_plot_frame.grid_columnconfigure(0, weight=1)

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
        logo_path = self.static_method.resource_path(os.path.join(directory_path, "Images", "logo.png"))
        input_logo_img = tk.PhotoImage(file=logo_path)

        # Créez un label pour afficher l'image
        logo_label = ttk.Label(input_logo, image=input_logo_img, background="#1C1C1C", anchor="center")
        logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 10), padx=(0, 0), sticky="n")
        # Ajoutez des poids pour partager la hauteur
        logo_label.grid_rowconfigure(0, weight=1)

        # Assurez-vous que l'image ne soit pas collectée par le garbage collector
        logo_label.photo = input_logo_img

        # Créer une sous-frame pour plotter_path
        input_subframe_1 = tk.Frame(input_logo, bg="#1C1C1C")
        input_subframe_1.grid(row=1, column=0, columnspan=2, padx=(0, 0), pady=(0, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_1.columnconfigure(0, weight=1)
        input_subframe_1.columnconfigure(1, weight=1)

        # Ligne 5 : Chemin vers l'exécutable de plotter
        self.plotter_path_label = ttk.Label(input_subframe_1, style="Custom.TLabel", text="Sélectionner le plotter", anchor="center")
        self.plotter_path_label.grid(row=0, column=0, pady=(0, 5), padx=4, sticky="nsew", columnspan=2)

        # Créer une liste déroulante avec les exécutables disponibles
        self.plotter_path_combobox = ttk.Combobox(input_subframe_1, values=available_executables)
        self.plotter_path_combobox.grid(row=1, column=0, pady=(0, 0), padx=4, sticky="nsew", columnspan=2)
        self.plotter_path_combobox.bind("<<ComboboxSelected>>", self.plotter_gui.on_combobox_selected)
        self.plotter_path_combobox.set(current_plotter)

        # Créer une sous-frame pour check_plot
        input_subframe_2 = tk.Frame(input_subframe_1, bg="#1C1C1C")
        input_subframe_2.grid(row=2, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="n")

        # Ajouter des poids pour partager la largeur
        input_subframe_2.columnconfigure(0, weight=1)
        input_subframe_2.columnconfigure(1, weight=1)

        # Ligne 3 : check_plot
        self.check_plot_value_label = ttk.Label(input_subframe_2, style="Custom.TLabel", text="Nombre de contrôles", anchor="center")
        self.check_plot_value_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        check_plot_value = self.config_manager.read_config(self.config_manager.config_file).get("check_plot_value")
        self.check_plot_value_var = tk.StringVar(value=check_plot_value)

        self.check_plot_value_combobox = ttk.Combobox(input_subframe_2, textvariable=self.check_plot_value_var)
        self.check_plot_value_combobox.grid(row=1, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_plot_value_combobox['values'] = ["30", "60", "100", "300", "500", "700", "1000"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_plot_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_check_plot_value_config())

        # Ligne 4 : check_threshold
        self.check_threshold_value_label = ttk.Label(input_subframe_2, style="Custom.TLabel", text="Taux de preuve en %", anchor="center")
        self.check_threshold_value_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        check_threshold_value = self.config_manager.read_config(self.config_manager.config_file).get("check_threshold_value")
        self.check_threshold_value_var = tk.StringVar(value=check_threshold_value)
        self.check_threshold_value_combobox = ttk.Combobox(input_subframe_2, textvariable=self.check_threshold_value_var)
        self.check_threshold_value_combobox.grid(row=1, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.check_threshold_value_combobox['values'] = ["80", "85", "90", "95", "100"]
        # Associez la fonction à l'événement de changement de la combobox
        self.check_threshold_value_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_check_threshold_config())

        if current_plotter_name == "bladebit_cuda" or current_plotter_name.startswith("bladebit-cuda"):
            # Configurez le combobox de check en fonction de la valeur de check_plot_status
            if self.plotter_gui.check_plot_status == "on":
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
        input_subframe_3: Frame = tk.Frame(input_subframe_2, bg="#1C1C1C")
        input_subframe_3.grid(row=3, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="n")

        # Ajouter des poids pour partager la largeur
        input_subframe_3.columnconfigure(0, weight=1)
        input_subframe_3.columnconfigure(1, weight=1)

        # Ligne 1 : Taux de compression du plot
        self.compression_label = ttk.Label(input_subframe_3, style="Custom.TLabel", text="Taux de compression", anchor="center")
        self.compression_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Récupérez les valeurs de compression à partir de InitializeVariables.plotSizes
        current_compression = self.config_manager.read_config(self.config_manager.config_file).get("compression")

        # S'assurer que compress est une chaîne ou None
        if current_compression is not None:
            current_compression = str(current_compression)

        if current_plotter_name == "bladebit_cuda" or current_plotter_name.startswith("bladebit-cuda"):
            # Si le plotter est bladebit, n'afficher que les compressions de 1 à 7
            compression_values = [str(compression) for compression in range(1, 8)]
            # Si la compression est supérieur à 9, on assigne 5 par défaut
            compression = min(int(current_compression), 5) if current_compression and current_compression.isdigit() else 5
            # Mise à jour du fichier de configuration
            self.config_manager.update_config({"compression": compression}, self.config_manager.config_file)
            ram_qty_values = ["16", "128", "256"]
        else:
            # Sinon, utilisez toutes les compressions disponibles
            compression_values = [str(compression) for compression in InitializeVariables().plotSizes.keys()]
            compression = int(current_compression) if current_compression is not None else None
            ram_qty_values = ["16", "32", "64", "128", "256", "512"]

        self.compression_var = tk.StringVar(value=compression)
        self.compression_combobox = ttk.Combobox(input_subframe_3, textvariable=self.compression_var)
        self.compression_combobox.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.compression_combobox['values'] = compression_values
        # Associez la fonction à l'événement de changement de la combobox
        self.compression_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_compression_config())

        # Ligne 2 : Quantité de RAM
        current_ram_qty = self.config_manager.read_config(self.config_manager.config_file).get("ram_qty")
        self.ram_qty_label = ttk.Label(input_subframe_3, style="Custom.TLabel", text="Quantité de RAM", anchor="center")
        self.ram_qty_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")
        self.ram_qty_var = tk.StringVar(value=current_ram_qty)
        self.ram_qty_combobox = ttk.Combobox(input_subframe_3, textvariable=self.ram_qty_var, values=ram_qty_values)
        self.ram_qty_combobox.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")
        # Associez la fonction à l'événement de changement de la combobox
        self.ram_qty_combobox.bind("<<ComboboxSelected>>", lambda event=None: self.update_ram_config())

        # Créer une sous-frame pour compression_label, ram_qty_label
        input_subframe_4 = tk.Frame(input_subframe_3, bg="#1C1C1C")
        input_subframe_4.grid(row=4, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_4.columnconfigure(0, weight=1)
        input_subframe_4.columnconfigure(1, weight=1)

        # Ligne 3 : Pool contract
        self.contract_label = ttk.Label(input_subframe_4, style="Custom.TLabel", text="Pool contract", anchor="center")
        self.contract_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle du contrat de pool
        current_contract_key = self.config_manager.read_config(self.config_manager.config_file).get("contract")
        self.contract_var = tk.StringVar(value=current_contract_key)
        self.contract_entry = ttk.Entry(input_subframe_4, textvariable=self.contract_var)
        self.contract_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.contract_entry.bind("<FocusOut>", lambda event=None: self.update_contract_config())

        # Ligne 4 : Farmer public key
        self.farmer_key_label = ttk.Label(input_subframe_4, style="Custom.TLabel", text="Farmer public key", anchor="center")
        self.farmer_key_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        # Créez une variable pour stocker la valeur actuelle de la clé du fermier
        current_farmer_key = self.config_manager.read_config(self.config_manager.config_file).get("farmer_key")
        self.farmer_key_var = tk.StringVar(value=current_farmer_key)
        self.farmer_key_entry = ttk.Entry(input_subframe_4, textvariable=self.farmer_key_var)
        self.farmer_key_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew", columnspan=2)

        # Associez la fonction à l'événement de modification du champ d'entrée
        self.farmer_key_entry.bind("<FocusOut>", lambda event=None: self.update_farmer_key_config())

        # Créer une sous-frame pour ssd_temp et ssd_temp2move
        input_subframe_5 = tk.Frame(input_subframe_4, bg="#1C1C1C")
        input_subframe_5.grid(row=5, column=0, columnspan=2, padx=(0, 0), pady=(20, 0), sticky="nsew")

        # Ajouter des poids pour partager la largeur
        input_subframe_5.columnconfigure(0, weight=1)
        input_subframe_5.columnconfigure(1, weight=1)

        # Ligne 6 : Disque temporaire -t1 (nvme/ssd)
        self.ssd_temp_label = ttk.Label(input_subframe_5, style="Custom.TLabel", text="Disque temporaire -t1", anchor="center")
        self.ssd_temp_label.grid(row=0, column=0, pady=(0, 5), padx=(5, 5), sticky="nsew")

        self.ssd_temp_entry = ttk.Entry(input_subframe_5)
        self.ssd_temp_entry.grid(row=1, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp")
        if ssd_temp_value is None or ssd_temp_value == "":
            ssd_temp_value = self.config_manager.defaults["ssd_temp"]

        self.ssd_temp_entry.insert(0, ssd_temp_value)

        self.ssd_temp_button = ttk.Button(input_subframe_5, text="Parcourir", command=self.plotter_gui.browse_ssd_temp)
        self.ssd_temp_button.grid(row=2, column=0, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp_button.config(cursor="hand2")

        # Ligne 7 : Disque temporaire 2 -t2 (nvme/ssd/hdd - Non obligatoire)
        self.ssd_temp2move_label = ttk.Label(input_subframe_5, style="Custom.TLabel", text="Disque temporaire -t2", anchor="center")
        self.ssd_temp2move_label.grid(row=0, column=1, pady=(0, 5), padx=(5, 5), sticky="nsew")

        self.ssd_temp2move_entry = ttk.Entry(input_subframe_5)
        self.ssd_temp2move_entry.grid(row=1, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")

        ssd_temp2move_value = self.config_manager.read_config(self.config_manager.config_file).get("ssd_temp2move")
        if not ssd_temp2move_value:
            ssd_temp2move_value = self.config_manager.defaults["ssd_temp2move"]

        self.ssd_temp2move_entry.insert(0, ssd_temp2move_value)

        self.ssd_temp2move_button = ttk.Button(input_subframe_5, text="Parcourir", command=self.plotter_gui.browse_ssd_temp2move)
        self.ssd_temp2move_button.grid(row=2, column=1, pady=(0, 0), padx=(5, 5), sticky="nsew")
        self.ssd_temp2move_button.config(cursor="hand2")
        if int(current_ram_qty) >= 256:
            self.ssd_temp2move_button.configure(state="disabled")

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
        self.start_button.configure(style="CustomSend.TButton")

        # Ligne 10 : Bouton Arrêter
        self.stop_button = ttk.Button(button_frame, text="Fermer la fenêtre", command=self.plotter_gui.stop_or_close, cursor="hand2")
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
        error_label.configure(background="#1C1C1C", foreground="#F10000")

        self.errors_text = tk.Text(log_frame, wrap=tk.WORD, height=5, highlightthickness=1, highlightbackground="#565656")
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
        log_label = ttk.Label(log_frame, style="Custom.TLabel", text="Journal de l'application:", anchor="nw")
        log_label.grid(row=3, column=0, pady=(10, 1), padx=15, sticky="nw")
        log_label.configure(background="#1C1C1C", foreground="#0792ea")

        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10, highlightthickness=1, highlightbackground="#565656")
        self.log_text.grid(row=4, column=0, pady=(0, 5), padx=(15, 0), sticky="nsew")
        self.log_text.configure(bg="#2C2C2C", fg="#00DF03")
        self.log_text.tag_configure("timestamp", foreground="#FFFFFF")
        self.log_text.tag_configure("error", foreground="#F10000")
        self.log_text.tag_configure("warning", foreground="#FF9B00")
        self.log_text.tag_configure("info", foreground="#0792ea")

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
        # Si la mémoire sélectionnée est supérieur à 128Go, on grise le bouton du disque temporaire 2
        if int(selected_ram_qty) >= 256:
            self.ssd_temp2move_button.configure(state="disabled")
        else:
            self.ssd_temp2move_button.configure(state="normal")
        # Mise à jour du fichier de configuration
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

            self.logging_button.config(image=self.logging_button_off, background="#1C1C1C")
            self.logging_label.config(foreground="#F10000")
            self.plotter_gui.logs_status = "off"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": "off"}, self.config_manager.config_file)
        else:
            # Activer la journalisation à un niveau spécifique (par exemple, INFO)
            self.plotter_gui.logger.setLevel(logging.INFO)

            self.logging_button.config(image=self.logging_button_on, background="#1C1C1C")
            self.logging_label.config(foreground="#00DF03")
            self.plotter_gui.logs_status = "on"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"logs_status": "on"}, self.config_manager.config_file)

    # Define our switch function
    def check_button_switch(self):
        # Récupère le nom du plotter utilisé
        current_plotter = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")

        if current_plotter is not None:
            current_plotter = os.path.splitext(current_plotter)[0]
        else:
            current_plotter = "unknown"

        if current_plotter == "bladebit_cuda" or current_plotter.startswith("bladebit-cuda"):
            # Determine si l'état est "on" ou "off"
            if self.plotter_gui.check_plot_status == "on":
                self.check_button.config(image=self.logging_button_off, background="#1C1C1C")
                self.check_label.config(foreground="#F10000")
                self.plotter_gui.check_plot_status = "off"
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": "off"}, self.config_manager.config_file)
                # Désactiver la Combobox
                self.check_button.configure(state="normal")
                self.check_plot_value_combobox.configure(state="disabled")
                self.check_threshold_value_combobox.configure(state="disabled")
            else:
                self.check_button.config(image=self.logging_button_on, background="#1C1C1C")
                self.check_label.config(foreground="#00DF03")
                self.plotter_gui.check_plot_status = "on"
                # Mise à jour du fichier de configuration
                self.plotter_gui.config_manager.update_config({"check_plot_status": "on"}, self.config_manager.config_file)
                # Activer la Combobox
                self.check_button.configure(state="normal")
                self.check_plot_value_combobox.configure(state="normal")
                self.check_threshold_value_combobox.configure(state="normal")
        else:
            self.check_button.configure(state="disabled")
            self.check_button.config(image=self.logging_button_off, background="#1C1C1C")
            self.check_label.config(foreground="#F10000")
            self.plotter_gui.check_plot_status = "off"
            # Mise à jour du fichier de configuration
            self.plotter_gui.config_manager.update_config({"check_plot_status": "off"}, self.config_manager.config_file)
            self.check_plot_value_combobox.configure(state="disabled")
            self.check_threshold_value_combobox.configure(state="disabled")
