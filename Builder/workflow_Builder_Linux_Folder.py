import os
import shutil
import subprocess

# Définir le nom de l'exécutable
executable_name = "FF_Gui_Linux"

# Définir le nom du dossier de destination
destination_folder_name = "FF_Gui_Linux_Folder"

# Chemin du répertoire contenant les fichiers
directory_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chemin du script principal
main_script_path = os.path.join(directory_path, "main.py")

# Chemin du répertoire de distribution
dist_path = os.path.join(directory_path, "dist")

# Chemin absolu du fichier .spec
spec_file_path = os.path.join(directory_path, executable_name + ".spec")

# Chemin absolu du dossier de destination
destination_folder_path = os.path.join(dist_path, destination_folder_name)

# Vérifier si le répertoire de destination existe, le créer s'il n'existe pas
if not os.path.exists(destination_folder_path):
    os.makedirs(destination_folder_path)

# Utiliser pyinstaller pour générer le fichier .spec
subprocess.run(
    [
        "pyi-makespec",
        "--windowed",
        "--onedir",
        "--name", executable_name,
        f"--icon={os.path.join(directory_path, 'Images/FF-icon.ico')}",
        "--add-data", f"{os.path.join(directory_path, 'Images/FF-icon.ico')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/logo.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/logo_hover.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/discord.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/discord_hover.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/off.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/on.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/open.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Images/close.png')}:Images",
        "--add-data", f"{os.path.join(directory_path, 'Files/config_manager.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/FF_Team_messages.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/find_method.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/initialize_variables.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/interface.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/lists.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/log_queue.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/none_false_variables.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/pattern.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/progress_bar.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/static_method.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/translation.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/version.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/version.txt')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Files/welcome.py')}:Files",
        "--add-data", f"{os.path.join(directory_path, 'Languages/translations_fr.py')}:Languages",
        "--add-data", f"{os.path.join(directory_path, 'Languages/translations_en.py')}:Languages",
        "--add-data", f"{os.path.join(directory_path, 'Languages/translations_de.py')}:Languages",
        "--add-data", f"{os.path.join(directory_path, 'Builder/System_Auto_Folder_Builder.py')}:Builder",
        "--add-data", f"{os.path.join(directory_path, 'Builder/System_Auto_Standalone_Builder.py')}:Builder",
        "--add-data", f"{os.path.join(directory_path, 'Plotter/cuda_plot_k32')}:Plotter",
        "--add-data", f"{os.path.join(directory_path, 'Plotter/cuda_plot_k32_v3')}:Plotter",
        "--add-data", f"{os.path.join(directory_path, 'Plotter/bladebit-cuda-v3.1.0-centos-x86-64.tar')}:Plotter",
        "--add-data", f"{os.path.join(directory_path, 'Plotter/bladebit-cuda-v3.1.0-ubuntu-x86-64.tar')}:Plotter",
        main_script_path
    ]
)

# Liste des modules externes utilisés dans l'application
external_modules = [
    'certifi',
    'charset-normalizer',
    'GPUtil',
    'idna',
    'PIL',
    'psutil',
    'requests',
    'ttkthemes',
    'setuptools',
    'urllib3',
    'PIL._tkinter_finder'
]

# Ouvrir le fichier .spec en mode lecture
with open(spec_file_path, "r") as spec_file:
    lines = spec_file.readlines()

# Chercher la ligne où se trouve hiddenimports
for i, line in enumerate(lines):
    if line.strip().startswith("hiddenimports="):
        # Extraire les modules cachés existants de la ligne
        modules_line = lines[i].strip().split("=")[1].strip()
        # Initialiser une liste vide si aucun module caché n'est déjà spécifié
        modules_list = [] if not modules_line else modules_line.strip('[]').split(',')
        # Ajouter les modules externes à la liste des hiddenimports
        modules_list.extend(external_modules)
        # Filtrer les éléments vides de la liste
        modules_list = [module.strip() for module in modules_list if module.strip()]
        # Ajouter des guillemets autour de chaque élément de la liste
        modules_str = ', '.join([f"'{module}'" for module in modules_list])
        # Modifier la ligne pour inclure les nouveaux modules cachés
        lines[i] = f"    hiddenimports=[{modules_str}],\n"
        break

# Écrire les modifications dans le fichier .spec
with open(spec_file_path, "w") as spec_file:
    spec_file.writelines(lines)

# Utiliser pyinstaller pour construire l'exécutable à partir du fichier .spec
subprocess.run(["pyinstaller", spec_file_path])

# Déplacer l'exécutable dans le dossier de destination
shutil.move(os.path.join(dist_path, executable_name), os.path.join(destination_folder_path, executable_name))

# Compresser le dossier de destination avec un nom différent
shutil.make_archive(os.path.join(dist_path, destination_folder_name), "gztar", dist_path, destination_folder_name)

# Supprimer les répertoires vides s'ils existent déjà
shutil.rmtree(destination_folder_path, ignore_errors=True)
