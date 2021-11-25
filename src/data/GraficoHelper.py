import numpy as np

# Classe para auxiliar graficos no notebook
class GraficoHelper:

    def exibirValores(axs, orient='v' ):
        def _single(ax):
            if orient == 'v':
                for p in ax.patches:
                    _x = p.get_x() + p.get_width() / 1.5
                    _y = p.get_y() + p.get_height() + (p.get_height() * 0.02)
                    val = p.get_height()
                    ax.text(_x, _y, val, ha="center")
            elif orient == 'h':
                for p in ax.patches:
                    _x = p.get_x() + p.get_width() + 1
                    _y = p.get_y() + p.get_height() / 1.8
                    val = p.get_width()
                    ax.text(_x, _y, val, ha="left")

        if isinstance(axs, np.ndarray):
            for idx, ax in np.ndenumerate(axs):
                _single(ax)
        else:
            _single(axs)