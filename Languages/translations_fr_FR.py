translations = {
    "githubResponseError": "Erreur lors de la récupération des données depuis l'API GitHub. Veuillez réessayer plus tard.",
    "versionNotFound": "Le fichier {version} n'existe pas",
    "guiName": "French Farmer Gui - ",
    "currentVersion": "Version actuelle: {current_version}",
    "newVersionAvailable": "Nouvelle version disponible: {latest_version}",
    "downloadNewVersion": "Cliquez pour télécharger la nouvelle version",
    "badProofPercent": "La parcelle vient d'être supprimé car elle n'avait que {requested_proof}%",
    "goodProofPercent": "Pourcentage de preuves de la dernière parcelle créé: {self.initialize_variables.percent_proof}%",
    "progressMonitoringError": "Erreur lors de la surveillance de la progression: {e}",
    "browse_select_t1": "Sélectionnez le disque temporaire -t1 (NVME/SSD)",
    "browse_select_t2": "Sélectionnez le disque temporaire 2 -t2 (NVME/SSD)",
    "browse_select_d": "Sélectionnez un dossier de destination -d",
    "errorRetrievingDiskSize": "Erreur lors de la récupération de la taille du disque: {e}",
    "spaceIsFull": "Space is full, looking for an old stud to remove...",
    "oldPlotFound": "Ancienne parcelle trouvé: {plot_path}",
    "deletionInProgress": "Suppression en cours...",
    "oldPlotSuccessfullyRemoved": "Ancienne parcelle supprimée avec succès",
    "errorDeletingPlot": "Erreur lors de la suppression de la parcelle {plot_path}: {e}",
    "title_launchPlotCreation": "Lancement",
    "launchPlotCreation": "Voulez-vous lancer la création de parcelle ?",
    "plotCreationAlreadyUnderway": "La création de parcelle est déjà en cours",
    "pleaseFillAllRequiredFields": "Veuillez remplir tous les champs obligatoires",
    "locationOfPlotterInvalid": "L'emplacement de l'exécutable n'est pas valide: {plotter_path_join}",
    "locationT1Invalid": "L'emplacement du disque temporaire -t1 n'est pas valide: {ssd_temp}",
    "locationT2Invalid": "L'emplacement du disque temporaire 2 -t2 n'est pas valide: {ssd_temp2move}",
    "initialisation": "Initialisation...",
    "destinationDiskNotAvailable": "Le disque de destination n'est plus disponible: {selected_hdd}",
    "noDestinationDisksHaveEnoughSpace": "Aucun disques de destinations n'a suffisamment d'espace pour créer une parcelle",
    "availableSpace": "Espace disponible: {available_space_mb:.2f} Mo | {available_space_gb:.2f} Go | {available_space_tb:.2f} To",
    "plotsToBeCreatedIn": "{on_selected_hdd} parcelles à créer dans {selected_hdd}",
    "launchWithPID": "Lancement de {plotter_executable} avec le PID: {plotter_pid}",
    "creationPlotsOnCompleted": "Création des parcelles sur le disque {selected_hdd} terminée",
    "plotterNotFound": "Exécutable introuvable : {e}",
    "permissionDenied": "Permission refusée : {e}",
    "errorDuringPlotterStartup": "Erreur lors du démarrage de l'exécutable: {e}",
    "plotterProcessSuccessfullyStopped": "Arrêt du processus de création effectué avec succès",
    "errorStoppingPlotterProcess": "Erreur lors de l'arrêt du processus de création: {e}",
    "processInProgress": "Processus de création en cours",
    "plotterProcessUnderway": "Le processus de création est en cours.\n\nVoulez-vous l'arrêter avant de fermer l'application ?",
    "stoppingPlotterProcessInProgress": "Arrêt du processus de création en cours...",
    "closingApplication": "Fermeture de l'application",
    "wantToCloseApp": "Êtes-vous sûr de vouloir fermer l'application ?",
    "stopCreation": "Stopper la création",
    "closeWindow": "Fermer la fenêtre",
    "searchForAvailableSpace": "Recherche d'espace disponible dans {seconds_left} secondes\n",
    "processIdentifierRetrieval": "Récupération de l'identifiant du processus {process_name}: {str(e)}",
    "totalPlotsCreated": "Total de plots créés : ",
    "totalOldPlotsDeleted": "Total d'anciens plots supprimés :",
    "totalNewPlotsDeleted": "Total de nouveaux plots supprimés :",
    "plotsToCreate": "Plots à créer :",
    "plotsCreated": "Plots créés :",
    "selectPlotter": "Sélectionner l'exécutable",
    "numberOfCheck": "Nombre de contrôles",
    "proofRateInPercent": "Taux de preuve en %",
    "compressionRate": "Taux de compression",
    "ramQuantity": "Quantité de RAM",
    "poolContract": "Contrat de pool",
    "farmerPublicKey": "Clé publique",
    "browse": "Parcourir",
    "on": "on",
    "off": "off",
    "temporaryDisk_t": "Disque temporaire -t",
    "temporaryDisk_2": "Disque temporaire -2",
    "temporaryDisk_3": "Disque temporaire -3",
    "destinationDisks_d": "Disques de destination -d",
    "add": "Ajouter",
    "remove": "Supprimer",
    "gpuOne": "GPU 1*",
    "gpuTwo": "GPU 2*",
    "Q_Flag": "-Q*",
    "A_Flag": "-A*",
    "W_Flag": "-W*",
    "w_Flag": "-w*",
    "advancedOptions": "Options avancées pour utilisateur averti",
    "launchCreation": "Lancer la création",
    "errorLogs": "Journal des erreurs :",
    "applicationLogs": "Journal de l'application :",
    "plotterLogs": "Journal de l'exécutable :",
    "plotCheck": "Check Plot",
    "logFile": "Logs",
    "delPlot": "Suppression des plots",
    "welcome": (
        "\n"
        "Hello Farmer's,"
        "\n\n"
        "Voici quelques informations utiles avant de commencer."
        "\n\n"
        "Si tu n'es pas sur la pool French Farmer, tu peux quand même utiliser ce Gui mais"
        "\n"
        "nous serions ravis de te compter parmi nous alors n'hésite pas à nous rejoindre."
        "\n"
        "Adresse de la pool: pool-xch.ffarmers.eu"
        "\n\n"
        "Pour lancer la création de parcelles, tu dois configurer les champs sur la gauche:"
        "\n"
        "  - Sélectionne l'exécutable'."
        "\n"
        "  - Sélectionne la compression que tu veux utiliser."
        "\n"
        "  - Sélectionne la quantité de mémoire que tu veux utiliser."
        "\n"
        "  - Ajoute le contrat de pool."
        "\n"
        "  - Ajoute ta clé publique du fermier."
        "\n"
        "  - Ajoute le chemin vers le disque temporaire."
        "\n"
        "  - Ajoute le chemin vers le disque temporaire 2 si tu utilises moins de 256 Go de mémoire."
        "\n"
        "  - Enfin, il ne te reste plus qu'à cliquer sur 'Lancer la création'."
        "\n\n"
        "Informations :"
        "\n"
        "Le GUI French Farmer contient les exécutables de:"
        "\n"
        "  - gigaHorse du 25 Mars 2024."
        "\n"
        "  - bladebit du 04 Octobre 2023."
        "\n\n"
        "  - Si l'exécutable sélectionné est bladebit, tu pourras effectuer une vérification des parcelles pendant la création."
        "\n"
        "  - Si tu veux effectuer une vérification des parcelles, tu dois:"
        "\n"
        "       - Activer le bouton Check Plot."
        "\n"
        "       - Choisir le nombre de contrôles."
        "\n"
        "       - Choisir le taux de preuve que tu veux."
        "\n\n"
        "  - Par défaut, les valeurs du nombre de contrôles sont de 30 et le taux de preuve est de 80 %."
        "\n"
        "  - Si tu ne veux pas trop ralentir la création, il est conseillé d'utiliser:"
        "\n"
        "       - 30 à 100 en nombre de contrôles."
        "\n"
        "       - 80 à 90 % en taux de preuve."
        "\n\n"
        "Un fichier de configuration portant le nom de '{config_file}' sera enregistré dans le même répertoire que ce script "
        "et sera sauvegardé à chaque modification que tu effectueras."
        "\n\n"
        "Nous espérons que le GUI te permettra de créer tes parcelles compressés de façon simple et efficace."
        "\n"
        "Si tu as une question à poser, n'oublie pas que nous sommes disponibles sur Discord."
        "\n\n"
    ),
    "joinDiscord_help": (
        "Clique pour rejoindre le serveur Discord"
    ),
    "joinWebsite_help": (
        "Clique pour visiter le site internet"
    ),
    "firstGpuID_help": (
        "Périphérique CUDA (par défaut = 0)\n"
        "ID de la première carte graphique"
    ),
    "secondGpuID_help": (
        "Périphérique CUDA (par défaut = 1)\n"
        "ID de la seconde carte graphique\n"
        "Cette option ne s'active que si ton système comporte plus d'une carte graphique"
    ),
    "waitForCopy_help": (
        "Le processus de création attend la fin de la copie avant de commencer la parcelle suivante"
    ),
    "numberCachePlots_help": (
        "Nombre maximal de parcelles à mettre en cache dans tmpdir (par défaut = -1)"
    ),
    "numberParallelCopy_help": (
        "Nombre maximal de copies parallèles au total (par défaut = -1)"
    ),
    "numberHddCopy_help": (
        "Nombre maximal de copies parallèles sur le même disque dur (par défaut = 1, illimité = -1)"
    ),
    "delPlotsButton_help": (
        "Si tu active cette case, le script cherchera automatiquement les anciens formats de parcelles ainsi que toutes les parcelles ayant une compression inférieure\n"
        "à celle que tu crée pour les supprimer et faire de la place pour les nouvelles parcelles"
    ),
    "checkButton_help": (
        "Si tu choisi l'exécutable bladebit, tu as la possibilité d'activer la vérification des parcelles créées en plaçant ce bouton sur on\n"
        "pour plus d'informations sur la vérification des parcelles, tu peux soit nous demander sur discord ou te rendre sur le wiki de chia:\n"
        "https://docs.chia.net/cli/#plots-check"
    ),
    "logging_help": (
        "Tu as la possibilité d'activer la création de fichier journal en plaçant ce bouton sur on, cela aura pour effet de créer un fichier .log dans le\n"
        "répertoire logs de French Farmer Gui."
    ),
    "plotter_help": (
        "Ce menu te permet de choisir l'exécutable que tu souhaites utiliser, bladebit cuda est le \"plotter\" officiel de chia qui te permet de compresser les parcelles de 1 à 7\n"
        "cuda_plot_k32 est le premier \"plotter\" de madMAx43v3r, il te permet de compresser les parcelles de 1 à 20\n"
        "cuda_plot_k32_v3 est le second \"plotter\" de madMAx43v3r, il te permet de compresser les parcelles de 29 à 33"
    ),
    "checkPlot_help": (
        "Choisi le nombre de défis à exécuter sur la parcelle (défaut: 30)"
    ),
    "threshold_help": (
        "Choisi le pourcentage que la parcelle doit obtenir pour que tu le considère comme valide (défaut: 80%)"
    ),
    "compression_help": (
        "Niveau de compression (1 à 9 et 11 à 20)\n"
        "Choisi le niveau de compression que tu veux appliquer aux parcelles\n"
        "plus tu compresses plus tu consommes mais meilleurs est ton rendement"
    ),
    "ram_help": (
        "Mémoire partagée / épinglée maximale en GiB (par défaut = illimité)\n"
        "Choisi la quantité de ram que tu veux allouer pour la création des parcelles compressées, en général tu dois allouer autant de ram que ton pc contient"
    ),
    "contract_help": (
        "Adresse du contrat du pool (62 caractères)\n"
        "Tu peux récupérer le n° de contrat de pool en tapant la commande cli \"chia plotnft show\" dans un terminal\n"
        "note la \"Pool contract address\" et inscrit la dans la case \"contrat de pool\""
    ),
    "farmerKey_help": (
        "Clé publique du fermier (48 octets)\n"
        "Tu peux récupérer ta clé publique en tapant la commande cli \"chia keys show\" dans un terminal, note la \"Farmer public key\" et inscrit la dans la case \"Clé publique\""
    ),
    "hddDir_help": (
        "Destinations finales (default = <tmpdir>, remote = @HOST)\n"
        "Ajoute les disques que tu veux remplir de parcelles"
    ),
    "temp2move_help": (
        "Répertoire temporaire 2 pour le mode partiel RAM / disque (défaut = @RAM)\n"
        "Répertoire temporaire 3 pour le mode disque (par défaut = @RAM)\n"
        "Changement automatique entre le 2 et 3 selon la quantité de mémoire sélectionné"
    ),
    "temp_help": (
        "Répertoire temporaire pour le stockage des parcelles"
    ),
}
