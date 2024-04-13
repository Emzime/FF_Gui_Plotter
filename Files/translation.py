# translation.py
import os
import locale

# Répertoire des fichiers de traduction
translation_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Languages")

# Obtenez la langue par défaut du système
lang, _ = locale.getdefaultlocale()

# Construisez dynamiquement le chemin du fichier de traduction en fonction de la langue
translation_file = os.path.join(translation_dir, f"translations_{lang}.py")

# Importez le module de traduction correspondant
try:
    translations_module = __import__(f"Languages.translations_{lang}", fromlist=['translations'])
except ImportError:
    # Si le fichier de traduction pour la langue spécifiée n'existe pas, utilisez le fichier par défaut (en anglais par exemple)
    translations_module = __import__("Languages.translations_en_US", fromlist=['translations'])

# Accédez au dictionnaire de traductions
translations = translations_module.translations


class Lang:
    @staticmethod
    def translate(text):
        # Renvoie la traduction correspondante si elle existe, sinon renvoie le texte d'origine
        return translations.get(text, text)

# Exemple d'utilisation
# from Files.translation import Lang
# translated_text = Lang.translate("badProofPercent")
# print(translated_text)
