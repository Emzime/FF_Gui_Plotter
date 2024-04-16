# version.py
import os
import requests
import time
from datetime import datetime

from Files.config_manager import ConfigManager
from Files.log_queue import LogQueue
from Files.translation import Lang


class CheckVersion:
    def __init__(self):
        # Création des instances
        self.queue_logs = LogQueue()
        self.config_manager = ConfigManager()

    def check_new_package_version(self):
        # Vérifier si une vérification a déjà été effectuée aujourd'hui
        if not self.is_daily_check_needed():
            return None, None

        try:
            # URL de l'API GitHub
            github_api = "https://api.github.com/repos/Emzime/FF_Gui_Plotter/releases/latest"

            # Récupérer le contenu
            response = requests.get(github_api)
            json_data = response.json()

            # Obtenir la version depuis GitHub
            tag_id = json_data['tag_name']
        except RecursionError:
            # Gestion de l'erreur de dépassement de profondeur de récursion
            self.queue_logs.log_queue_errors.put(Lang.translate("githubResponseError"))
            return None, None

        # Répertoire du script en cours d'exécution
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Chemin du fichier de version
        version_file_path = os.path.join(script_dir, "version.txt")

        # Si le fichier de version n'existe pas
        if not os.path.exists(version_file_path):
            self.queue_logs.log_queue_errors.put(Lang.translate("versionNotFound").format(version=version_file_path))
            time.sleep(2)  # Pause

        # Obtenir la version actuelle
        with open(version_file_path, 'r') as file:
            current_id = file.read().strip()
            # debug
            print(Lang.translate("currentVersion").format(current_version=current_id))

        # Mettre à jour la date de la dernière vérification
        self.update_last_check_date()

        return current_id, tag_id

    def is_daily_check_needed(self):
        # Obtenir la date de la dernière vérification
        last_check_date = self.get_last_check_date()

        # Obtenir la date actuelle
        today_date = datetime.now().date()

        # Vérifier si une journée s'est écoulée depuis la dernière vérification
        return last_check_date != today_date

    def get_last_check_date(self):
        # Récupère la valeur actuelle dans le fichier de configuration
        return self.config_manager.read_config(self.config_manager.config_stats).get("last_check_date")

    def update_last_check_date(self):
        # Mise à jour du fichier de configuration
        self.config_manager.update_config({"last_check_date": datetime.now().date()}, self.config_manager.config_file)
