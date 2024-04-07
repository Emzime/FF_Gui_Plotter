# pattern.py
import re


class Pattern:
    def __init__(self):
        # Format des anciens plots
        self.plotFormatPattern = re.compile(r'plot-k3[2-5]-\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-[0-9a-fA-F]{32}.*\.plot')

        # N° du plot en cours
        self.currentPlotPattern = re.compile(r'Generating plot (\d+)')

        # Paterne de suppression
        self.currentBadProofPattern = re.compile(r'WARNING: Deleting plot')

        # Paterne de création ne correspondant pas aux preuves demandées
        self.currentBadPercentPattern = re.compile(r'Proofs requested/fetched: (\d+) / (\d+) \( (\d+\.\d+%) \)')

        # Paterne de création réussi
        self.currentCompletedPlot = re.compile(r'Completed writing plot in')
