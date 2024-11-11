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
    def internet_available():
        """Checks if there is an Internet connection by pinging a reliable server."""
        try:
            # Send a request to a reliable site
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def messages():
        """Fetches the Markdown content from GitHub if Internet is available."""
        if FFteam.internet_available():
            return FFteam.get_markdown_from_github()
        else:
            print("No Internet connection. Cannot fetch messages.")
            return None

    @staticmethod
    def get_markdown_from_github():
        """Fetches Markdown content from GitHub."""
        github_url = 'https://gui-plotter.ffarmers.eu/FFteam_message.md'

        try:
            # Attempt to retrieve the Markdown file content
            response = requests.get(github_url)
            response.raise_for_status()
            markdown_content = response.text
            return markdown_content

        except requests.exceptions.RequestException as e:
            # Handle request errors
            print("Error fetching Markdown content:", e)
            return None

    def check_message_change(self):
        """Periodically checks for updates in the message if Internet is available."""
        while self.team_message_thread:
            # Retrieve the new message
            new_message = self.messages()

            # Check if the message has changed
            if new_message != self.last_message and new_message is not None:
                # Update the last saved message
                self.last_message = new_message
                # Clear the old message
                self.plotter_gui.interface.message_text.delete("1.0", tk.END)
                # Display the new message
                self.plotter_gui.interface.message_text.insert("1.0", new_message)

                # Update the background color to indicate a new message
                self.plotter_gui.interface.news_plot_frame.config(bg="#00DF03")
                self.plotter_gui.interface.message_text.config(bg="#00DF03", fg="#000000")
                self.plotter_gui.interface.expand_text_label.config(background="#00DF03", foreground="#000000")
                self.plotter_gui.interface.expand_button.config(background="#00DF03")

                # Reset colors after 2 seconds
                self.plotter_gui.interface.news_plot_frame.after(2000, lambda: self.plotter_gui.interface.news_plot_frame.config(bg="#1C1C1C"))
                self.plotter_gui.interface.message_text.after(2000, lambda: self.plotter_gui.interface.message_text.config(bg="#1C1C1C", fg="#0792ea"))
                self.plotter_gui.interface.expand_text_label.after(2000, lambda: self.plotter_gui.interface.expand_text_label.config(background="#1C1C1C", foreground="#0792ea"))
                self.plotter_gui.interface.expand_button.after(2000, lambda: self.plotter_gui.interface.expand_button.config(background="#1C1C1C"))

            # Wait before checking again
            time.sleep(30)

    def start_checking(self):
        """Starts the message change checking process in a separate thread."""
        self.team_message_thread = threading.Thread(target=self.check_message_change)
        self.team_message_thread.daemon = True
        self.team_message_thread.start()

    def stop_checking(self):
        """Stops the message change checking process."""
        self.team_message_thread.daemon = False
