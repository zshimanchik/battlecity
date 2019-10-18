import random
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import QTimer, pyqtSlot as Slot, QRect, Qt, QPointF, QDir

from visualizer_server.receiver import Receiver


class MainWindow(QWidget):
    TIMER_INTERVAL = 500
    RIGHT_OFFSET = 200

    BLACK = (0, 0, 0)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.board = '*'* 34 * 34
        self.n = 34
        self.data = []

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Main window')
        # self.setWindowIcon(QIcon('web.png'))

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(self.TIMER_INTERVAL)

        self.show()

    @Slot()
    def on_timer_timeout(self):
        self.repaint()

    def hdata(self, row, col):
        return self.board[row * self.n + col]

    def hpos(self, row, col):
        return self.cell_width * col, self.cell_height * row

    def cell_rect(self, row, col):
        return self.hpos(row, col) + (self.cell_width, self.cell_height)

    @property
    def cell_width(self):
        return (self.width() - self.RIGHT_OFFSET) // self.n

    @property
    def cell_height(self):
        return self.height() // self.n

    @property
    def cell_half_width(self):
        return self.cell_width // 2

    @property
    def cell_half_height(self):
        return self.cell_height // 2

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        print_buffer = []
        try:
            painter.setRenderHint(QPainter.Antialiasing)
            for item in self.data:
                cmd = item['cmd']
                if cmd == 'print':
                    print_buffer.append(item['text'])
                elif hasattr(self, cmd):
                    getattr(self, cmd)(painter, item)

            if print_buffer:
                painter.drawText(QRect(self.width() - self.RIGHT_OFFSET, 0,
                                       self.RIGHT_OFFSET, self.height()),
                                 Qt.AlignTop,
                                 '\n'.join(print_buffer))

            # painter.setRenderHintenderHint(QPainter.Antialiasing)
            # painter.drawText(QRect(0, 0, 100, 100), Qt.AlignTop, "Qt")
            # painter.setPen(Qt.NoPen)

        finally:
            painter.end()

    def drawLine(self, painter, item):
        painter.setPen(QPen(QColor(*item.get('color', self.BLACK))))
        painter.drawLine(item['col1'] * self.cell_width + self.cell_half_width,
                         item['row1'] * self.cell_height + self.cell_half_height,
                         item['col2'] * self.cell_width + self.cell_half_width,
                         item['row2'] * self.cell_height + self.cell_half_height)

    def drawBoard(self, painter, item):
        self.board = item['board']

        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setBrush(QBrush(QColor(0, random.randint(0, 255), 255, 15)))
        for row in range(self.n):
            for col in range(self.n):
                # painter.setBrush(QBrush(QColor(0, random.randint(0, 255), 255, 255)))
                painter.setBrush(Qt.NoBrush)

                ch = self.hdata(row, col)
                # print(self.cell_rect(row, col), ch)
                # painter.drawEllipse(QRect(*self.cell_rect(row, col)))
                painter.drawText(
                    QRect(*self.cell_rect(row, col)),
                    Qt.AlignCenter,
                    ch
                )


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainWindow()
    receiver = Receiver(ex)
    flask_thread = Thread(target=receiver.run)
    flask_thread.start()
    sys.exit(app.exec_())
