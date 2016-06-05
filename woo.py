import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QApplication, QBoxLayout)
from PyQt5.QtCore import (qAbs, QLineF, QPointF, QRectF, qrand, qsrand, Qt,
        QTime, QTimer, QSize)
from PyQt5.QtGui import QColor, QPainter, QPalette, QPen
from PyQt5.QtGui import (QBrush, QColor, QPainter, QPainterPath, QPixmap,
        QPolygonF)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsRectItem, QGraphicsScene,
        QGraphicsView, QGridLayout, QGraphicsWidget, QScrollArea, QPushButton)
from PyQt5.QtGui import QPixmap, QImage, qRgb
import numpy as np
import h5py
from fylm.model.color import Color

green = QColor(50, 250, 50)
red = QColor(250, 50, 50)
gfp = Color(30, 250, 30)


class Example(QGraphicsRectItem):
    def __init__(self, rect):
        super().__init__(rect)
        self._top_left = rect.topLeft()
        self._bottom_right = rect.bottomRight()

    @property
    def bounds(self):
        coords = [self._top_left.x(), self._top_left.y(), self._bottom_right.x(), self._bottom_right.y()]
        return tuple(map(int, coords))


class PositiveExample(Example):
    def __init__(self, rect):
        super().__init__(rect)
        self.setPen(green)


class NegativeExample(Example):
    def __init__(self, rect):
        super().__init__(rect)
        self.setPen(red)


class FYLMGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(QRectF(0, 0, 1080, 1280))
        self.setScene(self.scene)

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        polygon = self.mapToScene(float(x), float(y), float(25), float(25))
        if event.button() == 1:
            # left click
            rect = PositiveExample(polygon.boundingRect())
        elif event.button() == 2:
            # right click
            rect = NegativeExample(polygon.boundingRect())
        else:
            # get out of here, middle click
            return
        self.scene.addItem(rect)


class WooButton(QPushButton):
    def __init__(self):
        super().__init__("Woo")
        self.clicked.connect(self.woo)

    def woo(self):
        print("\n".join(dir(self)))
        self.setText("Wooooooooo")


class DoneButton(QPushButton):
    def __init__(self):
        super().__init__("Done")
        self.clicked.connect(self.done)

    def done(self):
        print("done")


class DirectionButton(QPushButton):
    def __init__(self, direction):
        assert direction in ('<', '>')
        super().__init__(direction)
        action = self._left if direction == '<' else self._right
        self.clicked.connect(action)

    def sizeHint(self):
        return QSize(50, 25)

    def _left(self):
        pass

    def _right(self):
        pass


class ButtonRowLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.addWidget(DoneButton())
        self.addWidget(DirectionButton('<'))
        self.addWidget(QLabel("1/13"))
        self.addWidget(DirectionButton('>'))


if __name__ == '__main__':

    app = QApplication(sys.argv)

    with h5py.File("/var/fylm3/FYLM-160329.h5", "a") as h5:
        image = h5['/%d/%s/%d' % (0, "BF", 0)]['0'].value
        image = ((image / np.max(image)) * 255).astype(np.uint8)

    qim = QImage(image, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Indexed8)
    # gray_color_table = [qRgb(i, i, i) for i in range(256)]
    # qim = QImage(combo.data, combo.shape[1], combo.shape[0], combo.strides[0], QImage.Format_RGB888)
    # qim.setColorTable(gray_color_table)
    minimage = np.copy(image[400:600, 400:800])
    miniqim = QImage(minimage, minimage.shape[1], minimage.shape[0], minimage.strides[0], QImage.Format_Indexed8)

    pixmap = QPixmap.fromImage(qim).scaled(1080, 1280)
    view = FYLMGraphicsView()
    view.scene.addPixmap(pixmap)

    minpixmap = QPixmap.fromImage(miniqim)
    miniview = QLabel()
    miniview.setPixmap(minpixmap)

    graphics_layout = QVBoxLayout()
    graphics_layout.addWidget(view)
    window = QWidget()
    layout = QVBoxLayout()
    layout.addItem(graphics_layout)
    layout.addItem(ButtonRowLayout())
    layout.addWidget(miniview)
    window.setLayout(layout)
    window.show()
    app.exec_()
    # for item in view.scene.items():
    #     if type(item) not in (NegativeExample, PositiveExample):
    #         continue
    #     x1, y1, x2, y2 = item.bounds
