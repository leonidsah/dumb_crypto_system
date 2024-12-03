import random

import qrcode
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QImage, QColor
from PyQt5.uic.Compiler.qtproxies import QtCore


class QRImage(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size, qrcode_modules):
        # assigning border
        self.border = border

        # assigning  width
        self.width = width

        # assigning box size
        self.box_size = box_size

        # creating size
        size = (width + border * 2) * box_size

        # image
        self._image = QImage(size, size, QImage.Format_RGB16)
        self._image.fill(QColor.fromRgb(239,239,239))


    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.black
        )

def generate_qr_data(length=6):
    return ''.join(random.choice('0123456789') for _ in range(length))

def get_pixmap(data) -> QPixmap:
    return qrcode.make(data, image_factory=QRImage).pixmap()