import os

# Chemin du répertoire où est situé le script
directory_path = os.path.dirname(os.path.dirname(__file__))

# Chemin du répertoire contenant les fichiers
repertory = directory_path

# Chemin du script principal
main_script_path = os.path.join(repertory, "main.py")

# Définir les chemins des images en tant que variables
FF_icon_path = os.path.join(repertory, "Images/FF-icon.ico")

# Chemin des fichiers à ajouter
files_to_add = [
    ("Images/FF-icon.ico", "Images/"),
    ("Images/logo.png", "Images/"),
    ("Images/off.png", "Images/"),
    ("Images/on.png", "Images/"),
    ("Plotter/cuda_plot_k32_v3.exe", "Plotter/"),
    ("Plotter/cuda_plot_k32_v3", "Plotter/"),
    ("Plotter/bladebit_cuda.exe", "Plotter/"),
    ("Plotter/bladebit-cuda-v3.1.0-centos-x86-64.tar", "Plotter/"),
    ("Plotter/bladebit-cuda-v3.1.0-ubuntu-arm64.tar", "Plotter/"),
    ("Plotter/bladebit-cuda-v3.1.0-ubuntu-x86-64.tar", "Plotter/"),
    ("Files/config_manager.py", "Files/"),
    ("Files/find_method.py", "Files/"),
    ("Files/initialize_variables.py", "Files/"),
    ("Files/interface.py", "Files/"),
    ("Files/lists.py", "Files/"),
    ("Files/log_queue.py", "Files/"),
    ("Files/none_false_variables.py", "Files/"),
    ("Files/pattern.py", "Files/"),
    ("Files/progress_bar.py", "Files/"),
    ("Files/static_method.py", "Files/"),
    ("Files/welcome.py", "Files/")
]

# Utiliser les variables dans la commande PyInstaller
pyinstaller_cmd = (
    f"pyinstaller --noconfirm --windowed "
    f"--name \"French Farmer Gui\" "
    f"--icon \"{FF_icon_path}\" "
)

# Ajouter les fichiers à la commande PyInstaller
for file_path, dest_dir in files_to_add:
    full_path = os.path.join(repertory, file_path)
    pyinstaller_cmd += f"--add-data \"{full_path};{dest_dir}\" "

# Ajouter le chemin du script principal
pyinstaller_cmd += f"\"{main_script_path}\""

# Exécuter la commande PyInstaller
os.system(pyinstaller_cmd)
