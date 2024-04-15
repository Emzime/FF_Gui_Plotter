# FF_Team_messages.py
import threading
import requests
import time
import tkinter as tk


class FFteam:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.last_message = None
        self.team_message_thread = False

    @staticmethod
    def messages():
        # Appel de la fonction pour récupérer le contenu du fichier Markdown
        return FFteam.get_markdown_from_github()

    @staticmethod
    def get_markdown_from_github():
        # URL du fichier Markdown sur GitHub
        github_url = 'https://gui-plotter.ffarmers.eu/FFteam_message.md'

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

    def check_message_change(self):
        # Boucle jusqu'à ce que team_message_thread soit False
        while self.team_message_thread:
            # Récupérer le nouveau message
            new_message = self.messages()

            # Comparer avec le dernier message enregistré
            if new_message != self.last_message:
                # Mettre à jour le dernier message enregistré
                self.last_message = new_message
                # Efface l'ancien message
                self.plotter_gui.interface.message_text.delete("1.0", tk.END)
                # Affiche le nouveau message
                self.plotter_gui.interface.message_text.insert("1.0", new_message)

                # Changer la couleur de fond de la zone de message
                self.plotter_gui.interface.news_plot_frame.config(bg="#00DF03")
                self.plotter_gui.interface.message_text.config(bg="#00DF03", fg="#000000")
                self.plotter_gui.interface.expand_text_label.config(background="#00DF03", foreground="#000000")
                self.plotter_gui.interface.expand_button.config(background="#00DF03")

                # Attendre un certain temps avant de réinitialiser la couleur
                self.plotter_gui.interface.news_plot_frame.after(2000, lambda: self.plotter_gui.interface.news_plot_frame.config(bg="#1C1C1C"))
                self.plotter_gui.interface.message_text.after(2000, lambda: self.plotter_gui.interface.message_text.config(bg="#1C1C1C", fg="#0792ea"))
                self.plotter_gui.interface.expand_text_label.after(2000, lambda: self.plotter_gui.interface.expand_text_label.config(background="#1C1C1C", foreground="#0792ea"))
                self.plotter_gui.interface.expand_button.after(2000, lambda: self.plotter_gui.interface.expand_button.config(background="#1C1C1C"))

            # Attendre un certain temps avant de vérifier à nouveau
            time.sleep(30)

    def start_checking(self):
        # Lancer la vérification du changement de message dans un thread séparé
        self.team_message_thread = threading.Thread(target=self.check_message_change)
        # Le thread se terminera lorsque le programme principal se terminera
        self.team_message_thread.daemon = True
        self.team_message_thread.start()

    def stop_checking(self):
        # Démarrer le thread d'arrêt du processus de manière asynchrone
        self.team_message_thread.daemon = False
