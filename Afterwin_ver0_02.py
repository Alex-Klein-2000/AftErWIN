import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog, QGraphicsScene,
    QGraphicsView, QGraphicsProxyWidget, QGraphicsItem
)
#-------------------------------------------------------------------------------------------#
from PyQt6.QtGui import QAction, QPainter
from PyQt6.QtCore import Qt, QRectF, QSize
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
#-------------------------------------------------------------------------------------------#
# file reader
def lire_fichier(fichier):
    donnees =[]
    with open(fichier, 'r') as f:
        reader = csv.reader(f)
        for ligne in reader:
            donnees.append(ligne)
        datafile = []
        for i in donnees:
            try: 
                datafile.append(float(i[0]))
            except:
                continue
    return datafile
#-------------------------------------------------------------------------------------------#
#waveforms plotter
class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.fig, (self.ax_signal,self.ax_phase) = plt.subplots(2,1,figsize=(5, 3), dpi=100,gridspec_kw={"height_ratios":[3,2]})
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.plot_graph()

    def plot_graph(self,datafile=None):

        if datafile:
            x = np.linspace(0, 100, len(datafile))
            y = datafile
            self.ax_signal.clear()
            self.ax_signal.plot(x, y, label="waveform", color="blue")
            self.ax_signal.set_title("Waveforms")
            self.ax_signal.set_xlabel("time (µs)")
            self.ax_signal.set_ylabel("Voltage (V)")
            self.ax_signal.legend()
            self.canvas.draw() 

            fft_data = np.fft.fft(y)
            phase = np.unwrap(np.angle(fft_data))
            freq = np.fft.fftfreq(len(y), d=(x[1] - x[0]))

            self.ax_phase.clear()
            self.ax_phase.plot(freq, phase, color="green", label="Phase")
            self.ax_phase.set_title("Phase du signal")
            self.ax_phase.set_xlabel("Fréquence (Hz)")
            self.ax_phase.set_ylabel("Phase (rad)")
            self.ax_phase.legend()

        else:
            x = np.linspace(0, 10, 100)
            y = np.sin(x)
            self.ax_signal.clear()
            self.ax_signal.plot(x, y, label="sin(x)", color="blue")
            self.ax_signal.set_title("Waveforms")
            self.ax_signal.set_xlabel("time (µs)")
            self.ax_signal.set_ylabel("Voltage (V)")
            self.ax_signal.legend()
            self.canvas.draw()

            fft_data = np.fft.fft(y)
            phase = np.unwrap(np.angle(fft_data))
            freq = np.fft.fftfreq(len(y), d=(x[1] - x[0]))

            self.ax_phase.clear()
            self.ax_phase.plot(freq, phase, color="green", label="Phase")
            self.ax_phase.set_title("Phase du signal")
            self.ax_phase.set_xlabel("Fréquence (Hz)")
            self.ax_phase.set_ylabel("Phase (rad)")
            self.ax_phase.legend()

class ResizableProxyWidget(QGraphicsProxyWidget):
    MARGIN = 8

    def __init__(self, widget):
        super().__init__()
        self.setWidget(widget)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)
        self._resizing = False
        self._resize_direction = None

    def hoverMoveEvent(self, event):
        rect = self.boundingRect()
        pos = event.pos()
        margin = self.MARGIN

        if abs(pos.x() - rect.left()) < margin:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self._resize_direction = 'left'
        elif abs(pos.x() - rect.right()) < margin:
            self.setCursor(Qt.CursorShape.SizeHorCursor)
            self._resize_direction = 'right'
        elif abs(pos.y() - rect.top()) < margin:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self._resize_direction = 'top'
        elif abs(pos.y() - rect.bottom()) < margin:
            self.setCursor(Qt.CursorShape.SizeVerCursor)
            self._resize_direction = 'bottom'
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._resize_direction = None

    def mousePressEvent(self, event):
        if self._resize_direction:
            self._resizing = True
            self._start_pos = event.pos()
            self._start_rect = self.rect()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing:
            delta = event.pos() - self._start_pos
            new_rect = QRectF(self._start_rect)

            if self._resize_direction == 'right':
                new_rect.setRight(new_rect.right() + delta.x())
            elif self._resize_direction == 'left':
                new_rect.setLeft(new_rect.left() + delta.x())
            elif self._resize_direction == 'bottom':
                new_rect.setBottom(new_rect.bottom() + delta.y())
            elif self._resize_direction == 'top':
                new_rect.setTop(new_rect.top() + delta.y())

            min_size = QSize(100, 80)
            if new_rect.width() >= min_size.width() and new_rect.height() >= min_size.height():
                self.widget().resize(int(new_rect.width()), int(new_rect.height()))
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None
        super().mouseReleaseEvent(event)

class DraggableGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene())
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.init_matplotlib_widget()

    def init_matplotlib_widget(self):
        self.matplotlib_widget = MatplotlibWidget()
        self.proxy = ResizableProxyWidget(self.matplotlib_widget)
        self.scene().addItem(self.proxy)
        self.proxy.setPos(50, 50)

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AftErWIN")
        self.setGeometry(50, 50, 1200, 700)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(50, 50, 50, 50)
        self.graphics_view = DraggableGraphicsView()
        layout.addWidget(self.graphics_view)
        self.create_menubar()

    def create_menubar(self):
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        file_menu = menu_bar.addMenu("Fichier")
        open_files = QAction("Ouvrir des documents signaux", self)
        close_action = QAction("Quitter", self)
        open_files.triggered.connect(self.open_files)
        close_action.triggered.connect(self.close)
        file_menu.addAction(open_files)
        file_menu.addSeparator()
        file_menu.addAction(close_action)

    def open_files(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier",
            "",
            "Fichiers Texte (*.txt);;Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        if file_path:
            print(f"Fichier sélectionné : {file_path}")
            try:
                datafile = lire_fichier(file_path)
                self.graphics_view.matplotlib_widget.plot_graph(datafile)
            except Exception as e:
                print(f"Erreur lors de la lecture : {e}")
            
        
        return(datafile)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())