# translations_en.py

translations = {
    "open": "Open",
    "close": "Close",
    "githubResponseError": "Error retrieving data from GitHub API. Please try again later.",
    "versionNotFound": "File {version} not found",
    "guiName": "French Farmer Gui",
    "currentVersion": " - Current version: {current_version}",
    "newVersionAvailable": "New version available: {latest_version}",
    "downloadNewVersion": "Click to download the new version",
    "badProofPercent": "The plot has been deleted because it only had {requested_proof}%",
    "goodProofPercent": "Proof percentage of the last created plot: {self.initialize_variables.percent_proof}%",
    "progressMonitoringError": "Error monitoring progress: {e}",
    "gitTextError": "Error retrieving news file content: {e}",
    "browse_select_t1": "Select temporary disk -t1 (NVME/SSD)",
    "browse_select_t2": "Select temporary disk 2 -t2 (NVME/SSD)",
    "browse_select_d": "Select destination folder -d",
    "errorRetrievingDiskSize": "Error retrieving disk size: {e}",
    "spaceIsFull": "Space is full, searching for an old plot to delete...",
    "oldPlotFound": "Old plot found: {plot_path}",
    "deletionInProgress": "Deletion in progress...",
    "oldPlotSuccessfullyRemoved": "Old plot successfully removed",
    "fileNotFoundError": "Error, file {plot_path} does not exist or has already been deleted",
    "errorDeletingPlot": "Error deleting plot {plot_path}: {e}",
    "title_launchPlotCreation": "Launch",
    "launchPlotCreation": "Do you want to launch plot creation?",
    "plotCreationAlreadyUnderway": "Plot creation is already underway",
    "pleaseFillAllRequiredFields": "Please fill in all required fields",
    "locationOfPlotterInvalid": "Invalid executable location: {plotter_path_join}",
    "locationT1Invalid": "Invalid temporary disk -t1 location: {ssd_temp}",
    "locationT2Invalid": "Invalid temporary disk 2 -t2 location: {ssd_temp2move}",
    "initialisation": "Initialization...",
    "destinationDiskNotAvailable": "Destination disk is no longer available or full",
    "noDestinationDisksHaveEnoughSpace": "No destination disks have enough space to create a plot",
    "availableSpace": "Available space: {available_space_mb:.2f} MB | {available_space_gb:.2f} GB | {available_space_tb:.2f} TB",
    "plotsToBeCreatedIn": "{on_selected_hdd} plots to be created in {selected_hdd}",
    "launchWithPID": "Launching {plotter_executable} with PID: {plotter_pid}",
    "creationPlotsOnCompleted": "Plot creation on disk {selected_hdd} completed",
    "plotterNotFound": "Executable not found: {e}",
    "permissionDenied": "Permission denied: {e}",
    "errorDuringPlotterStartup": "Error during executable startup: {e}",
    "plotterProcessSuccessfullyStopped": "Plotter process stopped successfully",
    "errorStoppingPlotterProcess": "Error stopping plotter process: {e}",
    "processInProgress": "Creation process in progress",
    "plotterProcessUnderway": "The creation process is underway.\n\nDo you want to stop it before closing the application?",
    "stoppingPlotterProcessInProgress": "Stopping plotter process in progress...",
    "closingApplication": "Closing application",
    "wantToCloseApp": "Are you sure you want to close the application?",
    "stopCreation": "Stop creation",
    "closeWindow": "Close window",
    "searchForAvailableSpace": "Searching for available space in {seconds_left} seconds\n",
    "noDiskAvailable": "No destination disks have enough space to create a plot.\nStopping creation.",
    "processIdentifierRetrieval": "Retrieving process identifier for {process_name}: {str(e)}",
    "totalPlotsCreated": "Total plots created: ",
    "totalOldPlotsDeleted": "Total old plots deleted: ",
    "totalNewPlotsDeleted": "Total new plots deleted: ",
    "plotsToCreate": "Plots to create: ",
    "plotsCreated": "Plots created: ",
    "selectPlotter": "Select executable",
    "numberOfCheck": "Number of checks",
    "proofRateInPercent": "Proof rate in %",
    "compressionRate": "Compression rate",
    "ramQuantity": "RAM quantity",
    "poolContract": "Pool contract",
    "farmerPublicKey": "Farmer public key",
    "browse": "Browse",
    "on": "on",
    "off": "off",
    "temporaryDisk_t": "Temporary disk -t",
    "temporaryDisk_2": "Temporary disk -2",
    "temporaryDisk_3": "Temporary disk -3",
    "destinationDisks_d": "Destination disks -d",
    "add": "Add",
    "remove": "Remove",
    "gpuOne": "GPU 1*",
    "gpuTwo": "GPU count*",
    "Q_Flag": "-Q*",
    "A_Flag": "-A*",
    "W_Flag": "-W*",
    "w_Flag": "-w*",
    "advancedOptions": "Advanced options for experienced users",
    "launchCreation": "Launch creation",
    "errorLogs": "Error logs:",
    "applicationLogs": "Application logs:",
    "plotterLogs": "Plotter logs:",
    "plotCheck": "Check Plot",
    "logFile": "Logs",
    "delPlot": "Delete Plots",
    "welcome": (
        "\n"
        "Hello Farmers,"
        "\n\n"
        "Here are some useful information before starting."
        "\n\n"
        "If you're not on the French Farmer pool, you can still use this Gui but"
        "\n"
        "we would be happy to have you with us so don't hesitate to join us."
        "\n"
        "Pool address: pool-xch.ffarmers.eu"
        "\n\n"
        "To launch plot creation, you must configure the fields on the left:"
        "\n"
        "  - Select the executable."
        "\n"
        "  - Select the compression you want to use."
        "\n"
        "  - Select the amount of memory you want to use."
        "\n"
        "  - Add the pool contract."
        "\n"
        "  - Add your farmer public key."
        "\n"
        "  - Add the path to the temporary disk."
        "\n"
        "  - Add the path to temporary disk 2 if you're using less than 256 GB of memory."
        "\n"
        "  - Finally, just click on \"Launch creation\"."
        "\n\n"
        "Information:"
        "\n"
        "The French Farmer GUI contains the executables:"
        "\n"
        "  - gigaHorse from March 25, 2024."
        "\n"
        "  - bladebit from October 4, 2023."
        "\n\n"
        "  - If the selected executable is bladebit, you can perform plot checks during creation."
        "\n"
        "  - If you want to perform plot checks, you must:"
        "\n"
        "       - Activate the Check Plot button."
        "\n"
        "       - Choose the number of checks."
        "\n"
        "       - Choose the proof rate you want."
        "\n\n"
        "  - By default, the number of checks is 30 and the proof rate is 80%."
        "\n"
        "  - If you don't want to slow down the creation too much, it is recommended to use:"
        "\n"
        "       - 30 to 100 checks."
        "\n"
        "       - 80 to 90% proof rate."
        "\n\n"
        "A configuration file named \"{config_file}\" will be saved in the same directory as this script "
        "and will be saved each time you make a modification."
        "\n\n"
        "We hope that the GUI will allow you to create your compressed plots easily and efficiently."
        "\n"
        "If you have any questions, don't forget that we are available on Discord."
        "\n\n"
    ),
    "joinDiscord_help": (
        "Click to join the Discord server"
    ),
    "joinWebsite_help": (
        "Click to visit the website"
    ),
    "firstGpuID_help": (
        "CUDA device (default = 0)\n"
        "ID of the first GPU"
    ),
    "secondGpuID_help": (
        "Number of CUDA devices (default = 1)\n"
        "Number of GPUs to use for plot creation.\n"
        "This option only activates if your system has more than one GPU"
    ),
    "waitForCopy_help": (
        "The creation process waits for the copy to finish before starting the next plot"
    ),
    "numberCachePlots_help": (
        "Maximum number of plots to cache in tmpdir (default = -1)"
    ),
    "numberParallelCopy_help": (
        "Maximum number of parallel copies in total (default = -1)"
    ),
    "numberHddCopy_help": (
        "Maximum number of parallel copies on the same hard disk (default = 1, unlimited = -1)"
    ),
    "delPlotsButton_help": (
        "If you check this box, the script will automatically search for old plot formats as well as any plots with a lower compression\n"
        "than the one you're creating to delete them and make room for new plots"
    ),
    "checkButton_help": (
        "If you choose the bladebit executable, you have the option to enable plot checks for created plots by toggling this button to on\n"
        "for more information on plot checks, you can either ask us on discord or visit the chia wiki:\n"
        "https://docs.chia.net/cli/#plots-check"
    ),
    "logging_help": (
        "You have the option to enable log file creation by toggling this button to on, this will create a .log file in the\n"
        "French Farmer Gui logs directory."
    ),
    "plotter_help": (
        "This menu allows you to choose the executable you want to use, bladebit cuda is the official chia plotter which allows you to compress plots from 1 to 7\n"
        "cuda_plot_k32 is the first plotter by madMAx43v3r, it allows you to compress plots from 1 to 20\n"
        "cuda_plot_k32_v3 is the second plotter by madMAx43v3r, it allows you to compress plots from 29 to 33"
    ),
    "checkPlot_help": (
        "Choose the number of challenges to run on the plot (default: 30)"
    ),
    "threshold_help": (
        "Choose the percentage the plot must achieve for you to consider it valid (default: 80%)"
    ),
    "compression_help": (
        "Compression level (1 to 9 and 11 to 20)\n"
        "Choose the compression level you want to apply to plots\n"
        "the more you compress the more you consume but the better your yield"
    ),
    "ram_help": (
        "Maximum shared/pinned memory in GiB (default = unlimited)\n"
        "Choose the amount of ram you want to allocate for compressed plot creation, typically you should allocate as much ram as your pc contains"
    ),
    "contract_help": (
        "Pool contract address (62 characters)\n"
        "You can retrieve the pool contract number by typing the cli command \"chia plotnft show\" in a terminal\n"
        "note the \"Pool contract address\" and enter it in the \"Pool contract\" field"
    ),
    "farmerKey_help": (
        "Farmer public key (48 bytes)\n"
        "You can retrieve your public key by typing the cli command \"chia keys show\" in a terminal, note the \"Farmer public key\" and enter it in the \"Farmer public key\" field"
    ),
    "hddDir_help": (
        "Final destinations (default = <tmpdir>, remote = @HOST Not available)\n"
        "Add the disks you want to fill with plots"
    ),
    "temp2move_help": (
        "Temporary directory 2 for partial RAM/disk mode (default = @RAM)\n"
        "Temporary directory 3 for disk mode (default = @RAM)\n"
        "Automatic switch between 2 and 3 depending on the selected amount of memory"
    ),
    "temp_help": (
        "Temporary directory for storing plots"
    ),
}
