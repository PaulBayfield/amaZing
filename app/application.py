from app import Menu, Maze, ConvertMazet2Image, User, __version__

from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QSize, QTimer, QRectF
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QBrush, QPainterPath, QPixmap
from qframelesswindow import FramelessWindow


import os, sys
import keyboard
import asyncio
import pygame

from datetime import timedelta
from PIL.ImageQt import ImageQt
from threading import Thread


class Labyrinthe(FramelessWindow):
    def __init__(self):
        super().__init__()
        self._menuOpened = False
        self._infoMenuOpened = False
        self._mousePressed = False
        self._maximized = False
        self._cornerRadius = 8.0

        self.POPUPWIDTH = 220


        # Chemin des 'assets'
        self.pathAssets = self.resource_path('assets')

        # Music
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.load(f'{self.pathAssets}\\bubblerythmunit-a.wav')
        pygame.mixer.music.play(-1)


        # Fenetre 
        self.setWindowTitle("SAE Labyrinthe")
        self.setWindowIcon(QIcon(f"{self.pathAssets}\\icon.ico"))

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setStyleSheet("background:transparent")

        self.default_width = 680
        self.default_height = 400
        self.resize(self.default_width, self.default_height)
        self.setMinimumSize(680, 270)


        # Ajout des composants, boutons, etc...
        self.setupComponents()
        self.hook = keyboard.on_press(self.keyboardEvent)


        # Laby Data
        self.loaded = False
        self.image = None
        self.user = None


        Thread(target=self.runLoadMaze, ).start()


        # Timer
        self.task = QTimer(self)
        self.task.timeout.connect(self.mainTask)
        self.task.start(1000)

        self.timerTime = 0
        self.timerIndex = 0
        self.timerLight = 0
        self.timerBlock = 0


        self.labyWidth = 10
        self.labyHeight = 10


    def runLoadMaze(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.loadMaze())
        loop.close()


    def mainTask(self):
        if self.user and self.user.alive:
            if self.image.block:
                self.timerBlock += 1

                if self.timerBlock == 3:
                    self.image.block = False
                    self.timerBlock = 0
                    asyncio.run(self.user.refresh())

            if self.user.light:
                self.timerLight += 1

                if self.timerLight == 7:
                    self.user.light = False
                    self.timerLight = 0
                    self.user.radius -= 20
                    self.user.updateRadius()
                    self.user.updateBonus()
                    asyncio.run(self.user.refresh())

            self.timerTime += 1

            if self.timerIndex == 0:
                self.timerIcon.setIcon(QIcon(f"{self.pathAssets}\\icons\\hourglass-start.svg"))
            elif self.timerIndex == 1:
                self.timerIcon.setIcon(QIcon(f"{self.pathAssets}\\icons\\hourglass-half.svg"))
            elif self.timerIndex == 2:
                self.timerIcon.setIcon(QIcon(f"{self.pathAssets}\\icons\\hourglass-end.svg"))

            self.timerIndex += 1
            if self.timerIndex > 2:
                self.timerIndex = 0
                
            self.timerBox.setText(str(timedelta(seconds=self.timerTime)))


    def setupComponents(self):
        self.menuButton = QPushButton(self)
        self.menuButton.setIcon(QIcon(f"{self.pathAssets}\\iut.png"))
        self.menuButton.setToolTip('Menu')
        self.menuButton.setGeometry(4, 4, 30, 30)
        self.menuButton.setIconSize(QSize(25, 25))
        self.menuButton.setStyleSheet("""
            QPushButton {
                background-color: lightgray; 
                border-radius: 8px;
            }
            QPushButton::hover {
                background-color: gray; 
                border-radius: 8px;
            }
        """)
        self.menuButton.clicked.connect(self.open_menu)
        self.menuButton.setFocusPolicy(Qt.NoFocus)

        self.title = QLabel(self)
        self.title.setText("amaZing")
        self.title.setStyleSheet("""
            QLabel {
                font-size: 27px;
                color: qlineargradient(x1:200, x2:1, stop:0 rgba(89, 221, 224, 255), stop:1 rgba(44, 169, 239, 255));
                font-weight: bold;
                background-color: #616161;
            }
        """)
        self.title.adjustSize()
        self.title.setGeometry(40, 1, 160, 34)
        self.title.setFocusPolicy(Qt.NoFocus)

        self.timerBox = QLineEdit(self)
        self.timerBox.setText("0:00:00")
        self.timerBox.setEnabled(False)
        self.timerBox.setStyleSheet("""
            QLineEdit {
                color: white;
                border-width: 2px; 
                border-radius: 10px;
                border-style: solid; 
                border-color: gray; 
                padding-left: 20px;
                padding-top: -2px;
                font-weight: bold;
            }
        """)
        self.timerBox.setFocusPolicy(Qt.NoFocus)

        self.timerIcon = QPushButton(QIcon(f"{self.pathAssets}\\icons\\hourglass-start.svg"), "", self)
        self.timerIcon.setIconSize(QSize(14, 14))
        self.timerIcon.setStyleSheet("""
            QPushButton::hover {
                padding-left: 1px; 
                padding-top: 1px;
            }
        """)
        self.timerIcon.setFocusPolicy(Qt.NoFocus)


        self.reloadButton = QPushButton(self)
        self.reloadButton.setIcon(QIcon(f"{self.pathAssets}\\icons\\reload.svg"))
        self.reloadButton.setToolTip('Restart')
        self.reloadButton.setIconSize(QSize(20, 20))
        self.reloadButton.setStyleSheet("""
            QPushButton::hover {
                background-color: #73737391; 
                border-radius: 8px;
            }
        """)
        self.reloadButton.clicked.connect(self.reset)
        self.reloadButton.setFocusPolicy(Qt.NoFocus)


        self.label = QLabel(self)
        self.pixmap = QPixmap(f"{self.pathAssets}\\loading.png")
        self.label.setPixmap(self.pixmap)
        

        self.characterLife = QLabel(self)
        self.characterLife.setText("Health:")
        self.characterLife.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.characterLife.adjustSize()
        self.characterLife.move(10, 50)
        self.characterLife.setFocusPolicy(Qt.NoFocus)


        self.characterCoins = QLabel(self)
        self.characterCoins.setText("Coins:")
        self.characterCoins.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.characterCoins.adjustSize()
        self.characterCoins.move(10, 70)
        self.characterCoins.setFocusPolicy(Qt.NoFocus)


        self.characterRadius = QLabel(self)
        self.characterRadius.setText("Vision:")
        self.characterRadius.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.characterRadius.adjustSize()
        self.characterRadius.move(10, 90)
        self.characterRadius.setFocusPolicy(Qt.NoFocus)
        
        
        self.characterBonus = QLabel(self)
        self.characterBonus.setText("Bonus:")
        self.characterBonus.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.characterBonus.adjustSize()
        self.characterBonus.move(10, 110)
        self.characterBonus.setFocusPolicy(Qt.NoFocus)


        self.characterLevel = QLabel(self)
        self.characterLevel.setText("Level 0")
        self.characterLevel.setStyleSheet("""
            QLabel {
                font-size: 20px;
                color: white;
                font-weight: bold;
            }
        """)
        self.characterLevel.adjustSize()
        self.characterLevel.setFocusPolicy(Qt.NoFocus)


        self.buyVision = QLabel(self)
        self.buyVision.setAlignment(Qt.AlignRight)
        self.buyVision.setText("Extra Vision [V]:")
        self.buyVision.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.buyVision.setFocusPolicy(Qt.NoFocus)


        self.buyLife = QLabel(self)
        self.buyLife.setAlignment(Qt.AlignRight)
        self.buyLife.setText("Extra Life [E]:")
        self.buyLife.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.buyLife.setFocusPolicy(Qt.NoFocus)


        self.buyPath = QLabel(self)
        self.buyPath.setAlignment(Qt.AlignRight)
        self.buyPath.setText("Exit Path [P]:")
        self.buyPath.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        self.buyPath.setFocusPolicy(Qt.NoFocus)


        self.minimizebutton = QPushButton(self)
        self.minimizebutton.setIcon(QIcon(f"{self.pathAssets}\\icons\\minimize.svg"))
        self.minimizebutton.setToolTip('Minimize')
        self.minimizebutton.setIconSize(QSize(20, 20))
        self.minimizebutton.setStyleSheet("""
            QPushButton::hover {
                background-color: #73737391; 
                border-radius: 8px;
            }
        """)
        self.minimizebutton.clicked.connect(self.window().showMinimized)
        self.minimizebutton.setFocusPolicy(Qt.NoFocus)

        self.maximizebutton = QPushButton(self)
        self.maximizebutton.setIcon(QIcon(f"{self.pathAssets}\\icons\\maximize.svg"))
        self.maximizebutton.setToolTip('Maximize')
        self.maximizebutton.setIconSize(QSize(20, 20))
        self.maximizebutton.setStyleSheet("""
            QPushButton::hover {
                background-color: #73737391; 
                border-radius: 8px;
            }
        """)
        self.maximizebutton.clicked.connect(self.maxi)
        self.maximizebutton.setFocusPolicy(Qt.NoFocus)

        self.exitbutton = QPushButton(self)
        self.exitbutton.setIcon(QIcon(f"{self.pathAssets}\\icons\\close.svg"))
        self.exitbutton.setToolTip('Quit')
        self.exitbutton.setIconSize(QSize(30, 30))
        self.exitbutton.setStyleSheet("""
            QPushButton::hover {
                background-color: red; 
                border-radius: 8px;
            }
        """)
        self.exitbutton.clicked.connect(self.close)
        self.exitbutton.setFocusPolicy(Qt.NoFocus)


    def updateGeometry(self):
        self.timerIcon.setGeometry(223, 10, 19, 19)
        self.timerBox.setGeometry(220, 8, 90, 23)

        self.reloadButton.setGeometry(180, 4, 30, 30)
        
        self.buyVision.setGeometry(self.width()-190, 50, 180, 20)
        self.buyLife.setGeometry(self.width()-190, 70, 180, 20)
        self.buyPath.setGeometry(self.width()-190, 90, 180, 20)
        
        self.characterLevel.move(self.width()//2-30, self.height()-30)

        if self.pixmap.height() > self.height() - 70:
            self.pixmap = self.pixmap.scaled(self.height()-100, self.height()-100, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label.setPixmap(self.pixmap)

        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.move(self.width()//2-self.pixmap.width()//2, self.height()//2-self.pixmap.height()//2+15)


        self.minimizebutton.setGeometry(self.size().width() - 94, 4, 30, 30)
        self.maximizebutton.setGeometry(self.size().width() - 64, 4, 30, 30)
        self.exitbutton.setGeometry(self.size().width() - 34, 4, 30, 30)

        if self._menuOpened:
            self.open_menu()
            self.open_menu()

            self.menu.close_menu.setGeometry(self.POPUPWIDTH, 4, self.width(), self.height())

            if self._infoMenuOpened:
                self.menu.infoMenu.setGeometry(self.POPUPWIDTH, 34, self.width(), self.height())

        asyncio.run(self.updateLabyImage())


    async def loadMaze(self):
        await self.updateLabyImage()

        self.laby = Maze.gen_exploration(self.labyWidth, self.labyHeight)

        self.image = ConvertMazet2Image(self, self.laby)
        await self.image.generateImage()
        await self.image.generateItems()


        if self.user:
            coins = self.user.coins
            hearts = self.user.hearts
            radius = self.user.radius
            level = self.user.level + 1
            radiusPrices = self.user.radiusPrices

            self.user = User(self.image, coins=coins, hearts=hearts, radius=radius, level=level, radiusPrices=radiusPrices)
        else:
            self.user = User(self.image)

        self.user.display()
        await self.user.move((0, 0))


        self.loaded = True
        await self.updateLabyImage()


    async def updateLabyImage(self):
        if self.image and self.loaded:
            if not self.user.alive:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(f'{self.pathAssets}\\bubblerythmunit-d.wav')
                pygame.mixer.music.play(-1)

                self.pixmap = QPixmap.fromImage(ImageQt(f"{self.pathAssets}\\died.png"))
            else:
                self.pixmap = QPixmap.fromImage(ImageQt(self.image.image))
        else:
            self.pixmap = QPixmap(f"{self.pathAssets}\\loading.png")
        self.label.setPixmap(self.pixmap)

        if self.pixmap.height() > self.height() - 70:
            self.pixmap = self.pixmap.scaled(self.height()-100, self.height()-100, Qt.KeepAspectRatio, Qt.FastTransformation)
            self.label.setPixmap(self.pixmap)

        self.label.resize(self.pixmap.width(), self.pixmap.height())
        self.label.move(self.width()//2-self.pixmap.width()//2, self.height()//2-self.pixmap.height()//2+15)

    
    def keyboardEvent(self, event):
        if event.event_type == 'down' and self.user and self.loaded and self.user.alive and not self._menuOpened:
            if self.image.block:
                self.image.block = False
                self.timerBlock = 0

            if event.name == 'haut':
                self.user.checkMove(0, -1)
                asyncio.run(self.updateLabyImage())
            elif event.name == 'bas':
                self.user.checkMove(0, 1)
                asyncio.run(self.updateLabyImage())
            elif event.name == 'gauche':
                self.user.checkMove(-1, 0)
                asyncio.run(self.updateLabyImage())
            elif event.name == 'droite':
                self.user.checkMove(1, 0)
                asyncio.run(self.updateLabyImage())
            elif event.name == 'v':
                self.user.buyRange()
                self.user.updateRadius()
                asyncio.run(self.user.refresh())
            elif event.name == 'e':
                self.user.buyHeart()
            elif event.name == 'p':
                self.user.buyPath()


    def resizeEvent(self, event):
        self.updateGeometry()
        
    
    def maxi(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
            
        self.updateGeometry()


    def show_window(self):
        self.window().showNormal()


    def destroy_window(self):
        self.close()


    def open_menu(self):
        if not self._menuOpened:
            self.menu = Menu(self)
            self.menu.move(0, 34)
            self.menu.resize(self.width(), self.height())
            self.menu.SIGNALS.CLOSE.connect(self.close_menu)
            self._menuOpened = True
            self.menu.show()

            if self._infoMenuOpened:
                self._infoMenuOpened = False
                self.menu.openInfo()
        else:
            if self._infoMenuOpened:
                self.menu.close_infoMenu(disable=False)
            self.close_menu()


    def close_menu(self):
        self.menu.close()
        self._menuOpened = False

        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    def paintEvent(self, event):
        x = -1
        width = self.size().width()

        painter = QPainter(self)
        painter.setPen(QPen(QColor("#616161"), 2))
        painter.setBrush(QBrush(QColor("#616161")))
        painter.setOpacity(1)
        painter.setRenderHints(QPainter.Antialiasing)


        path = QPainterPath()
        rect = self.rect()
        path.addRoundedRect(QRectF(rect), self._cornerRadius, self._cornerRadius)
        painter.drawPath(path)


        painter.setPen(QPen(QColor("#ffffff"), 1))
        painter.setOpacity(0.8)
        painter.drawRect(x, 36, width, 1)

        painter.end()

        
    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self.pos()
        self._mouseY = event.y()


    def mouseMoveEvent(self, event):
        if self._mousePressed and self._mouseY < 36:
            if bool(self.windowState() & Qt.WindowMaximized):
                self.setWindowState(Qt.WindowNoState)

            self.move(self._windowPos + (event.globalPos() - self._mousePos))


    def mouseReleaseEvent(self, event):
        self._mousePressed = False

        rect = self.geometry()

        if rect.y() < 0:
            difference = abs(0-rect.y())
            rect.setY(0)
            rect.setHeight(rect.height() + difference)
            self.setGeometry(rect)


    def mouseDoubleClickEvent(self, event):
        if event.y() < 36:
            self.maxi()

            if self._menuOpened:
                self.menu.resize(self.width(), self.height())


    def reset(self):
        self.loaded = False
        self.image = None
        self.user = None

        Thread(target=self.runLoadMaze, ).start()
            
        self.timerTime = 0
        self.timerIndex = 0
        self.timerLight = 0
        self.timerBlock = 0

        self.labyWidth = 10
        self.labyHeight = 10

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.load(f'{self.pathAssets}\\bubblerythmunit-a.wav')
        pygame.mixer.music.play(-1)
