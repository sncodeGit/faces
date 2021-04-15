#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
# QT
from PyQt5.QtGui        import *
from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
# Selfmade
from faceclass          import *

class facesWindowSettings():

    def __init__(self, X_offset, Y_offset, Width, Height,
                acceptButtonWidth):
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.Width = Width
        self.Height = Height
        self.acceptButtonWidth = acceptButtonWidth

class facesWindow(QWidget):

    def __init__(self, Settings):
        super().__init__()
        self.Settings = Settings
        self.initUI()

    def initUI(self):
        self.acceptButtonText = 'Запустить'
        self.methods_list = ['histogram', 'dft', 'dct', 'gradient', 'scale']
        self.num_elements_list = list(map(str, range(1, 10)))
        self.title_col_list = ['train', 'histogram', 'dft', 'dct',
                'gradient', 'scale', 'голосование']

        # 1 step
        self._1_label = QLabel(self)
        self._1_tab = QFrame()
        self._1_vLayout = QVBoxLayout()
        self._1_checkbox_num_elements = QComboBox(self)
        self._1_checkbox_methods = QComboBox(self)
        self._1_textbox_accuracy = QLineEdit()
        self._1_textbox_parametr = QLineEdit()
        self._1_lbl_pixmap_1 = QLabel(self)
        self._1_lbl_pixmap_2 = QLabel(self)
        self._1_lbl_pixmap_3 = QLabel(self)
        self._1_lbl_plot_1 = QLabel(self)
        self._1_lbl_plot_2 = QLabel(self)
        self._1_lbl_plot_3 = QLabel(self)
        # 2 step
        self._2_label = QLabel(self)
        self._2_tab = QFrame()
        self._2_vLayout = QVBoxLayout()
        self._2_checkbox_methods = QComboBox(self)
        self._2_parambox = []
        self._2_accuracybox = []
        self._2_lbl_pixmap_cross = QLabel(self)
        # 3 step
        self._3_label = QLabel(self)
        self._3_tab = QFrame()
        self._3_vLayout = QVBoxLayout()
        self._3_textbox_matrix = []
        self._3_col_num = 7
        self._3_str_num = 10
        self._3_lbl_plot = QLabel(self)
        # self._3_parambox = []
        # Main tab
        self.tab = QTabWidget()

        # 1 step

        self._1_checkbox_methods.addItems(self.methods_list)
        self._1_checkbox_methods.setEditable(True)
        line_edit = self._1_checkbox_methods.lineEdit()
        line_edit.setText('Выберите метод')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._1_vLayout.addWidget(self._1_checkbox_methods)

        self._1_checkbox_num_elements.addItems(self.num_elements_list)
        self._1_checkbox_num_elements.setEditable(True)
        line_edit = self._1_checkbox_num_elements.lineEdit()
        line_edit.setText('Выберите количество элементов из сэмпла для обучения')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._1_vLayout.addWidget(self._1_checkbox_num_elements)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._1_on_click_calculate)
        hLayout.addWidget(accept)
        self._1_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        self._1_textbox_accuracy.setText('accuracy')
        self._1_textbox_accuracy.setAlignment(Qt.AlignCenter)
        self._1_textbox_accuracy.setReadOnly(True)
        hLayout.addWidget(self._1_textbox_accuracy)
        self._1_textbox_parametr.setText('Параметр')
        self._1_textbox_parametr.setAlignment(Qt.AlignCenter)
        hLayout.addWidget(self._1_textbox_parametr)
        self._1_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        accept = QPushButton('Смотреть примеры')
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._1_on_click_examples)
        hLayout.addWidget(accept)
        self._1_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._1_lbl_pixmap_1)
        hLayout.addWidget(self._1_lbl_pixmap_2)
        hLayout.addWidget(self._1_lbl_pixmap_3)
        hLayout.setAlignment(Qt.AlignCenter)
        self._1_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._1_lbl_plot_1)
        hLayout.addWidget(self._1_lbl_plot_2)
        hLayout.addWidget(self._1_lbl_plot_3)
        hLayout.setAlignment(Qt.AlignCenter)
        self._1_vLayout.addLayout(hLayout)

        self._1_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._1_tab.setLayout(self._1_vLayout)

        # 2 step

        self._2_checkbox_methods.addItems(self.methods_list)
        self._2_checkbox_methods.setEditable(True)
        line_edit = self._2_checkbox_methods.lineEdit()
        line_edit.setText('Выберите метод')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._2_vLayout.addWidget(self._2_checkbox_methods)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._2_on_click)
        hLayout.addWidget(accept)
        self._2_vLayout.addLayout(hLayout)

        self._2_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._2_tab.setLayout(self._2_vLayout)

        hLayoutTitle = QHBoxLayout()
        hLayoutParams = QHBoxLayout()
        hLayoutAccuracy = QHBoxLayout()

        for i in range(0, 3):
            for j in range(0, self._3_str_num):
                textbox = QLineEdit()
                textbox.setAlignment(Qt.AlignCenter)
                if (i == 0):
                    if (j == 0):
                        textbox.setText('train')
                    else:
                        textbox.setText(str(j))
                    textbox.setReadOnly(True)
                    hLayoutTitle.addWidget(textbox)
                if (i == 1):
                    if (j == 0):
                        textbox.setText('param')
                    self._2_parambox.append(textbox)
                    hLayoutParams.addWidget(textbox)
                    textbox.setReadOnly(True)
                if (i == 2):
                    if (j == 0):
                        textbox.setText('accuracy')
                    self._2_accuracybox.append(textbox)
                    hLayoutAccuracy.addWidget(textbox)
                    textbox.setReadOnly(True)
            self._2_vLayout.addLayout(hLayoutTitle)
            self._2_vLayout.addLayout(hLayoutParams)
            self._2_vLayout.addLayout(hLayoutAccuracy)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._2_lbl_pixmap_cross)
        hLayout.setAlignment(Qt.AlignCenter)
        self._2_vLayout.addLayout(hLayout)

        # 3 step

        # hLayoutTitle = QHBoxLayout()
        # hLayoutParams = QHBoxLayout()

        # for i in range(0, 2):
        #     for j in range(1, self._3_col_num - 1):
        #         textbox = QLineEdit()
        #         textbox.setAlignment(Qt.AlignCenter)
        #         if (i == 0):
        #             textbox.setText(self.title_col_list[j] + ' параметр')
        #             textbox.setReadOnly(True)
        #             hLayoutTitle.addWidget(textbox)
        #         if (i == 1):
        #             self._3_parambox.append(textbox)
        #             hLayoutParams.addWidget(textbox)
        #     self._3_vLayout.addLayout(hLayoutTitle)
        #     self._3_vLayout.addLayout(hLayoutParams)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._3_on_click)
        hLayout.addWidget(accept)
        self._3_vLayout.addLayout(hLayout)

        layout = QGridLayout()
        for i in range(1, self._3_col_num):
            layout.setColumnStretch(i,2)

        for string in range(0, self._3_str_num):
            textbox_str = []
            for column in range(0, self._3_col_num):
                textbox = QLineEdit()
                if (string != 0) and (column == 0):
                    textbox.setText(str(string))
                if (string == 0):
                    textbox.setText(self.title_col_list[column])
                textbox.setAlignment(Qt.AlignCenter)
                textbox.setReadOnly(True)
                layout.addWidget(textbox)
                textbox_str.append(textbox)
            self._3_textbox_matrix.append(textbox_str)

        self._3_vLayout.addLayout(layout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._3_lbl_plot)
        hLayout.setAlignment(Qt.AlignCenter)
        self._3_vLayout.addLayout(hLayout)

        self._3_vLayout.setAlignment(Qt.AlignTop)
        self._3_tab.setLayout(self._3_vLayout)

        # Main tab

        self.tab.addTab(self._1_tab, "Поиск лучшего параметра")
        self.tab.addTab(self._2_tab, "Кросс-валидация")
        self.tab.addTab(self._3_tab, "Голосование методов")

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.tab)
        self.setLayout(main_layout)

        # Window settings

        self.setGeometry(self.Settings.X_offset, self.Settings.Y_offset,
                        self.Settings.Width, self.Settings.Height)
        self.setWindowTitle('Практика 3: классификация лиц')
        self.show()

    def _1_on_click_calculate(self):
        data = get_data()
        data_train, data_test = get_split_data(data,
                10 - int(self._1_checkbox_num_elements.currentText()))
        best_p, accuracy = get_best_params(data_train, data_test,
                eval('get_' + self._1_checkbox_methods.currentText()))
        self._1_textbox_accuracy.setText(str(accuracy))
        self._1_textbox_parametr.setText(str(best_p))

    def _1_on_click_examples(self):
        data = get_data()
        samples, r = get_samples(data)
        samples = samples[0]
        images = random.choices(samples, k=3)
        for i in range(3):
            image = cv2.resize(images[i], (110, 110), interpolation=cv2.INTER_AREA)
            cv2.imwrite('photo.jpg', 255*image)
            pixmap = QPixmap('photo.jpg')
            eval(f'self._1_lbl_pixmap_{i+1}').setPixmap(pixmap)
            eval(f'self._1_lbl_pixmap_{i+1}').adjustSize()
            method = 'get_' + self._1_checkbox_methods.currentText()
            method = eval(method)
            if method == get_histogram:
                hist, bins = get_histogram(images[i], int(self._1_textbox_parametr.text()))
                hist = np.insert(hist, 0, 0.0)
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.plot(bins, hist)
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)
            elif method == get_dct or method == get_dft:
                ex = method(images[i], int(self._1_textbox_parametr.text()))
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.pcolormesh(range(ex.shape[0]), range(ex.shape[0]), np.flip(ex, 0))
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)
            elif method == get_scale:
                image = method(images[i], float(self._1_textbox_parametr.text()))
                cv2.imwrite('plot.png', 255 * image)
            else:
                ex = method(images[i], int(self._1_textbox_parametr.text()))
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.plot(range(0, len(ex)), ex)
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)

            pixmap1 = QPixmap('plot.png')
            eval(f'self._1_lbl_plot_{i+1}').setPixmap(pixmap1)
            eval(f'self._1_lbl_plot_{i+1}').adjustSize()

    def _2_on_click(self):
        data = get_data()
        method = eval('get_' + self._2_checkbox_methods.currentText())
        ans, ps = get_cross(data, method)
        fig, ax = plt.subplots(figsize=(3.2, 2.5))
        plt.plot(range(1, len(ans)+1), ans)
        plt.grid(True)
        plt.xlabel("Number of test")
        plt.ylabel("Accuracy")
        plt.savefig('plot1.png')
        plt.close()
        pixmap2 = QPixmap('plot1.png')
        self._2_lbl_pixmap_cross.setPixmap(pixmap2)
        self._2_lbl_pixmap_cross.adjustSize()
        for i in range(1, 10):
            if method == get_scale:
                self._2_parambox[i].setText(str(round(ps[i - 1], 3)))
            else:
                self._2_parambox[i].setText(str(ps[i - 1]))
            self._2_accuracybox[i].setText(str(round(ans[i - 1], 3)))

    def _3_on_click(self):
        data = get_data()
        accuracy = []
        ps = []
        for i in range(9, 0, -1):
            data_train, data_test = get_split_data(data, i)
            r, p = get_vote(data_train, data_test)
            a = accuracy_score(r, data_test[1])
            p.append(a)
            accuracy.append(a)
            ps.append(p)

        fig, ax = plt.subplots(figsize=(3.2, 2.5))
        plt.plot(range(1, len(accuracy) + 1), accuracy)
        plt.grid(True)
        plt.xlabel("Number of test")
        plt.ylabel("Accuracy")
        plt.savefig('plot1.png')
        plt.close()
        pixmap2 = QPixmap('plot1.png')
        self._3_lbl_plot.setPixmap(pixmap2)
        self._3_lbl_plot.adjustSize()
        for string in range(1, self._3_str_num):
            for column in range(1, self._3_col_num):
                self._3_textbox_matrix[string][column].setText(
                    str(round(ps[string - 1][column - 1], 3))
                )

if __name__ == '__main__':
    app = QApplication([])
    settings = facesWindowSettings(500, 120, 1000, 700, 200)
    widget = facesWindow(settings)
    widget.show()
    sys.exit(app.exec_())