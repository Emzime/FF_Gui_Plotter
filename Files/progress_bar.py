# progress_bar.py
import re
import time


class ProgressBar:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.config_manager = ff_plotter_gui.config_manager
        self.initialize_variables = ff_plotter_gui.initialize_variables
        self.none_false_variable = ff_plotter_gui.none_false_variable
        self.static_method = ff_plotter_gui.static_method
        self.lists = ff_plotter_gui.lists
        self.pattern = ff_plotter_gui.pattern
        self.queue_logs = ff_plotter_gui.queue_logs
        self.interface = ff_plotter_gui.interface

    def plots_progress(self):
        try:
            # Calcul le nombre d'étapes
            total_steps = len(self.lists.progress_steps)

            while not self.none_false_variable.stop_creation:
                # Boucle sur les lignes de logs
                for line in self.lists.output_lines:
                    # Détection du début d'un nouveau plot
                    current_plot_pattern_match = self.pattern.currentPlotPattern.search(line)
                    if current_plot_pattern_match:
                        requested_pattern_match = current_plot_pattern_match.group(1)
                        if requested_pattern_match is not None:
                            new_plot_number = int(requested_pattern_match)
                            if new_plot_number > self.initialize_variables.current_plot_number:
                                self.initialize_variables.current_plot_number = new_plot_number

                    # Détection du pourcentage de preuves du plot créé
                    current_bad_percent_match = self.pattern.currentBadPercentPattern.search(line)
                    if current_bad_percent_match:
                        requested_proof = current_bad_percent_match.group(1)
                        if requested_proof is not None:
                            # Met à jour la variable
                            self.initialize_variables.requested_proof = int(requested_proof)

                        # Extraction du pourcentage
                        bad_percent_match = re.search(r'(\d+(\.\d+)?)%', current_bad_percent_match.group(3))
                        if bad_percent_match:
                            # Convertit en entier
                            bad_percent = int(float(bad_percent_match.group(1)))
                            # Met à jour la variable
                            self.initialize_variables.percent_proof = bad_percent

                    # Détection de la suppression d'un plot n'ayant pas le pourcentage de preuves voulues
                    current_bad_proof_match = self.pattern.currentBadProofPattern.search(line)
                    #
                    if current_bad_proof_match and self.config_manager.read_config(self.config_manager.config_stats).get("check_plot_status") == "on":
                        # Récupère la valeur du fichier de configuration
                        current_bad_plot_number = self.config_manager.read_config(self.config_manager.config_stats).get("bad_plot_number")
                        current_bad_plot_number = int(current_bad_plot_number) if current_bad_plot_number is not None else 0
                        # Ajoute 1 au total de plot supprimé
                        new_bad_plot_number = current_bad_plot_number + 1
                        # Mise à jour de l'interface graphique
                        self.interface.bad_plot_number_label.config(text=f"{new_bad_plot_number}")
                        # Mise à jour du fichier de configuration
                        self.config_manager.update_config({"bad_plot_number": new_bad_plot_number}, self.config_manager.config_stats)
                        # Initialisation de la variable de message
                        self.none_false_variable.bad_plot_messages = True
                        # Affichez le message
                        self.progress_messages()
                        # Réinitialisation de la progression
                        self.progress_reset()
                        # Relance la création parce que le plot n'a pas le nombre de preuves suffisant
                        self.none_false_variable.bad_proof_found = True

                    # Détection de la création réussie d'un plot
                    current_completed_plot_match = self.pattern.currentCompletedPlot.search(line)
                    if current_completed_plot_match:
                        if not self.none_false_variable.bad_proof_found:
                            # Récupère la valeur du fichier de configuration
                            current_total_plot_created = self.config_manager.read_config(self.config_manager.config_stats).get("total_plot_created")
                            current_total_plot_created = int(current_total_plot_created) if current_total_plot_created is not None else 0
                            # Ajoute 1 au total de plot créé
                            new_total_plot_created = current_total_plot_created + 1
                            # Mise à jour de l'interface graphique
                            self.interface.current_plot_text.config(text=f"{self.initialize_variables.current_plot_number}")
                            self.interface.total_plot_number_label.config(text=f"{new_total_plot_created}")
                            # Mise à jour du fichier de configuration
                            self.config_manager.update_config({"total_plot_created": new_total_plot_created}, self.config_manager.config_stats)
                            # Initialisation de la variable de message
                            self.none_false_variable.total_plot_created_messages = True
                            # Affichez le message
                            self.progress_messages()
                            # Réinitialisation de la progression
                            self.progress_reset()
                            # Réinitialisation de la variable
                            self.none_false_variable.bad_proof_found = False

                    if self.initialize_variables.current_step < len(self.lists.progress_steps):
                        step = self.lists.progress_steps[self.initialize_variables.current_step]
                        if step in line:
                            self.initialize_variables.current_step += 1
                            progress_percentage = (self.initialize_variables.current_step / total_steps) * 100

                            if progress_percentage > 0:
                                # Mise à jour de la barre de progression
                                self.interface.progress_single_plot_bar["value"] = progress_percentage
                                self.interface.progress_label.config(text=f"{progress_percentage:.2f}%")

                            # Mise à jour de l'interface graphique
                            self.plotter_gui.update_idletasks()

                # Pause pour éviter une utilisation excessive du CPU
                time.sleep(0.8)

        except Exception as e:
            self.queue_logs.log_queue_errors.put(f"Erreur lors de la surveillance de la progression: {str(e)}")

    def progress_reset(self):
        self.interface.progress_single_plot_bar["value"] = 0
        self.interface.progress_label.config(text="0%")
        self.initialize_variables.current_step = 0
        self.initialize_variables.requested_proof = 0
        self.none_false_variable.bad_plot_messages = False
        self.none_false_variable.total_plot_created_messages = False
        self.plotter_gui.update_idletasks()

    def progress_messages(self):
        if self.none_false_variable.bad_plot_messages:
            self.lists.output_lines.clear()
            # Affichez le message
            self.queue_logs.log_queue_messages.put((f"Le plot vient d'être supprimé car il n'avait que {self.initialize_variables.requested_proof}%", "warning"))
            self.none_false_variable.bad_plot_messages = False

        if self.none_false_variable.total_plot_created_messages:
            self.lists.output_lines.clear()
            # Affichez le message
            self.queue_logs.log_queue_messages.put((f"Pourcentage de preuves du dernier plot créé: {self.initialize_variables.percent_proof}%", "info"))
            self.none_false_variable.total_plot_created_messages = False
