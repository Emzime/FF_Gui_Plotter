# progress_bar.py
import time
from Files.translation import Lang


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
                for line in self.lists.output_lines:
                    # Détection du pourcentage de preuves du plot créé sous Bladebit
                    if self.plotter_gui.check_plot_status == Lang.translate("on"):
                        current_bad_percent_match = self.pattern.currentBadPercentPattern.search(line)
                        if current_bad_percent_match:
                            requested_proof = current_bad_percent_match.group(1)
                            if requested_proof is not None:
                                # Met à jour la variable
                                self.initialize_variables.requested_proof = int(requested_proof)

                            # Extraction du pourcentage
                            bad_percent_match = self.pattern.currentSeePercentPattern.search(current_bad_percent_match.group(3))
                            if bad_percent_match:
                                # Convertit en entier
                                bad_percent = int(float(bad_percent_match.group(1)))
                                # Met à jour la variable
                                self.initialize_variables.percent_proof = bad_percent

                    # Détection de la suppression d'un plot n'ayant pas le pourcentage de preuves voulues sous Bladebit
                    current_bad_proof_match = self.pattern.currentBadProofPattern.search(line)
                    # Traitement lorsque la suppression d'un plot avec un pourcentage de preuves insuffisant est détectée
                    if current_bad_proof_match and self.plotter_gui.check_plot_status == Lang.translate("on"):
                        self.handle_bad_proof_detection()

                    # Traitement lorsque la création d'un plot est réussie avec Bladebit
                    current_completed_plot_match = self.pattern.currentCompletedPlot.search(line)
                    if current_completed_plot_match and not self.none_false_variable.bad_proof_found:
                        self.handle_successful_plot_creation()

                    # Traitement lorsque la création d'un plot est réussie avec gigaHorse
                    current_completed_gh_plot_match = self.pattern.currentCompletedGHPlot.search(line)
                    if current_completed_gh_plot_match and not self.none_false_variable.bad_proof_found:
                        self.handle_successful_plot_creation()

                    # Mise à jour de la barre de progression lorsque des étapes spécifiques sont détectées
                    if self.initialize_variables.current_step < len(self.lists.progress_steps):
                        step = self.lists.progress_steps[self.initialize_variables.current_step]
                        if step in line:
                            # Incrémenter le nombre d'étapes
                            self.initialize_variables.current_step += 1
                            # Mise à jour de la barre de progression
                            progress_percentage = (self.initialize_variables.current_step / total_steps) * 100
                            self.interface.progress_single_plot_bar["value"] = progress_percentage
                            self.interface.progress_label.config(text=f"{progress_percentage:.2f}%")
                            # Mise à jour de l'interface graphique
                            self.plotter_gui.update_idletasks()

                # Pause pour éviter une utilisation excessive du CPU
                time.sleep(0.8)

        except Exception as e:
            self.queue_logs.log_queue_errors.put(Lang.translate("progressMonitoringError").format(e=str(e)))

    # Gère les cas de création réussie d'un plot
    def handle_successful_plot_creation(self):
        if not self.none_false_variable.bad_proof_found:
            # Récupérer le nombre actuel de plots maximums
            current_max_plots = self.initialize_variables.max_plots_on_selected_hdd
            # Décrémenter le nombre de plots maximums
            new_max_plots = current_max_plots - 1
            # Mettre à jour l'interface graphique avec le nouveau nombre de plots maximums
            self.interface.current_plot_max_text.config(text=str(new_max_plots))
            # Mettre à jour la variable de plots maximums
            self.initialize_variables.max_plots_on_selected_hdd = new_max_plots

            # Récupérer le nombre actuel de plots total créés
            current_total_plot_created = self.config_manager.read_config(self.config_manager.config_stats).get("total_plot_created")
            current_total_plot_created = int(current_total_plot_created) if current_total_plot_created is not None else 0
            # Incrémenter le nombre de plots total créés
            new_total_plot_created = current_total_plot_created + 1
            # Mettre à jour l'interface graphique avec le nouveau nombre de plots total créés
            self.interface.total_plot_number_label.config(text=str(new_total_plot_created))

            # Récupérer le nombre actuel de plots créés
            current_plot_number = self.initialize_variables.current_plot_number
            # Incrémente le nombre de plots créés
            new_current_plot_number = current_plot_number + 1
            # Mettre à jour l'interface graphique avec le nouveau nombre de plots créés
            self.interface.current_plot_text.config(text=str(new_current_plot_number))
            # Mettre à jour la variable de plots créés
            if new_current_plot_number > self.initialize_variables.current_plot_number:
                self.initialize_variables.current_plot_number = new_current_plot_number

            # Mettre à jour le fichier de configuration
            self.config_manager.update_config({"total_plot_created": new_total_plot_created}, self.config_manager.config_stats)
            self.none_false_variable.total_plot_created_messages = True
            self.progress_messages()
            self.progress_reset()
            self.none_false_variable.bad_proof_found = False

    # Gère les cas de suppression d'un plot avec un pourcentage de preuves insuffisant
    def handle_bad_proof_detection(self):
        # Récupérer le nombre actuel de mauvais plots créés
        current_bad_plot_number = self.config_manager.read_config(self.config_manager.config_stats).get("bad_plot_number")
        current_bad_plot_number = int(current_bad_plot_number) if current_bad_plot_number is not None else 0
        # Incrémenter le nombre de mauvais plots créés
        new_bad_plot_number = current_bad_plot_number + 1
        # Mettre à jour l'interface graphique avec le nouveau nombre de mauvais plots créés
        self.interface.bad_plot_number_label.config(text=f"{new_bad_plot_number}")

        # Mettre à jour le fichier de configuration
        self.config_manager.update_config({"bad_plot_number": new_bad_plot_number}, self.config_manager.config_stats)
        self.none_false_variable.bad_plot_messages = True
        self.progress_messages()
        self.progress_reset()
        self.none_false_variable.bad_proof_found = True

    # Réinitialise les paramètres de progression après chaque événement de création de plot
    def progress_reset(self):
        if hasattr(self.interface, "progress_single_plot_bar"):
            self.interface.progress_single_plot_bar["value"] = 0
        if hasattr(self.interface, "progress_label"):
            self.interface.progress_label.config(text="0%")
        self.initialize_variables.current_step = 0
        self.initialize_variables.requested_proof = 0
        self.none_false_variable.bad_plot_messages = False
        self.none_false_variable.total_plot_created_messages = False

    # Affiche les messages correspondant aux événements détectés
    def progress_messages(self):
        if self.none_false_variable.bad_plot_messages:
            self.lists.output_lines.clear()
            self.none_false_variable.bad_plot_messages = False
            # Affichez le message
            if self.plotter_gui.check_plot_status == Lang.translate("on"):
                self.queue_logs.log_queue_messages.put((Lang.translate("badProofPercent").format(requested_proof=self.initialize_variables.requested_proof), "warning"))

        if self.none_false_variable.total_plot_created_messages:
            self.lists.output_lines.clear()
            self.none_false_variable.total_plot_created_messages = False
            # Affichez le message
            if self.plotter_gui.check_plot_status == Lang.translate("on"):
                self.queue_logs.log_queue_messages.put((Lang.translate("goodProofPercent").format(percent_proof=self.initialize_variables.percent_proof), "info"))
