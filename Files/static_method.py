# static_method.py
import os
import sys
import logging


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
