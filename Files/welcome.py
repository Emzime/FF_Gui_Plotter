# welcome.py
from Files.translation import Lang


class Welcome:
    def __init__(self, ff_plotter_gui):
        self.config_manager = ff_plotter_gui.config_manager
        self.queue_logs = ff_plotter_gui.queue_logs
        self.log_manager = ff_plotter_gui.log_manager

    def show_message(self):
        self.queue_logs.log_queue_messages.put((Lang.translate("welcome").format(config_file=self.config_manager.config_file), "welcome"))
