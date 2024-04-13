# find_method.py
import os
import shutil
import psutil
import platform
from Files.translation import Lang


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
                self.queue_logs.log_queue_errors.put(Lang.translate("processIdentifierRetrieval").format(process_name=process_name, e=str(e)))

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
