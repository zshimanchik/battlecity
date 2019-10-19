import sys

from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from receiver import Receiver

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    receiver = Receiver(window)

    receiver.start()
    code = app.exec_()

    print(f'code {code}')
    receiver.shutdown()
    sys.exit(0)
