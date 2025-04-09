# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 15:48:10 2025

@author: e183630
"""
#---------------------------------------------------------------------#
import numpy as np
import matplotlib.pyplot as plt
import sys
#---------------------------------------------------------------------#
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox, QWidget, QVBoxLayout, QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem 
from PyQt6.QtGui import QAction, QPixmap, QPainter
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from io import BytesIO
#---------------------------------------------------------------------#

class InteractiveGraphicsView(QGraphicsView):
    """ Vue interactive permettant le zoom et le déplacement """
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)  # Déplacement au clic

    def wheelEvent(self, event):
        """ Zoom avec la molette de la souris """
        factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
        self.scale(factor, factor)

class MyWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
    
        self.Central_Widget = QWidget(self)
        self.setCentralWidget(self.Central_Widget)
        
        self.init_ui()

    def init_ui(self):
        # Paramètres de la fenêtre
        self.setWindowTitle("AftErWIN")

        

        layout = QVBoxLayout(self.Central_Widget)
        layout.setContentsMargins(50,50,50,50)
        # ✅ Création de la scène et de la vue
        self.scene = QGraphicsScene()
        self.view = InteractiveGraphicsView(self.scene)
        layout.addWidget(self.view)

        self.plot_graph()
        self.create_menubar()  # ✅ Création du menu correctement appelée
        

    def create_menubar(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)  # ✅ Affichage dans la fenêtre sur Mac
        
        file_menu = menu_bar.addMenu("Fichier")


        new_action = QAction('Nouveau Layout', self)
        open_action = QAction("Ouvrir Layout", self)
        save_action = QAction("Enregistrer Layout", self)
        open_files = QAction("Ouvrir des des documents signaux", self)
        close_action = QAction("Quitter", self)

        new_action.triggered.connect(self.new_action)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        open_files.triggered.connect(self.open_files)
        close_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(open_files)
        file_menu.addSeparator()
        file_menu.addAction(close_action)

        file_menu = menu_bar.addMenu("propriété")

        hardware = QAction('Hardware', self)
        Materiau = QAction('Matériau', self)

        hardware.triggered.connect(self.hardware)
        Materiau.triggered.connect(self.Materiau)

        file_menu.addAction(hardware)
        file_menu.addAction(Materiau)


        file_menu = menu_bar.addMenu("aide")

        preference = QAction('préference', self)
        credit = QAction('crédit', self)

        preference.triggered.connect(self.preference)
        credit.triggered.connect(self.credit)

        file_menu.addAction(preference)
        file_menu.addSeparator()
        file_menu.addAction(credit)

    def new_action(self):
        QMessageBox.information(self,"nouveau", "nouveau layout")
    def open_file(self):
        QMessageBox.information(self, "Ouvrir", "Ouvrir document")  # ✅ Correction

    def save_file(self):
        QMessageBox.information(self, "Sauvegarde", "Sauvegarder document")  # ✅ Correction

    def credit(self):
        QMessageBox.information(self, "Sauvegarde", "Sauvegarder document")
    
    def open_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un fichier", 
            "", 
            "Fichiers Texte (*.txt);;Fichiers CSV (*.csv);;Tous les fichiers (*)",
            None
        )



        if file_path:  # Vérifie si un fichier a été sélectionné
            print(f"Fichier sélectionné : {file_path}")  # Affichage dans la console

    def hardware(self):
        QMessageBox.information(self, "Sauvegarde", "Sauvegarder document")
    
    def Materiau(self):
        QMessageBox.information(self, "Sauvegarde", "Sauvegarder document")


    def preference(self):
        QMessageBox.information(self, "Sauvegarde", "Sauvegarder document")

#-----------------------------------------------------------------------------------------------------------------------------#
   
    def plot_graph(self):
        x = np.linspace(0, 10, 100)
        y = np.sin(x)  # Exemple : courbe sinusoïdale

        fig,self.ax = plt.subplots(figsize=(5,3),dpi = 100)
        self.ax.clear()  # Efface l'ancien graphique
        self.ax.plot(x, y, label="sin(x)", color="blue")
        self.ax.set_title("Waveforms")
        self.ax.set_xlabel("time(µs)")
        self.ax.set_ylabel("Voltage (V)")
        self.ax.legend()

        #convertir la figure en graphique

        buf = BytesIO()
        fig.savefig(buf, format = "png", bbox_inches ="tight")
        buf.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(buf.getvalue())

        #ajuster l'image à la scene
        self.scene.clear()
        self.scene.addPixmap(pixmap)

#-----------------------------------------------------------------------------------------------------------------------------#

# Lancer l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
