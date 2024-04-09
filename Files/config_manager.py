# config_manager.py
import os


class ConfigManager:
    # Nom du fichier de configuration
    config_file = "config.txt"
    config_stats = "stats.txt"

    # Chemin du répertoire où est situé le script
    directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plotter_directory = os.path.join(directory_path, "Plotter")

    def __init__(self):
        self.defaults = {
            "compression": "29",
            "ram_qty": "128",
            "plotter_executable": "",
            "plotter_path": self.plotter_directory,
            "ssd_temp": "",
            "ssd_temp2move": "",
            "hdd_dir": "",
            "contract": "",
            "farmer_key": "",
            "progress_status": "on",
            "logs_status": "off",
            "check_plot_status": "off",
            "check_plot_value": "30",
            "check_threshold_value": "80",
            "gpu_1": "0",
            "gpu_2": "",
            "max_tmp_cache": "",
            "parallel_copies": "1",
            "copy_limit": "1"
        }

        self.stats = {
            "total_plot_created": "0",
            "bad_plot_number": "0",
            "deleted_plot_number": "0"
        }

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
