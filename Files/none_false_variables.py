# none_false_variables.py


class NoneFalseVariables:
    def __init__(self):
        # DEBUG
        self.debug = False
        # Initialisez la variable
        self.process = None
        # Initialisez la variable
        self.plotter_pid = None
        # Initialisez la variable
        self.plotter_process = None
        # Indicateur de création en cours
        self.plot_creation_in_progress = False
        # Drapeau pour contrôler l'arrêt de la création
        self.stop_creation = False
        # Variable pour suivre si current_bad_proof_match a déjà été trouvé
        self.bad_proof_found = False

        self.bad_plot_messages = False
        self.total_plot_created_messages = False

        self.delOldPlots = False
