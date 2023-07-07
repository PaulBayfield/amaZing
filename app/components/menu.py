from app import __version__


from PyQt5.QtWidgets import QWidget, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt, QObject, QSize
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QPainterPath


import webbrowser


class WidgetSignals(QObject):
    CLOSE = pyqtSignal()

class Menu(QWidget):
    def __init__(self, window):
        super(Menu, self).__init__(window)
        self.win = window
        

        # Background Button to close the Popup Menu
        self.close_menu = QPushButton("", self)
        self.close_menu.setGeometry(self.win.POPUPWIDTH, 4, self.win.width(), self.win.height())
        self.close_menu.clicked.connect(self._onclose)


        textStyle = """
            QLabel {
                color: black; 
                padding-left: 35px;
                font-size: 22px;
                font-weight: bold;
                background-color: transparent;
            }
        """

        buttonStyle = """
            QPushButton {
                padding-right: 150px;
                background-color: transparent;
            }
            QPushButton::hover {
                background-color: #73737391;
                border-radius: 8px;
                padding-right: 150px;
            }
        """
        
        
        text = QLabel("À Propos", self)
        text.adjustSize()
        text.setStyleSheet(textStyle)
        text.setGeometry(20, 11, 190, 40)

        text = QLabel("Gitlab", self)
        text.adjustSize()
        text.setStyleSheet(textStyle)
        text.setGeometry(20, 56, 190, 40)
        
        text = QLabel("Site", self)
        text.adjustSize()
        text.setStyleSheet(textStyle)
        text.setGeometry(20, 101, 190, 40)

        text = QLabel("Discord", self)
        text.adjustSize()
        text.setStyleSheet(textStyle)
        text.setGeometry(20, 146, 190, 40)


        self.infoButton = QPushButton(self)
        self.infoButton.setIcon(QIcon(f"{self.win.pathAssets}/icons/info.svg"))
        self.infoButton.setToolTip('À Propos')
        self.infoButton.setIconSize(QSize(24, 24))
        self.infoButton.clicked.connect(self.openInfo)
        self.infoButton.setGeometry(15, 12, 190, 40)
        self.infoButton.setStyleSheet(buttonStyle)
        self.infoButton.setFocusPolicy(Qt.NoFocus)

        self.gitlabButton = QPushButton(self)
        self.gitlabButton.setIcon(QIcon(f"{self.win.pathAssets}/icons/gitlab.svg"))
        self.gitlabButton.setToolTip('Help & Information')
        self.gitlabButton.setToolTip('https://gitlab.com/paul.bayfield/amazing')
        self.gitlabButton.setIconSize(QSize(24, 24))
        self.gitlabButton.clicked.connect(lambda: webbrowser.open('https://gitlab.com/paul.bayfield/amazing'))
        self.gitlabButton.setGeometry(15, 57, 190, 40)
        self.gitlabButton.setStyleSheet(buttonStyle)
        self.gitlabButton.setFocusPolicy(Qt.NoFocus)

        self.websiteButton = QPushButton(self)
        self.websiteButton.setIcon(QIcon(f"{self.win.pathAssets}/icons/website.svg"))
        self.websiteButton.setToolTip('https://www.iut-rcc.fr/')
        self.websiteButton.setIconSize(QSize(24, 24))
        self.websiteButton.clicked.connect(lambda: webbrowser.open('https://www.iut-rcc.fr/'))
        self.websiteButton.setGeometry(15, 102, 190, 40)
        self.websiteButton.setStyleSheet(buttonStyle)
        self.websiteButton.setFocusPolicy(Qt.NoFocus)

        self.discordButton = QPushButton(self)
        self.discordButton.setIcon(QIcon(f"{self.win.pathAssets}/icons/discord.svg"))
        self.discordButton.setToolTip('https://discord.gg/qRqwTrQFPY')
        self.discordButton.setIconSize(QSize(24, 24))
        self.discordButton.clicked.connect(lambda: webbrowser.open('https://discord.gg/qRqwTrQFPY'))
        self.discordButton.setGeometry(15, 147, 190, 40)
        self.discordButton.setStyleSheet(buttonStyle)
        self.discordButton.setFocusPolicy(Qt.NoFocus)
       
        
        label = QLabel("amaZing", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 27px;
                color: qlineargradient(x1:200, x2:1, stop:0 rgba(89, 221, 224, 255), stop:1 rgba(44, 169, 239, 255));
                font-weight: bold;
                background-color: transparent;
            }
        """)
        label.move(30, self.win.size().height()-70)

        label = QLabel(f"v{__version__}", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #2CA9EF;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        label.move(150, self.win.size().height()-57)
        

        self.SIGNALS = WidgetSignals()

        
    def openInfo(self):
        if not self.win._infoMenuOpened:
            self.infoMenu = Info(self.win)
            self.infoMenu.setGeometry(self.win.POPUPWIDTH, 34, self.win.width(), self.win.height())
            self.infoMenu.SIGNALS.CLOSE.connect(self.close_infoMenu)
            self.win._infoMenuOpened = True
            self.infoMenu.show()
        else:
            self.close_infoMenu()


    def close_infoMenu(self, disable: bool = True):
        self.infoMenu.close()
        if disable:
            self.win._infoMenuOpened = False


    def paintEvent(self, event):
        x = -1
        y = 3
        width = self.win.POPUPWIDTH
        height = self.size().height()-36
        
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.setPen(QPen(QColor("lightgray"), 1))
        painter.setBrush(QColor("lightgray"))

        # Menu
        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x, y + (height - 2 * self.win._cornerRadius))
        path.arcTo(x, y + (height - 2 * self.win._cornerRadius), 2 * self.win._cornerRadius, 2 * self.win._cornerRadius, 180.0, 90.0)
        path.lineTo(width, y + height)
        path.lineTo(width, y)
        path.lineTo(x + self.win._cornerRadius, y)

        painter.drawPath(path)

        painter.end()

    
    def _onclose(self):
        self.SIGNALS.CLOSE.emit()


class Info(QWidget):
    def __init__(self, parent):
        super(Info, self).__init__(parent)
        self.win = parent


        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon(f"{self.win.pathAssets}/icons/exit.svg"))
        self.closeButton.setToolTip('Close the Help')
        self.closeButton.setGeometry(400, 15, 24, 24)
        self.closeButton.setIconSize(QSize(24, 24))
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: transparent;
            }
            QPushButton::hover {
                background-color: gray;
                border-radius: 8px;
            }
        """)
        self.closeButton.clicked.connect(self.close_info)

        label = QLabel("amaZing", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                color: qlineargradient(x1:200, x2:1, stop:0 rgba(89, 221, 224, 255), stop:1 rgba(44, 169, 239, 255));
                font-weight: bold;
                background-color: transparent;
            }
        """)
        label.move(20, 15)


        textStyle = """
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
                background-color: transparent;
            }
        """

        label = QLabel("Fait par BAYFIELD Paul et RATTANAVONG LOUIS en", self)
        label.setStyleSheet(textStyle)
        label.move(20, 50)

        label = QLabel("Python.", self)
        label.setStyleSheet(textStyle)
        label.move(20, 70)

        label = QLabel("Pistes audios composées par xtrem-dm (#la Bulle)", self)
        label.setStyleSheet(textStyle)
        label.move(20, 105)

        label = QLabel("> https://soundcloud.com/xtrem-dm", self)
        label.setStyleSheet(textStyle)
        label.move(20, 125)

        label = QLabel("Liste des items disponible en jeu :", self)
        label.setStyleSheet(textStyle)
        label.move(20, 160)

        label = QLabel("> https://gitlab.com/paul.bayfield/amazing", self)
        label.setStyleSheet(textStyle)
        label.move(20, 180)

        self.SIGNALS = WidgetSignals()


    def close_info(self):
        self.win._infoMenuOpened = False
        self.close()


    def paintEvent(self, event):
        x = -1
        y = 3
        width = self.size().width() - self.win.POPUPWIDTH
        height = self.size().height() - 34
        
        painter = QPainter(self)
        painter.setOpacity(0.8)
        painter.setPen(QPen(QColor("lightgray"), 1))
        painter.setBrush(QColor("lightgray"))

        path = QPainterPath()
        path.moveTo(x, y)
        path.lineTo(x, height)
        path.lineTo(width - 2 * self.win._cornerRadius, height)
        path.arcTo(width - 2 * self.win._cornerRadius, y + (height - 2 * self.win._cornerRadius), 2 * self.win._cornerRadius, 2 * self.win._cornerRadius, 270.0, 90.0)
        path.lineTo(width, y)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.drawPath(path)


        painter.setBrush(QColor("#5b5f62"))
        painter.setOpacity(0.8)
        painter.drawRoundedRect(10, 10, 420, 200, 20.0, 20.0)

        painter.end()


    def _onclose(self):
        self.SIGNALS.CLOSE.emit()
