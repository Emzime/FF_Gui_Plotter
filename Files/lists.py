# lists.py
import os


class Lists:
    def __init__(self, ff_plotter_gui):
        # Création des instances
        self.plotter_gui = ff_plotter_gui
        self.interface = ff_plotter_gui.interface
        self.config_manager = ff_plotter_gui.config_manager

        plotter = self.config_manager.read_config(self.config_manager.config_file).get("plotter_executable")
        plotter_name = os.path.splitext(plotter)[0]

        # Initialisation de la liste des messages de progression
        self.output_lines = []

        # Liste des étapes de progression à rechercher
        if plotter_name.startswith("bladebit"):
            self.progress_steps = [
                "Generating plot",
                "Generating F1",
                "Finished F1 in",
                "Table 2 completed in",
                "Table 3 completed in",
                "Table 4 completed in",
                "Table 5 completed in",
                "Table 6 completed in",
                "Table 7 completed in",
                "Finalizing Table 7",
                "Finalized Table 7 in",
                "Completed Phase 1 in",
                "Marked Table 6 in",
                "Marked Table 5 in",
                "Marked Table 4 in",
                "Marked Table 3 in",
                "Completed Phase 2 in",
                "Compressing Table 2 and 3...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Completed table 2 in",
                "Compressing tables 3 and 4...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 3 in",
                "Compressing tables 4 and 5...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 4 in",
                "Compressing tables 5 and 6...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 5 in",
                "Compressing tables 6 and 7...",
                "Step 1 completed step in",
                "Step 2 completed step in",
                "Step 3 completed step in",
                "Completed table 6 in",
                "Completed Phase 3 in",
                "Completed Plot",
                "Completed writing plot in"
            ]
        else:
            self.progress_steps = [
                "[P1] Setup took",
                "[P1] Table 1 took",
                "[P1] Table 2 took",
                "[P1] Table 3 took",
                "[P1] Table 4 took",
                "[P1] Table 5 took",
                "[P1] Table 6 took",
                "[P1] Table 7 took",
                "Phase 1 took",
                "Phase 2 took",
                "[P3] Setup took",
                "Phase 3 took",
                "[P4] Setup took",
                "Phase 4 took",
                "Total plot creation time was"
            ]

        # Désactiver tous les éléments de l'interface pendant la création
        self.check_plot_elements_disable = [
            self.interface.check_plot_value_combobox,
            self.interface.check_threshold_value_combobox,
            self.interface.compression_combobox,
            self.interface.ram_qty_combobox,
            self.interface.contract_entry,
            self.interface.farmer_key_entry,
            self.interface.ssd_temp_entry,
            self.interface.ssd_temp_button,
            self.interface.ssd_temp2move_entry,
            self.interface.ssd_temp2move_button,
            self.interface.plotter_path_combobox,
            self.interface.hdd_dir_listbox,
            self.interface.add_hdd_dir_button,
            self.interface.remove_hdd_dir_button
        ]
