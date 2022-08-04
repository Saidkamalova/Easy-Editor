import os


from PyQt5.QtWidgets import (
    QApplication, QWidget,
    QFileDialog,  # Диалог открытия файлов (и папок)
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt  # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap  # оптимизированная для показа на экране картинка

from PIL import Image
from PIL.ImageFilter import SHARPEN
from PyQt5 import QtGui

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setStyleSheet("color: yellow;"
                  "background-color: #F4F1B7;"
                  "border : 1px solid lime;")



win.setWindowTitle('Easy Editor')
lb_image = QLabel("Картинка")
btn_dir = QPushButton("Folders")
btn_dir.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_dir.setStyleSheet("background-color: #ACEF8A;"
                      "color: #64765A;"
                      "border: 2px solid red;"


                      )
lw_files = QListWidget()

btn_left = QPushButton("Left")
btn_left.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_left.setStyleSheet("background-color: #ACEF8A;"
                        "color: red;"
"width: 200px;"

                       )
btn_right = QPushButton("Right")
btn_right.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_right.setStyleSheet("background-color: #ACEF8A;"
                        )
btn_flip = QPushButton("Mirror")
btn_flip.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_flip.setStyleSheet("background-color: #ACEF8A;"
                       )
btn_sharp = QPushButton("Sharpness")
btn_sharp.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_sharp.setStyleSheet("background-color: #ACEF8A;"
                        )
btn_bw = QPushButton("B/W")
btn_bw.setFont(QtGui.QFont("Algerian", weight=QtGui.QFont.Bold))
btn_bw.setStyleSheet("background-color: #ACEF8A;"
                     )

row = QHBoxLayout()  # Основная строка
col1 = QVBoxLayout()  # делится на два столбца
col2 = QVBoxLayout()
col1.addWidget(btn_dir)  # в первом - кнопка выбора директории
col1.addWidget(lw_files)  # и список файлов
col2.addWidget(lb_image, 95)  # вo втором - картинка
row_tools = QHBoxLayout()
# и строка кнопок
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1, 20)
row.addLayout(col2, 80)
win.setLayout(row)

win.show()

workdir = ''


def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)


btn_dir.clicked.connect(showFilenamesList)


class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadimage(self, dir, filename):
        self.dir = dir  # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation
        self.filename = filename  # /field.png
        image_path = os.path.join(dir, filename)  # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\field.png
        self.image = Image.open(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified\field.png
        self.showimage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showimage(image_path)

    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir((path))
        image_path = os.path.join(path, self.filename)
        # C:\Users\bilol\Desktop\start2\Part 3\Part 3\my vacation\Modified\field.png
        self.image.save(image_path)

    def showimage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()


def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimage.loadimage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showimage(image_path)


workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharpen)
btn_flip.clicked.connect(workimage.do_flip)

app.exec()

