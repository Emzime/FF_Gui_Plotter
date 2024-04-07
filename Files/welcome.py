# welcome.py


class Welcome:
    def __init__(self, ff_plotter_gui):
        self.config_manager = ff_plotter_gui.config_manager
        self.queue_logs = ff_plotter_gui.queue_logs
        self.log_manager = ff_plotter_gui.log_manager

    def show_message(self):
        self.queue_logs.log_queue_messages.put((
            "\nHello French Farmer's, voici quelques informations utiles avant de commencer.\n"
            "\n"
            "Pour lancer la création de plot, tu dois configurer les champs sur la gauche\n"
            "  - Sélectionne le plotter.\n"
            "  - Sélectionne la compression que tu veux utiliser.\n"
            "  - Sélectionne la quantité de mémoire que tu veux utiliser.\n"
            "  - Ajoute le contrat de pool.\n"
            "  - Ajoute ta clé publique du farmer.\n"
            "  - Ajoute le chemin vers le disque temporaire.\n"
            "  - Ajoute le chemin vers le disque temporaire 2 si tu utilise moins de 256Go de mémoire.\n"
            "  - Enfin, il ne te reste plus qu'a cliquer sur 'Lancer la création.\n"
            "\n"
            "Information:\n"
            "Le GUI French Farmer contient les exécutables de:\n"
            "  - gigaHorse du 25 Mars 2024.\n"
            "  - bladebit du 04 Octobre 2023.\n"
            "\n"
            "  - Si le plotter sélectionné est bladebit, tu pourra effectuer un check plot pendant la création.\n"
            "  - Si tu veux effectuer un check plot, tu dois:\n"
            "       - Activer le bouton en haut\n"
            "       - Choisir le nombre de contrôle\n"
            "       - Choisir le taux de preuve que tu veux.\n"
            "\n"
            "  - Par défaut les valeurs du nombre de contrôle est de 30 et le taux de preuve est de 80%.\n"
            "  - Si tu ne veux trop ralentir la création, il est conseillé d'utiliser:\n"
            "       - 30 à 100 en nombre de contrôle\n"
            "       - 80 à 90% en taux de preuve.\n"
            "\n"
            f"Un fichier de configuration portant le nom de '{self.config_manager.config_file}' sera enregistré dans le même répertoire que ce script "
            "et sera sauvegardé à chaque modification que tu effectueras.\n"
            "\n"
            "Nous espérons que le Gui te permettra de créer tes plots compressés de façon simple et efficace.\n"
            "Si tu as une question à poser, n'oubli pas que nous sommes disponible sur discord.\n"
            "\n", None
        ))
