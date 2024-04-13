# FF_Team_messages.py
import requests


class FFteam:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui

    @staticmethod
    def messages():
        # Appel de la fonction pour récupérer le contenu du fichier Markdown
        return FFteam.get_markdown_from_github()

    @staticmethod
    def get_markdown_from_github():
        # URL du fichier Markdown sur GitHub
        github_url = 'https://raw.githubusercontent.com/Emzime/FF_Gui_Plotter/main/Files/FFteam_message.md'

        try:
            # Effectuer une requête GET pour récupérer le contenu du fichier Markdown
            response = requests.get(github_url)
            # Lever une exception en cas d'erreur HTTP
            response.raise_for_status()
            # Contenu du fichier
            markdown_content = response.text
            return markdown_content

        except requests.exceptions.RequestException as e:
            # Gérer les erreurs de requête
            print("Error fetching Markdown content:", e)
            return None
