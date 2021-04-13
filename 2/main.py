#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
# QT
from PyQt5.QtGui        import *
from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
# Selfmade
from facedet            import *

class facesWindowSettings():

    def __init__(self, X_offset, Y_offset, Width, Height,
                imagesTypes, acceptButtonWidth):
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.Width = Width
        self.Height = Height
        self.imagesTypes = imagesTypes
        self.acceptButtonWidth = acceptButtonWidth

class facesWindow(QWidget):

    chosen_files = {
        't': {'target': '', 'standard': ''},
        'v': {'target': ''},
        's': {'target': ''},
    }

    def __init__(self, Settings):
        super().__init__()
        self.Settings = Settings
        self.initUI()

    def initUI(self):
        self.acceptButtonText = 'Подтвердить'
        self.chooseButtonText = 'Выберите файл'

        # TemplateMatching tab
        self.t_buttons = {}
        self.t_label = QLabel(self)
        self.t_tab = QFrame()
        self.t_vLayout = QVBoxLayout()
        # Viola-Jones tab
        self.v_buttons = {}
        self.v_label = QLabel(self)
        self.v_tab = QFrame()
        self.v_vLayout = QVBoxLayout()
        # SymmetryLines tab
        self.s_buttons = {}
        self.s_label = QLabel(self)
        self.s_tab = QFrame()
        self.s_vLayout = QVBoxLayout()
        # Main tab
        self.tab = QTabWidget()

        # TemplateMatching tab

        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self.t_on_click_main)
        self.t_buttons['accept'] = accept

        chooseStandard = QPushButton(self.chooseButtonText + ' эталона')
        chooseStandard.clicked.connect(self.t_on_click_chooseStandard)
        self.t_buttons['chooseStandard'] = chooseStandard

        chooseTarget = QPushButton(self.chooseButtonText + ' фотографии')
        chooseTarget.clicked.connect(self.t_on_click_chooseTarget)
        self.t_buttons['chooseTarget'] = chooseTarget

        self.t_vLayout.addWidget(self.t_buttons['chooseStandard'])
        self.t_vLayout.addWidget(self.t_buttons['chooseTarget'])
        self.t_vLayout.addWidget(self.t_buttons['accept'],
                alignment=Qt.AlignCenter | Qt.AlignTop)
        self.t_tab.setLayout(self.t_vLayout)

        # Viola-Jones tab

        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self.v_on_click_main)
        self.v_buttons['accept'] = accept

        choose = QPushButton(self.chooseButtonText)
        choose.clicked.connect(self.v_on_click_choose)
        self.v_buttons['choose'] = choose

        self.v_vLayout.addWidget(self.v_buttons['choose'])
        self.v_vLayout.addWidget(self.v_buttons['accept'],
                alignment=Qt.AlignCenter | Qt.AlignTop)
        self.v_tab.setLayout(self.v_vLayout)

        # SymmetryLines tab

        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self.s_on_click_main)
        self.s_buttons['accept'] = accept

        choose = QPushButton(self.chooseButtonText)
        choose.clicked.connect(self.s_on_click_choose)
        self.s_buttons['choose'] = choose

        self.s_vLayout.addWidget(self.s_buttons['choose'])
        self.s_vLayout.addWidget(self.s_buttons['accept'],
                alignment=Qt.AlignCenter | Qt.AlignTop)
        self.s_tab.setLayout(self.s_vLayout)

        # Main tab

        self.tab.addTab(self.t_tab, "Template matching")
        self.tab.addTab(self.v_tab, "Виола-Джонс")
        self.tab.addTab(self.s_tab, "Линии симметрии")

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tab)
        self.setLayout(main_layout)

        # Window settings

        self.setGeometry(self.Settings.X_offset, self.Settings.Y_offset,
                        self.Settings.Width, self.Settings.Height)
        self.setWindowTitle('Детекция лиц')
        self.show()

    def clear_chosen_files(self):
        self.chosen_files = {
        't': {'target': '', 'standard': ''},
        'v': {'target': ''},
        's': {'target': ''},
        }

    def t_on_click_main(self):
        self.t_label.clear()
        image = template_matching(self.chosen_files['t']['target'], self.chosen_files['t']['standard'])
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = QImage.rgbSwapped(image)
        pixmap = QPixmap.fromImage(image)
        self.t_label.setPixmap(pixmap)
        self.t_vLayout.addWidget(self.t_label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.t_tab.setLayout(self.t_vLayout)
        self.clear_chosen_files()
        self.t_buttons['chooseStandard'].setText(self.chooseButtonText + ' эталона')
        self.t_buttons['chooseTarget'].setText(self.chooseButtonText + ' фотографии')

    def t_on_click_chooseStandard(self):
        file_path = QFileDialog.getOpenFileName(self, self.chooseButtonText,
                None, 'Images (' + self.Settings.imagesTypes + ')')[0]
        self.chosen_files['t']['standard'] = file_path
        file_name = file_path.split('/')[-1]
        self.t_buttons['chooseStandard'].setText(file_name)

    def t_on_click_chooseTarget(self):
        file_path = QFileDialog.getOpenFileName(self, self.chooseButtonText,
                None, 'Images (' + self.Settings.imagesTypes + ')')[0]
        self.chosen_files['t']['target'] = file_path
        file_name = file_path.split('/')[-1]
        self.t_buttons['chooseTarget'].setText(file_name)

    def v_on_click_main(self):
        self.v_label.clear()
        image = viola_jones(self.chosen_files['v']['target'])
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = QImage.rgbSwapped(image)
        pixmap = QPixmap.fromImage(image)
        self.v_label.setPixmap(pixmap)
        self.v_vLayout.addWidget(self.v_label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.v_tab.setLayout(self.v_vLayout)
        self.clear_chosen_files()
        self.v_buttons['choose'].setText(self.chooseButtonText)

    def v_on_click_choose(self):
        file_path = QFileDialog.getOpenFileName(self, self.chooseButtonText,
                None, 'Images (' + self.Settings.imagesTypes + ')')[0]
        self.chosen_files['v']['target'] = file_path
        file_name = file_path.split('/')[-1]
        self.v_buttons['choose'].setText(file_name)

    def s_on_click_main(self):
        self.s_label.clear()
        image = symmetry_lines(self.chosen_files['s']['target'])
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        image = QImage.rgbSwapped(image)
        pixmap = QPixmap.fromImage(image)
        self.s_label.setPixmap(pixmap)
        self.s_vLayout.addWidget(self.s_label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.s_tab.setLayout(self.s_vLayout)
        self.clear_chosen_files()
        self.s_buttons['choose'].setText(self.chooseButtonText)

    def s_on_click_choose(self):
        file_path = QFileDialog.getOpenFileName(self, self.chooseButtonText,
                None, 'Images (' + self.Settings.imagesTypes + ')')[0]
        self.chosen_files['s']['target'] = file_path
        file_name = file_path.split('/')[-1]
        self.s_buttons['choose'].setText(file_name)

    def on_click_t(self):
        file1 = QFileDialog.getOpenFileName(self, self.chooseButtonText,
                None, 'Images (' + self.Settings.imagesTypes + ')')[0]
        self.btn_t.setText(file1)
        self.label.clear()
        print(file1)
        pass
        # file1 = QFileDialog.getOpenFileName(self, 'Choose image', None, 'Images (*.png *.xpm *.jpg)')[0]
        # file2 = QFileDialog.getOpenFileName(self, 'Choose template', None, 'Images (*.png *.xpm *.jpg)')[0]
        # self.label.clear()
        # image = template_matching.template_matching(file1, file2)
        # height, width, channel = image.shape
        # bytesPerLine = 3 * width
        # image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # image = QImage.rgbSwapped(image)
        # pixmap = QPixmap.fromImage(image)
        # self.label.setPixmap(pixmap)
        # self.label.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())
        # self.layout_tab_1.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)
        # self.tab_1.setLayout(self.layout_tab_1)

    def on_click_v(self):
        pass
        # file = QFileDialog.getOpenFileName(self, 'Choose image', None, 'Images (*.png *.xpm *.jpg)')[0]
        # self.label2.clear()
        # image = ViolaJones.viola_jones(file)
        # height, width, channel = image.shape
        # bytesPerLine = 3 * width
        # image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # image = QImage.rgbSwapped(image)
        # pixmap = QPixmap.fromImage(image)
        # self.label2.setPixmap(pixmap)
        # self.label2.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())
        # self.layout_tab_2.addWidget(self.label2, alignment=Qt.AlignCenter | Qt.AlignTop)
        # self.tab_2.setLayout(self.layout_tab_2)

    def on_click_s(self):
        pass
        # file = QFileDialog.getOpenFileName(self, 'Choose image', None, 'Images (*.png *.xpm *.jpg)')[0]
        # self.label3.clear()
        # image = symmetryLines.symmetryLines(file)
        # height, width, channel = image.shape
        # bytesPerLine = 3 * width
        # image = QImage(image.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # image = QImage.rgbSwapped(image)
        # pixmap = QPixmap.fromImage(image)
        # self.label3.setPixmap(pixmap)
        # self.label3.resize(pixmap.width(), pixmap.height())
        # self.resize(pixmap.width(), pixmap.height())
        # self.layout_tab_3.addWidget(self.label3, alignment=Qt.AlignCenter | Qt.AlignTop)
        # self.tab_3.setLayout(self.layout_tab_3)

if __name__ == '__main__':
    app = QApplication([])
    settings = facesWindowSettings(200, 120, 1000, 700, '*.png *.jpg', 150)
    widget = facesWindow(settings)
    widget.show()
    sys.exit(app.exec_())