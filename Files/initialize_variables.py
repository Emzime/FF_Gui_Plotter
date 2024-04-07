# initialize_variables.py


class InitializeVariables:
    def __init__(self):
        # Taille d'un plot par compression
        self.plotSizes = {
            0: 109000000000,
            1: 90409061581,
            2: 88691074663,
            3: 86973087744,
            4: 85255100826,
            5: 83537113908,
            6: 81819126989,
            7: 80101140071,
            8: 76557792052,
            9: 73121818215,
            11: 92019674317,
            12: 88583700480,
            13: 84718229914,
            14: 80208514253,
            15: 76879914599,
            16: 69578470196,
            17: 67645734912,
            18: 64102386893,
            19: 60559038874,
            20: 57015690855,
            29: 51539607552,
            30: 46493020980,
            31: 41446434407,
            32: 36399847834,
            33: 31245887079
        }

        # Initialiser les variables de progressions
        self.max_plots_on_selected_hdd = 0
        self.current_plot_number = 0
        self.current_step = 0
        self.requested_proof = 0
        self.percent_proof = 0
