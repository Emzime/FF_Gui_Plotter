# System_Auto_Folder_Builder.py
import os


def build_executable():
    # Chemin du répertoire contenant les fichiers
    directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Chemin du script principal
    main_script_path = os.path.join(directory_path, "main.py")

    # Définir les chemins des images en tant que variables
    FF_icon_path = os.path.join(directory_path, "Images/FF-icon.ico")

    # Initialisation
    files_to_add = None
    separator = None

    # Chemin des fichiers à ajouter (pour Windows)
    files_to_add_windows = [
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
        ("Files/static_method.py", "Files/"),
        ("Files/translation.py", "Files/"),
        ("Files/version.py", "Files/"),
        ("Files/version.txt", "Files/"),
        ("Files/welcome.py", "Files/"),
        ("Languages/translations_fr_FR.py", "Languages/"),
        ("Languages/translations_en_US.py", "Languages/"),
        ("Builder/System_Auto_Folder_Builder.py", "Builder/"),
        ("Builder/System_Auto_Standalone_Builder.py", "Builder/"),
        ("Plotter/cuda_plot_k32.exe", "Plotter/"),
        ("Plotter/cuda_plot_k32_v3.exe", "Plotter/"),
        ("Plotter/bladebit_cuda.exe", "Plotter/")
    ]

    # Chemin des fichiers à ajouter (pour Linux)
    files_to_add_linux = [
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
        ("Files/static_method.py", "Files/"),
        ("Files/translation.py", "Files/"),
        ("Files/version.py", "Files/"),
        ("Files/version.txt", "Files/"),
        ("Files/welcome.py", "Files/"),
        ("Languages/translations_fr_FR.py", "Languages/"),
        ("Languages/translations_en_US.py", "Languages/"),
        ("Builder/System_Auto_Folder_Builder.py", "Builder/"),
        ("Builder/System_Auto_Standalone_Builder.py", "Builder/"),
        ("Builder/linux_build.sh", "Builder/"),
        ("Plotter/cuda_plot_k32", "Plotter/"),
        ("Plotter/cuda_plot_k32_v3", "Plotter/"),
        ("Plotter/bladebit-cuda-v3.1.0-centos-x86-64.tar", "Plotter/"),
        ("Plotter/bladebit-cuda-v3.1.0-ubuntu-x86-64.tar", "Plotter/")
    ]

    # Utiliser les variables dans la commande PyInstaller
    pyinstaller_cmd = (
        f"pyinstaller --noconfirm --windowed "
        f"--name \"French Farmer Gui\" "
        f"--icon \"{FF_icon_path}\" "
    )

    # Ajouter les fichiers à la commande PyInstaller
    if os.name == "nt":  # Windows
        files_to_add = files_to_add_windows
        separator = ";"
    elif os.name == "posix":  # Linux
        files_to_add = files_to_add_linux
        separator = ":"

    for file_path, dest_dir in files_to_add:
        full_path = os.path.join(directory_path, file_path)
        pyinstaller_cmd += f"--add-data \"{full_path}{separator}{dest_dir}\" "

    # Ajouter le chemin du script principal
    pyinstaller_cmd += f"\"{main_script_path}\""

    # Exécuter la commande PyInstaller
    os.system(pyinstaller_cmd)


# Utilisation de la fonction pour créer l'exécutable approprié pour le système
build_executable()
