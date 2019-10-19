import math
import random
from collections import deque

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QFont
from PyQt5.QtCore import QTimer, pyqtSlot as Slot, QRect, Qt, QPointF, QDir



class MainWindow(QWidget):
    TIMER_INTERVAL = 500
    RIGHT_OFFSET = 200
    HISTORY_SIZE = 500

    BLACK = (0, 0, 0)

    def __init__(self):
        super().__init__()

        self.initUI()
        self.board = '*'* 34 * 34
        self.n = 34
        self.data = []
        self.history = deque(maxlen=self.HISTORY_SIZE)
        self.freeze = False
        self.freeze_index = 0

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Main window')
        # self.setWindowIcon(QIcon('web.png'))
        self.font = QFont()
        self.font.setFamily("Sans Mono")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(self.TIMER_INTERVAL)

        self.show()

    def update(self, data):
        if not self.freeze:
            self.data = data
            self.history.append(data)
            self.freeze_index = len(self.history) - 1

    @Slot()
    def on_timer_timeout(self):
        self.repaint()


    def keyPressEvent(self, event):
        print(event)
        key = event.key()
        if key == Qt.Key_Right:
            self.freeze_index = min(max(0, self.freeze_index + 1), len(self.history)-1)
            self.data = self.history[self.freeze_index]
        elif key == Qt.Key_Left:
            self.freeze_index = min(max(0, self.freeze_index - 1), len(self.history)-1)
            self.data = self.history[self.freeze_index]
        elif key == Qt.Key_Space:
            self.freeze = not self.freeze
            self.freeze_index = len(self.history) - 1
            self.data = self.history[self.freeze_index]
        elif key == Qt.Key_Return:
            pass
        else:
            print('key pressed: %s' % key)
        pass

    # @Sls('key pressed: %i' % event)

    def hdata(self, row, col):
        return self.board[row * self.n + col]

    def hpos(self, row, col):
        return self.cell_width * col, self.cell_height * row

    def cell_rect(self, x, y):
        return self.hpos(y, x) + (self.cell_width, self.cell_height)

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
        self.setWindowTitle(f'freeze={self.freeze} i={self.freeze_index} last={len(self.history)-1}')
        painter = QPainter()
        painter.begin(self)
        painter.setFont(self.font)
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

    def setPen(self, painter, item):
        color = [max(0, min(255, int(c))) for c in item['color']]
        painter.setPen(QPen(QColor(*color)))

    def drawLine(self, painter, item):
        painter.setPen(QPen(QColor(*item.get('color', self.BLACK))))
        painter.drawLine(item['x1'] * self.cell_width + self.cell_half_width,
                         item['y1'] * self.cell_height + self.cell_half_height,
                         item['x2'] * self.cell_width + self.cell_half_width,
                         item['y2'] * self.cell_height + self.cell_half_height)

    def drawRect(self, painter, item):
        painter.drawRect(item['x'] * self.cell_width,
                         item['y'] * self.cell_height,
                         self.cell_width,
                         self.cell_height)

    def drawText(self, painter, item):
        painter.drawText(
            QRect(*self.cell_rect(item['x'], item['y'])),
            Qt.AlignCenter,
            item['text']
        )

    def drawBoard(self, painter, item):
        self.board = item['board']
        self.n = int(math.sqrt(len(self.board)))

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
                    QRect(*self.cell_rect(col, row)),
                    Qt.AlignCenter,
                    ch
                )
