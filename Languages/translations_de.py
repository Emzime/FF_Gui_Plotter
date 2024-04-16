# translations_de.py

translations = {
    "open": "Öffnen",
    "close": "Schließen",
    "githubResponseError": "Fehler beim Abrufen von Daten von der GitHub-API. Bitte versuchen Sie es später erneut.",
    "versionNotFound": "Datei {version} nicht gefunden",
    "guiName": "French Farmer Gui",
    "currentVersion": " - Aktuelle Version: {current_version}",
    "newVersionAvailable": " | Neue Version verfügbar: {latest_version}",
    "downloadNewVersion": "Klicken Sie hier, um die neue Version herunterzuladen",
    "badProofPercent": "Das Plot wurde gelöscht, da es nur {requested_proof}% hatte",
    "goodProofPercent": "Beweisprozentsatz des zuletzt erstellten Plots: {self.initialize_variables.percent_proof}%",
    "progressMonitoringError": "Fehler bei der Überwachung des Fortschritts: {e}",
    "gitTextError": "Fehler beim Abrufen des Inhalts der News-Datei: {e}",
    "browse_select_t1": "Wählen Sie temporäre Festplatte -t1 (NVME/SSD)",
    "browse_select_t2": "Wählen Sie temporäre Festplatte 2 -t2 (NVME/SSD)",
    "browse_select_d": "Wählen Sie einen Zielpfad -d",
    "errorRetrievingDiskSize": "Fehler beim Abrufen der Festplattengröße: {e}",
    "spaceIsFull": "Der Speicherplatz ist voll, Suche nach einem alten Plot zum Löschen...",
    "oldPlotFound": "Alter Plot gefunden: {plot_path}",
    "deletionInProgress": "Löschung läuft...",
    "oldPlotSuccessfullyRemoved": "Alter Plot erfolgreich entfernt",
    "fileNotFoundError": "Fehler, Datei {plot_path} existiert nicht oder wurde bereits gelöscht",
    "errorDeletingPlot": "Fehler beim Löschen des Plots {plot_path}: {e}",
    "title_launchPlotCreation": "Start",
    "launchPlotCreation": "Möchten Sie die Plot-Erstellung starten?",
    "plotCreationAlreadyUnderway": "Die Plot-Erstellung ist bereits im Gange",
    "pleaseFillAllRequiredFields": "Bitte füllen Sie alle erforderlichen Felder aus",
    "locationOfPlotterInvalid": "Ungültiger Ausführungsort: {plotter_path_join}",
    "locationT1Invalid": "Ungültiger Ausführungsort der temporären Festplatte -t1: {ssd_temp}",
    "locationT2Invalid": "Ungültiger Ausführungsort der temporären Festplatte 2 -t2: {ssd_temp2move}",
    "initialisation": "Initialisierung...",
    "destinationDiskNotAvailable": "Zielfestplatte ist nicht mehr verfügbar oder voll",
    "noDestinationDisksHaveEnoughSpace": "Keine Zielfestplatten haben genügend Platz zum Erstellen eines Plots",
    "availableSpace": "Verfügbarer Speicherplatz: {available_space_mb:.2f} MB | {available_space_gb:.2f} GB | {available_space_tb:.2f} TB",
    "plotsToBeCreatedIn": "{on_selected_hdd} Plots sollen in {selected_hdd} erstellt werden",
    "launchWithPID": "Start von {plotter_executable} mit PID: {plotter_pid}",
    "creationPlotsOnCompleted": "Plot-Erstellung auf Laufwerk {selected_hdd} abgeschlossen",
    "plotterNotFound": "Ausführbare Datei nicht gefunden: {e}",
    "permissionDenied": "Zugriff verweigert: {e}",
    "errorDuringPlotterStartup": "Fehler beim Starten der ausführbaren Datei: {e}",
    "plotterProcessSuccessfullyStopped": "Plotter-Prozess erfolgreich gestoppt",
    "errorStoppingPlotterProcess": "Fehler beim Stoppen des Plotter-Prozesses: {e}",
    "processInProgress": "Erstellungsprozess läuft",
    "plotterProcessUnderway": "Der Erstellungsprozess ist im Gange.\n\nMöchten Sie ihn stoppen, bevor Sie die Anwendung schließen?",
    "stoppingPlotterProcessInProgress": "Plotter-Prozess wird gestoppt...",
    "closingApplication": "Anwendung wird geschlossen",
    "wantToCloseApp": "Möchten Sie die Anwendung wirklich schließen?",
    "stopCreation": "Erstellung stoppen",
    "closeWindow": "Fenster schließen",
    "searchForAvailableSpace": "Suche nach verfügbarem Speicherplatz in {seconds_left} Sekunden\n",
    "noDiskAvailable": "Keine Zielfestplatten haben genügend Platz zum Erstellen eines Plots.\nErstellung wird gestoppt.",
    "processIdentifierRetrieval": "Abrufen der Prozess-ID für {process_name}: {str(e)}",
    "totalPlotsCreated": "Insgesamt erstellte Plots: ",
    "totalOldPlotsDeleted": "Insgesamt alte Plots gelöscht: ",
    "totalNewPlotsDeleted": "Insgesamt neue Plots gelöscht: ",
    "plotsToCreate": "Zu erstellende Plots: ",
    "plotsCreated": "Erstellte Plots: ",
    "selectPlotter": "Ausführbare Datei auswählen",
    "numberOfCheck": "Anzahl der Überprüfungen",
    "proofRateInPercent": "Beweisrate in %",
    "compressionRate": "Kompressionsrate",
    "ramQuantity": "RAM-Menge",
    "poolContract": "Pool-Vertrag",
    "farmerPublicKey": "Öffentlicher Schlüssel des Farmers",
    "browse": "Durchsuchen",
    "on": "ein",
    "off": "aus",
    "temporaryDisk_t": "Temporäre Festplatte -t",
    "temporaryDisk_2": "Temporäre Festplatte -2",
    "temporaryDisk_3": "Temporäre Festplatte -3",
    "destinationDisks_d": "Zielfestplatten -d",
    "add": "Hinzufügen",
    "remove": "Entfernen",
    "gpuOne": "GPU 1*",
    "gpuTwo": "Anzahl GPUs*",
    "Q_Flag": "-Q*",
    "A_Flag": "-A*",
    "W_Flag": "-W*",
    "w_Flag": "-w*",
    "advancedOptions": "Erweiterte Optionen für erfahrene Benutzer",
    "launchCreation": "Erstellung starten",
    "errorLogs": "Fehlerprotokolle:",
    "applicationLogs": "Anwendungsprotokolle:",
    "plotterLogs": "Protokolle des Ausführbaren:",
    "plotCheck": "Plot-Überprüfung",
    "logFile": "Protokoll",
    "delPlot": "Plots löschen",
    "welcome": (
        "\n"
        "Hallo Farmer,"
        "\n\n"
        "Hier sind einige nützliche Informationen, bevor Sie beginnen."
        "\n\n"
        "Wenn Sie nicht auf dem French Farmer Pool sind, können Sie dieses Gui trotzdem verwenden,"
        "\n"
        "wir würden uns jedoch freuen, Sie bei uns begrüßen zu dürfen, also zögern Sie nicht, sich uns anzuschließen."
        "\n"
        "Pool-Adresse: pool-xch.ffarmers.eu"
        "\n\n"
        "Um die Plot-Erstellung zu starten, müssen Sie die Felder auf der linken Seite konfigurieren:"
        "\n"
        "  - Wählen Sie die ausführbare Datei aus."
        "\n"
        "  - Wählen Sie die Komprimierung, die Sie verwenden möchten."
        "\n"
        "  - Wählen Sie die Menge an Speicher, die Sie verwenden möchten."
        "\n"
        "  - Fügen Sie den Pool-Vertrag hinzu."
        "\n"
        "  - Fügen Sie Ihren Farmer-öffentlichen Schlüssel hinzu."
        "\n"
        "  - Fügen Sie den Pfad zum temporären Datenträger hinzu."
        "\n"
        "  - Fügen Sie den Pfad zum temporären Datenträger 2 hinzu, wenn Sie weniger als 256 GB Speicher verwenden."
        "\n"
        "  - Klicken Sie abschließend auf \"Erstellung starten\"."
        "\n\n"
        "Informationen:"
        "\n"
        "Das French Farmer Gui enthält die Ausführbaren von:"
        "\n"
        "  - bladebit vom 4. Oktober 2023."
        "\n\n"
        "  - Wenn die ausgewählte ausführbare Datei bladebit ist, können Sie während der Erstellung Plot-Überprüfungen durchführen."
        "\n"
        "  - Wenn Sie Plot-Überprüfungen durchführen möchten, müssen Sie:"
        "\n"
        "       - Aktivieren Sie die Schaltfläche Plot-Überprüfung."
        "\n"
        "       - Wählen Sie die Anzahl der Überprüfungen aus."
        "\n"
        "       - Wählen Sie die Beweisrate aus, die Sie möchten."
        "\n\n"
        "  - Standardmäßig beträgt die Anzahl der Überprüfungen 30 und die Beweisrate 80%."
        "\n"
        "  - Wenn Sie die Erstellung nicht zu sehr verlangsamen möchten, wird empfohlen:"
        "\n"
        "       - 30 bis 100 Überprüfungen."
        "\n"
        "       - 80 bis 90% Beweisrate."
        "\n\n"
        "Eine Konfigurationsdatei mit dem Namen \"{config_file}\" wird im selben Verzeichnis wie dieses Skript gespeichert "
        "und wird jedes Mal gespeichert, wenn Sie eine Änderung vornehmen."
        "\n\n"
        "Wir hoffen, dass das GUI es Ihnen ermöglicht, Ihre komprimierten Plots einfach und effizient zu erstellen."
        "\n"
        "Wenn Sie Fragen haben, denken Sie daran, dass wir auf Discord verfügbar sind."
        "\n\n"
    ),
    "joinDiscord_help": (
        "Klicken Sie hier, um dem Discord-Server beizutreten"
    ),
    "joinWebsite_help": (
        "Klicken Sie hier, um die Website zu besuchen"
    ),
    "firstGpuID_help": (
        "CUDA-Gerät (Standard = 0)\n"
        "ID der ersten GPU"
    ),
    "secondGpuID_help": (
        "Anzahl der CUDA-Geräte (Standard = 1)\n"
        "Anzahl der GPUs, die für die Plot-Erstellung verwendet werden sollen.\n"
        "Diese Option wird nur aktiviert, wenn Ihr System mehr als eine GPU hat"
    ),
    "waitForCopy_help": (
        "Der Erstellungsprozess wartet darauf, dass die Kopie abgeschlossen ist, bevor der nächste Plot gestartet wird"
    ),
    "numberCachePlots_help": (
        "Maximale Anzahl von Plots, die in tmpdir zwischengespeichert werden sollen (Standard = -1)"
    ),
    "numberParallelCopy_help": (
        "Maximale Anzahl von parallelen Kopien insgesamt (Standard = -1)"
    ),
    "numberHddCopy_help": (
        "Maximale Anzahl von parallelen Kopien auf derselben Festplatte (Standard = 1, unbegrenzt = -1)"
    ),
    "delPlotsButton_help": (
        "Wenn Sie dieses Feld aktivieren, sucht das Skript automatisch nach alten Plot-Formaten sowie nach allen Plots mit einer geringeren Komprimierung\n"
        "als die, die Sie erstellen, um sie zu löschen und Platz für neue Plots zu schaffen"
    ),
    "checkButton_help": (
        "Wenn Sie das bladebit-Ausführungsprogramm auswählen, haben Sie die Möglichkeit, Plot-Überprüfungen für erstellte Plots zu aktivieren, indem Sie diese Schaltfläche auf ein stellen\n"
        "Für weitere Informationen zu Plot-Überprüfungen können Sie uns entweder auf Discord fragen oder das Chia-Wiki besuchen:\n"
        "https://docs.chia.net/cli/#plots-check"
    ),
    "logging_help": (
        "Sie haben die Möglichkeit, die Erstellung von Logdateien zu aktivieren, indem Sie diese Schaltfläche auf ein stellen. Dadurch wird eine .log-Datei im\n"
        "Verzeichnis French Farmer Gui logs erstellt."
    ),
    "plotter_help": (
        "In diesem Menü können Sie das Ausführungsprogramm auswählen, das Sie verwenden möchten. bladebit cuda ist der offizielle chia-Plotter, mit dem Sie Plots von 1 bis 7 komprimieren können\n"
        "cuda_plot_k32 ist der erste Plotter von madMAx43v3r, mit dem Sie Plots von 1 bis 20 komprimieren können\n"
        "cuda_plot_k32_v3 ist der zweite Plotter von madMAx43v3r, mit dem Sie Plots von 29 bis 33 komprimieren können"
    ),
    "checkPlot_help": (
        "Wählen Sie die Anzahl der Herausforderungen aus, die auf dem Plot ausgeführt werden sollen (Standard: 30)"
    ),
    "threshold_help": (
        "Wählen Sie den Prozentsatz aus, den der Plot erreichen muss, damit Sie ihn als gültig betrachten (Standard: 80%)"
    ),
    "compression_help": (
        "Kompressionsstufe (1 bis 9 und 11 bis 20)\n"
        "Wählen Sie die Kompressionsstufe aus, die Sie auf die Plots anwenden möchten\n"
        "Je mehr Sie komprimieren, desto mehr Ressourcen werden verbraucht, aber Ihr Ertrag wird besser"
    ),
    "ram_help": (
        "Maximaler gemeinsam/genutzter RAM in GiB (Standard = unbegrenzt)\n"
        "Wählen Sie die Menge an RAM aus, die Sie für die Erstellung komprimierter Plots zuweisen möchten. Im Allgemeinen sollten Sie so viel RAM zuweisen, wie Ihr PC hat"
    ),
    "contract_help": (
        "Pool-Vertragsadresse (62 Zeichen)\n"
        "Sie können die Pool-Vertragsnummer abrufen, indem Sie den cli-Befehl \"chia plotnft show\" in einem Terminal eingeben\n"
        "Notieren Sie die \"Pool contract address\" und geben Sie sie in das Feld \"Poolvertrag\" ein"
    ),
    "farmerKey_help": (
        "Öffentlicher Schlüssel des Farmers (48 Bytes)\n"
        "Sie können Ihren öffentlichen Schlüssel abrufen, indem Sie den cli-Befehl \"chia keys show\" in einem Terminal eingeben. Notieren Sie den \"Farmer public key\" und geben Sie ihn in das Feld \"Farmer public key\" ein"
    ),
    "hddDir_help": (
        "Endziele (Standard = <tmpdir>, remote = @HOST Nicht verfügbar)\n"
        "Fügen Sie die Festplatten hinzu, die Sie mit Plots füllen möchten"
    ),
    "temp2move_help": (
        "Temporäres Verzeichnis 2 für teilweise RAM/Festplattenmodus (Standard = @RAM)\n"
        "Temporäres Verzeichnis 3 für den Festplattenmodus (Standard = @RAM)\n"
        "Automatischer Wechsel zwischen 2 und 3 je nach ausgewählter Speichermenge"
    ),
    "temp_help": (
        "Temporäres Verzeichnis zum Speichern der Plots"
    ),
}
