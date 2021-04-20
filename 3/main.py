#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import numpy as np
# QT
from PyQt5.QtGui        import *
from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from statistics         import mean
# Selfmade
from faceclass          import *

class facesWindowSettings():

    def __init__(self, X_offset, Y_offset, Width, Height,
                acceptButtonWidth, plotPause):
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.Width = Width
        self.Height = Height
        self.acceptButtonWidth = acceptButtonWidth
        self.plotPause = plotPause

class facesWindow(QWidget):

    def __init__(self, Settings):
        super().__init__()
        self.Settings = Settings
        self.initUI()

    def initUI(self):
        self.acceptButtonText = 'Принять'
        self.methods_list = ['histogram', 'dft', 'dct', 'gradient', 'scale']
        self.voting_methods_list = ['histogram', 'dft', 'dct', 'gradient', 'scale', 'voting']
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
        self._3_parambox = []
        # 4 step
        self._4_label = QLabel(self)
        self._4_tab = QFrame()
        self._4_vLayout = QVBoxLayout()
        self._4_lbl_pixmap_1 = QLabel(self)
        self._4_lbl_pixmap_2 = QLabel(self)
        self._4_lbl_pixmap_3 = QLabel(self)
        self._4_lbl_plot_1 = QLabel(self)
        self._4_lbl_plot_2 = QLabel(self)
        self._4_lbl_plot_3 = QLabel(self)
        self._4_checkbox_methods = QComboBox(self)
        self._4_textbox_parametr = QLineEdit()
        # 5 step
        self._5_label = QLabel(self)
        self._5_tab = QFrame()
        self._5_vLayout = QVBoxLayout()
        self._5_lbl_pixmap_1 = QLabel(self)
        self._5_lbl_pixmap_2 = QLabel(self)
        self._5_lbl_plot_1 = QLabel(self)
        self._5_lbl_plot_2 = QLabel(self)
        self._5_checkbox_num_elements = QComboBox(self)
        self._5_checkbox_methods = QComboBox(self)
        self._5_textbox_parametr = QLineEdit()
        self._5_exnum_parametr = QLineEdit()
        # 6 step
        self._6_label = QLabel(self)
        self._6_tab = QFrame()
        self._6_vLayout = QVBoxLayout()
        self._6_checkbox_num_elements = QComboBox(self)
        self._6_textboxes_accuracy = []
        for i in range(6):
            self._6_textboxes_accuracy.append(QLineEdit())
        self._6_textboxes_param = []
        for i in range(6):
            self._6_textboxes_param.append(QLineEdit())
        self._6_textboxes_method = []
        for i in range(6):
            self._6_textboxes_method.append(QLineEdit())

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

        self._2_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._2_tab.setLayout(self._2_vLayout)

        # 3 step

        # hLayoutTitle = QHBoxLayout()
        # hLayoutParams = QHBoxLayout()

        # for i in range(0, 1):
        #     for j in range(1, self._3_col_num - 1):
        #         textbox = QLineEdit()
        #         textbox.setAlignment(Qt.AlignCenter)
        #         if (i == 0):
        #             textbox.setText(self.title_col_list[j] + ' параметр')
        #             # textbox.setReadOnly(True)
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
                # textbox.setReadOnly(True)
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

        # 4 step

        self._4_checkbox_methods.addItems(self.methods_list)
        self._4_checkbox_methods.setEditable(True)
        line_edit = self._4_checkbox_methods.lineEdit()
        line_edit.setText('Выберите метод')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._4_vLayout.addWidget(self._4_checkbox_methods)

        self._4_textbox_parametr.setText('Параметр')
        self._4_textbox_parametr.setAlignment(Qt.AlignCenter)
        self._4_vLayout.addWidget(self._4_textbox_parametr)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._4_on_click_examples)
        hLayout.addWidget(accept)
        self._4_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._4_lbl_pixmap_1)
        hLayout.addWidget(self._4_lbl_pixmap_2)
        hLayout.addWidget(self._4_lbl_pixmap_3)
        hLayout.setAlignment(Qt.AlignCenter)
        self._4_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._4_lbl_plot_1)
        hLayout.addWidget(self._4_lbl_plot_2)
        hLayout.addWidget(self._4_lbl_plot_3)
        hLayout.setAlignment(Qt.AlignCenter)
        self._4_vLayout.addLayout(hLayout)

        self._4_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._4_tab.setLayout(self._4_vLayout)

        # Step 5

        self._5_checkbox_methods.addItems(self.methods_list)
        self._5_checkbox_methods.setEditable(True)
        line_edit = self._5_checkbox_methods.lineEdit()
        line_edit.setText('Выберите метод')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._5_vLayout.addWidget(self._5_checkbox_methods)

        self._5_checkbox_num_elements.addItems(self.num_elements_list)
        self._5_checkbox_num_elements.setEditable(True)
        line_edit = self._5_checkbox_num_elements.lineEdit()
        line_edit.setText('Выберите количество элементов из сэмпла для обучения')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._5_vLayout.addWidget(self._5_checkbox_num_elements)

        self._5_textbox_parametr.setText('Параметр')
        self._5_textbox_parametr.setAlignment(Qt.AlignCenter)
        self._5_vLayout.addWidget(self._5_textbox_parametr)

        self._5_exnum_parametr.setText('Введите номер тестового обьекта (нумерация от 0)')
        self._5_exnum_parametr.setAlignment(Qt.AlignCenter)
        self._5_vLayout.addWidget(self._5_exnum_parametr)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._5_on_click_examples)
        hLayout.addWidget(accept)
        self._5_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._5_lbl_pixmap_1)
        hLayout.addWidget(self._5_lbl_pixmap_2)
        hLayout.setAlignment(Qt.AlignCenter)
        self._5_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(self._5_lbl_plot_1)
        hLayout.addWidget(self._5_lbl_plot_2)
        hLayout.setAlignment(Qt.AlignCenter)
        self._5_vLayout.addLayout(hLayout)

        self._5_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._5_tab.setLayout(self._5_vLayout)

        # 6 step

        self._6_checkbox_num_elements.addItems(self.num_elements_list)
        self._6_checkbox_num_elements.setEditable(True)
        line_edit = self._6_checkbox_num_elements.lineEdit()
        line_edit.setText('Выберите количество элементов из сэмпла для обучения')
        line_edit.setAlignment(Qt.AlignCenter)
        line_edit.setReadOnly(True)
        self._6_vLayout.addWidget(self._6_checkbox_num_elements)

        for (i, method) in zip(range(6), self.voting_methods_list):
            hLayout = QHBoxLayout()
            self._6_textboxes_method[i].setText(method + ':')
            self._6_textboxes_method[i].setAlignment(Qt.AlignCenter)
            self._6_textboxes_method[i].setReadOnly(True)
            hLayout.addWidget(self._6_textboxes_method[i])
            self._6_textboxes_accuracy[i].setText('accuracy')
            self._6_textboxes_accuracy[i].setAlignment(Qt.AlignCenter)
            self._6_textboxes_accuracy[i].setReadOnly(True)
            hLayout.addWidget(self._6_textboxes_accuracy[i])
            if i != 5:
                self._6_textboxes_param[i].setText('Параметр')
                self._6_textboxes_param[i].setAlignment(Qt.AlignCenter)
                hLayout.addWidget(self._6_textboxes_param[i])
            self._6_vLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        accept = QPushButton(self.acceptButtonText)
        accept.setFixedWidth(self.Settings.acceptButtonWidth)
        accept.clicked.connect(self._6_voting)
        hLayout.addWidget(accept)
        self._6_vLayout.addLayout(hLayout)

        self._6_vLayout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self._6_tab.setLayout(self._6_vLayout)

        # Main tab

        self.tab.addTab(self._4_tab, "Примеры")
        self.tab.addTab(self._1_tab,"Лучший параметр")
        self.tab.addTab(self._5_tab, "Похожие")
        self.tab.addTab(self._2_tab, "Кросс-валидация")
        self.tab.addTab(self._6_tab, "Голосование")
        self.tab.addTab(self._3_tab, "Кросс-валидация - голосование")

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
        method = eval('get_' + self._1_checkbox_methods.currentText())
        data_train, data_test = get_split_data(data,
                10 - int(self._1_checkbox_num_elements.currentText()))
        if (self._1_textbox_parametr.text() == '') or (self._1_textbox_parametr.text() == 'Параметр'):
            best_p, accuracy = get_best_params(data_train, data_test, method)
            self._1_textbox_accuracy.setText(str(round(accuracy, 3)))
            self._1_textbox_parametr.setText(str(best_p))
        else:
            if method == get_scale:
                best_p = float(self._1_textbox_parametr.text())
            else:
                best_p = int(self._1_textbox_parametr.text())
            r = classifier(data_train, data_test, method, best_p)
            accuracy = accuracy_score(r, data_test[1])
            self._1_textbox_accuracy.setText(str(round(accuracy, 3)))

        fig = plt.figure()#figsize=(14, 8))
        ax1 = fig.add_subplot(5, 2, 1)
        ax1.set_title('Тестовое фото')
        ax1.axis('off')
        ax2 = fig.add_subplot(5, 2, 2)
        ax2.set_title('Ближайшее фото')
        ax2.axis('off')
        ax3 = fig.add_subplot(4, 2, 3)
        ax3.set_title('Признак на тесте')
        ax4 = fig.add_subplot(4, 2, 4)
        ax4.set_title('Признак на ближайшем')
        # ax3.axis('off')
        # ax4.axis('off')
        ax = fig.add_subplot(2, 1, 2)
        ax.set_xlim(0, len(data_test[0]))
        ax.set_ylim(0, 1.02)
        plt.ion()
        res = []
        for i in range(len(data_test[0])):
            ax1.clear()
            ax2.clear()
            ax3.clear()
            ax4.clear()
            ax.clear()
            ax1.set_title('Тестововое фото')
            ax2.set_title('Ближайшее фото')
            ax3.set_title('Признак на тесте')
            ax4.set_title('Признак на ближайшем')
            ax.set_xlabel('test_num')
            ax.set_ylabel('accuracy')
            ax.set_xlim(0, len(data_test[0]))
            ax.set_ylim(0, 1.02)
            # ax3.axis('off')
            # ax4.axis('off')
            ax1.axis('off')
            ax2.axis('off')
            image = cv2.resize(data_test[0][i], (100, 100), interpolation=cv2.INTER_AREA)
            cv2.imwrite('test.jpg', 255 * image)
            image = plt.imread('test.jpg')
            ax1.imshow(image, cmap='gray')

            ind = closest(data_train, data_test[0][i], method, best_p)
            im = data_train[0][ind]
            if data_test[1][i] == data_train[1][ind]:
                res.append(1)
            else:
                res.append(0)

            ax.plot([i for i in range(len(res))], [mean(res[:i+1]) for i in range(len(res))])

            im = cv2.resize(im, (100, 100), interpolation=cv2.INTER_AREA)
            cv2.imwrite('test.jpg', 255 * im)
            image = plt.imread('test.jpg')
            ax2.imshow(image, cmap='gray')


            self.get_plot(method, data_test[0][i], best_p, ax3)

            self.get_plot(method, im, best_p, ax4)
            plt.pause(self.Settings.plotPause)
            fig.show()
            fig.canvas.draw()

    def _4_on_click_examples(self):
        data = get_data()
        samples, r = get_samples(data)
        samples = samples[0]
        images = random.choices(samples, k=3)
        for i in range(3):
            image = cv2.resize(images[i], (110, 110), interpolation=cv2.INTER_AREA)
            cv2.imwrite('photo.jpg', 255*image)
            pixmap = QPixmap('photo.jpg')
            eval(f'self._4_lbl_pixmap_{i+1}').setPixmap(pixmap)
            eval(f'self._4_lbl_pixmap_{i+1}').adjustSize()
            method = 'get_' + self._4_checkbox_methods.currentText()
            method = eval(method)
            if method == get_histogram:
                hist, bins = get_histogram(images[i], int(self._4_textbox_parametr.text()))
                hist = np.insert(hist, 0, 0.0)
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.plot(bins, hist)
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)
            elif method == get_dct or method == get_dft:
                ex = method(images[i], int(self._4_textbox_parametr.text()))
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.pcolormesh(range(ex.shape[0]), range(ex.shape[0]), np.flip(ex, 0))
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)
            elif method == get_scale:
                image = method(images[i], float(self._4_textbox_parametr.text()))
                cv2.imwrite('plot.png', 255 * image)
            else:
                ex = method(images[i], int(self._4_textbox_parametr.text()))
                fig = plt.figure(figsize=(1.1, 1.1))
                ax = fig.add_subplot(111)
                ax.plot(range(0, len(ex)), ex)
                plt.xticks(color='w')
                plt.yticks(color='w')
                plt.savefig('plot.png')
                plt.close(fig)

            pixmap1 = QPixmap('plot.png')
            eval(f'self._4_lbl_plot_{i+1}').setPixmap(pixmap1)
            eval(f'self._4_lbl_plot_{i+1}').adjustSize()

    def _5_on_click_examples(self):
        method = eval('get_' + self._5_checkbox_methods.currentText())
        if method == get_scale:
            param = float(self._5_textbox_parametr.text())
        else:
            param = int(self._5_textbox_parametr.text())
        test = 10 - int(self._5_checkbox_num_elements.currentText())
        num = int(self._5_exnum_parametr.text())
        data = get_data()
        data_train, data_test = get_split_data(data, test)
        ind = closest(data_train, data_test[0][num], method, param)

        im = cv2.resize(data_test[0][num], (100, 100), interpolation=cv2.INTER_AREA)
        cv2.imwrite('test.jpg', 255 * im)
        pixmap = QPixmap('test.jpg')
        self._5_lbl_pixmap_1.setPixmap(pixmap)
        self._5_lbl_pixmap_1.adjustSize()

        im = cv2.resize(data_train[0][ind], (100, 100), interpolation=cv2.INTER_AREA)
        cv2.imwrite('test.jpg', 255 * im)
        pixmap = QPixmap('test.jpg')
        self._5_lbl_pixmap_2.setPixmap(pixmap)
        self._5_lbl_pixmap_2.adjustSize()

        self.get_plot_1(method, data_test[0][num], param)
        pixmap = QPixmap('plot.png')
        self._5_lbl_plot_1.setPixmap(pixmap)
        self._5_lbl_plot_1.adjustSize()

        self.get_plot_1(method, data_train[0][ind], param)
        pixmap = QPixmap('plot.png')
        self._5_lbl_plot_2.setPixmap(pixmap)
        self._5_lbl_plot_2.adjustSize()

    def _2_on_click(self):
        data = get_data()
        method = eval('get_' + self._2_checkbox_methods.currentText())
        ans, ps = get_cross(data, method)
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        plt.xlim((1, 9))
        plt.plot([i for i in range(1, len(ans) + 1)], ans)
        plt.grid(True)
        plt.title('Кросс-валидация')
        plt.xlabel("train_num")
        plt.ylabel("accuracy")
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
        plot = []
        data = get_data()
        ps = []
        for i in range(9, 0, -1):
            data_train, data_test = get_split_data(data, i)
            # for string in range(1, self._3_str_num):
            #     if (self._3_textbox_matrix[string][1].text() != '') and (self._3_textbox_matrix[string][1].text().find(' | ') == -1):
            #         p = []
            #         a = []
            #         for column in range(1, self._3_col_num - 1):
            #             p.append(self._3_textbox_matrix[string][column])
            #         r = get_vote_1(data_train, data_test, p)
            #     else:
            #         r, a, p = get_vote(data_train, data_test)
            r, a, p = get_vote(data_train, data_test)
            ps.append(p)
            ac = accuracy_score(r, data_test[1])
            a.append(ac)
            plot.append(a)

        fin = []
        for i in range(len(plot)):
            fin.append(plot[i])
            fin.append(ps[i])

        string = 1
        for i in range(len(plot[0])-1):
            column = 1
            for j in range(0, 17, 2):
                self._3_textbox_matrix[column][string].setText(str(round(fin[j][i], 2)) + ' | ' + str(round(fin[j+1][i], 2)))
                column += 1
            string += 1

        for (i, string) in zip(range(9), range(1, self._3_str_num)):
            self._3_textbox_matrix[string][self._3_col_num-1].setText(str(round(plot[i][-1], 2)))

        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        # ax = fig.add_subplot(111)
        plot = np.array(plot)
        plot = plot.transpose()
        for i in plot:
            plt.plot([j for j in range(1, len(i) + 1)], i)
        plt.grid(True)
        plt.legend(["histogram", "dft", "dct", "gradient", "scale", "voting"])
        plt.title('Кросс-валидация')
        plt.xlabel("train_num")
        plt.ylabel("accuracy")
        plt.savefig('plot1.png')
        pixmap = QPixmap('plot1.png')
        self._3_lbl_plot.setPixmap(pixmap)

    def _6_voting(self):
        test = 10 - int(self._6_checkbox_num_elements.currentText())
        methods = ["histogram", "gradient", "dft", "dct", "scale"]
        data = get_data()
        data_train, data_test = get_split_data(data, test)
        result = []
        for i in range(len(methods)):
            method = eval('get_'+methods[i])
            if (self._6_textboxes_param[i].text() == '') or (self._6_textboxes_param[i].text() == 'Параметр'):
                best_p, a = get_best_params(data_train, data_test, method)
                r = classifier(data_train, data_test, method, best_p)
                self._6_textboxes_param[i].setText(str(round(best_p, 3)))
                self._6_textboxes_accuracy[i].setText(str(round(a, 3)))
            else:
                if method == get_scale:
                    best_p = float(self._6_textboxes_param[i].text())
                else:
                    best_p = int(self._6_textboxes_param[i].text())
                r = classifier(data_train, data_test, method, best_p)
                a = accuracy_score(r, data_test[1])
                self._6_textboxes_accuracy[i].setText(str(round(a, 3)))
            result.append(r)

        result = np.array(result)
        result = result.transpose()
        result = result.tolist()
        result = list(map(lambda x: max(x, key=x.count), result))
        ac = accuracy_score(result, data_test[1])
        self._6_textboxes_accuracy[-1].setText(str(round(ac, 3)))

        fig = plt.figure(figsize=(12, 12))
        ax_im = []
        ax_f = []
        ax_im_f = []
        for i in range(6):
            ax_im.append(fig.add_subplot(6, 6, i+1))
            # ax_f.append(fig.add_subplot(6, 6, i+7))
            # ax_im_f.append(fig.add_subplot(6, 6, i+14))
        for i in range(5):
            ax_f.append(fig.add_subplot(6, 6, i+8))
            ax_im_f.append(fig.add_subplot(6, 6, i+14))

        ax = fig.add_subplot(2, 1, 2)
        ax.set_xlim(0, len(data_test[0]))
        ax.set_ylim(0, 1.02)
        plt.ion()
        res = {"histogram":[], "gradient":[], "dft":[], "dct":[], "scale":[], "voting":[]}

        for k in range(len(data_test[0])):
            ax_im[0].clear()
            ax_im[0].set_title('Тестовое изображение:')
            ax_im[0].axis('off')
            # ax_f[0].clear()
            for i in range(1, 6):
                ax_im[i].clear()
                ax_im[i].set_title(methods[i-1] + ':')
                ax_im[i].axis('off')
            for i in range(5):
                ax_f[i].clear()
                ax_im_f[i].clear()
            ax_f[4].axis('off')
            ax_im_f[4].axis('off')
            ax.clear()
            ax.set_xlabel('test_num')
            ax.set_ylabel('accuracy')
            ax.set_xlim(0, len(data_test[0]))
            ax.set_ylim(0, 1.02)

            image = cv2.resize(data_test[0][k], (100, 100), interpolation=cv2.INTER_AREA)
            cv2.imwrite('test.jpg', 255 * image)
            image = plt.imread('test.jpg')
            ax_im_image = data_test[0][k]
            ax_im[0].imshow(image, cmap='gray')

            for i in range(5):
                method = eval('get_'+methods[i])
                if method == get_scale:
                    p = float(self._6_textboxes_param[i].text())
                else:
                    p = int(self._6_textboxes_param[i].text())

                ind = closest(data_train, data_test[0][k], method, p)
                image = cv2.resize(data_train[0][ind], (100, 100), interpolation=cv2.INTER_AREA)
                cv2.imwrite('test.jpg', 255 * image)
                image = plt.imread('test.jpg')
                ax_im[i+1].imshow(image, cmap='gray')
                self.get_plot(method, data_train[0][ind], p, ax_f[i])
                self.get_plot(method, ax_im_image, p, ax_im_f[i])

                if data_test[1][k] == data_train[1][ind]:
                    res[methods[i]].append(1)
                else:
                    res[methods[i]].append(0)

            if data_test[1][k] == result[k]:
                res['voting'].append(1)
            else:
                res['voting'].append(0)
            data = []
            for m in res.keys():
                data.append([mean(res[m][:i+1]) for i in range(len(res[m]))])
            for y in data:
                ax.plot([i for i in range(len(res['voting']))], y)
            ax.legend(["histogram", "gradient", "dft", "dct", "scale", "voting"])
            plt.pause(self.Settings.plotPause)
            fig.show()
            fig.canvas.draw()

    def get_plot(self, method, im, best_p, ax):
        if method == get_histogram:
            hist, bins = get_histogram(im, best_p)
            hist = np.insert(hist, 0, 0.0)
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            ax.plot(bins, hist)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            # plt.savefig('plot.png')
            # plt.close(fig)
        elif method == get_dct or method == get_dft:
            ex = method(im, best_p)
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            ax.pcolormesh(range(ex.shape[0]), range(ex.shape[0]), np.flip(ex, 0))
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            # plt.savefig('plot.png')
            # plt.close(fig)
        elif method == get_scale:
            image = cv2.resize(im, (100, 100), interpolation=cv2.INTER_AREA)
            image = method(image, best_p)
            cv2.imwrite('plot.png', 255 * image)
            image = plt.imread('plot.png')
            ax.imshow(image, cmap='gray')
        # gradient
        else:
            ex = method(im, best_p)
            # fig = plt.figure(figsize=(1.1, 1.1))
            # ax = fig.add_subplot(111)
            ax.plot(range(0, len(ex)), ex)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            # plt.savefig('plot.png')
            # plt.close(fig)

    def get_plot_1(self, method, im, best_p):
        if method == get_histogram:
            hist, bins = get_histogram(im, best_p)
            hist = np.insert(hist, 0, 0.0)
            fig = plt.figure(figsize=(1.1, 1.1))
            ax = fig.add_subplot(111)
            plt.plot(bins, hist)
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            plt.savefig('plot.png')
            plt.close(fig)
        elif method == get_dct or method == get_dft:
            ex = method(im, best_p)
            fig = plt.figure(figsize=(1.1, 1.1))
            ax = fig.add_subplot(111)
            plt.pcolormesh(range(ex.shape[0]), range(ex.shape[0]), np.flip(ex, 0))
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            plt.savefig('plot.png')
            plt.close(fig)
        elif method == get_scale:
            image = cv2.resize(im, (100, 100), interpolation=cv2.INTER_AREA)
            image = method(image, best_p)
            cv2.imwrite('plot.png', 255 * image)
        # gradient
        else:
            ex = method(im, best_p)
            fig = plt.figure(figsize=(1.1, 1.1))
            ax = fig.add_subplot(111)
            plt.plot(range(0, len(ex)), ex)
            # plt.xticks(color='w')
            # plt.yticks(color='w')
            plt.savefig('plot.png')
            plt.close(fig)

if __name__ == '__main__':
    app = QApplication([])
    settings = facesWindowSettings(500, 120, 1000, 700, 200, 1.2)
    widget = facesWindow(settings)
    widget.show()
    sys.exit(app.exec_())
