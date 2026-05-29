# ============================================================
#  TFI - Simulador E-Waste | Scrap y Rezagos S.R.L.
#  UTN Facultad Regional Tucuman - Comision 4K2
#  Grupo N1: Ammiraglia, Bazan, Figueroa, Lazarte, Moeykens, Munoz
# ============================================================
#
#  Punto de entrada principal de la aplicacion.
#  Ejecutar con:
#      venv\Scripts\python.exe main.py
#
# ============================================================

import tkinter as tk
from src.gui.ventana_principal import VentanaPrincipal


def main():
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
