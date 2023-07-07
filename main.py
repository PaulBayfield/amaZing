from app.application import Labyrinthe


from PyQt5.QtWidgets import QApplication


import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Labyrinthe()
    window.show()
            
    sys.exit(app.exec_())
