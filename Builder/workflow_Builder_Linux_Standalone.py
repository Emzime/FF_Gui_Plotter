import os

# Chemin du répertoire contenant les fichiers
directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Définir le nom de l'exécutable
executable_name = "FF_Gui_Linux_Standalone"

# Chemin du script principal
main_script_path = os.path.join(directory_path, "main.py")

# Chemin des fichiers à ajouter (pour Linux)
files_to_add = [
    ("Images/FF-icon.ico", "Images/"),
    ("Images/logo.png", "Images/"),
    ("Images/logo_hover.png", "Images/"),
    ("Images/discord.png", "Images/"),
    ("Images/discord_hover.png", "Images/"),
    ("Images/off.png", "Images/"),
    ("Images/on.png", "Images/"),
    ("Images/open.png", "Images/"),
    ("Images/close.png", "Images/"),
    ("Files/config_manager.py", "Files/"),
    ("Files/FF_Team_messages.py", "Files/"),
    ("Files/find_method.py", "Files/"),
    ("Files/initialize_variables.py", "Files/"),
    ("Files/interface.py", "Files/"),
    ("Files/lists.py", "Files/"),
    ("Files/log_queue.py", "Files/"),
    ("Files/none_false_variables.py", "Files/"),
    ("Files/pattern.py", "Files/"),
    ("Files/progress_bar.py", "Files/"),
    ("Files/translation.py", "Files/"),
    ("Files/version.py", "Files/"),
    ("Files/version.txt", "Files/"),
    ("Files/welcome.py", "Files/"),
    ("Languages/translations_fr.py", "Languages/"),
    ("Languages/translations_en.py", "Languages/"),
    ("Languages/translations_de.py", "Languages/"),
    ("Builder/System_Auto_Folder_Builder.py", "Builder/"),
    ("Builder/System_Auto_Standalone_Builder.py", "Builder/"),
    ("Plotter/cuda_plot_k32", "Plotter/"),
    ("Plotter/cuda_plot_k32_v3", "Plotter/"),
    ("Plotter/bladebit-cuda-v3.1.0-centos-x86-64.tar", "Plotter/"),
    ("Plotter/bladebit-cuda-v3.1.0-ubuntu-x86-64.tar", "Plotter/")
]

# Utiliser les variables dans la commande PyInstaller
pyinstaller_cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    f"--name={executable_name}",
    "--hidden-import=PIL._tkinter_finder",
    f"--icon={os.path.join(directory_path, 'Images/FF-icon.ico')}"
]

# Ajouter les fichiers à la commande PyInstaller
for file_path, dest_dir in files_to_add:
    full_path = os.path.join(directory_path, file_path)
    pyinstaller_cmd += ["--add-data", f"{full_path}:{dest_dir}"]

# Ajouter le chemin du script principal
pyinstaller_cmd.append(main_script_path)

# Exécuter la commande PyInstaller
os.system(" ".join(pyinstaller_cmd))
