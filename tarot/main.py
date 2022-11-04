import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import random


class MeaningsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/meanings.ui', self)
        self.setWindowTitle('Значения карт')
        self.setWindowIcon(QIcon('pictures/icons/tarot.ico'))

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        self.window_notes = NotesWindow()
        self.btn_notes.clicked.connect(lambda: self.show_window(self.window_notes))

        self.senior.currentIndexChanged.connect(lambda: self.set_data(self.senior.currentIndex() - 1, 'senior_arcana'))
        self.wands.currentIndexChanged.connect(lambda: self.set_data(self.wands.currentIndex(), 'wands'))
        self.cups.currentIndexChanged.connect(lambda: self.set_data(self.cups.currentIndex(), 'cups'))
        self.swords.currentIndexChanged.connect(lambda: self.set_data(self.swords.currentIndex(), 'swords'))
        self.pentacles.currentIndexChanged.connect(lambda: self.set_data(self.pentacles.currentIndex(), 'pentacles'))

    def set_data(self, key, table):
        if key != -1 and table == 'senior_arcana' or \
           key != 0 and table != 'senior_arcana':
            name = self.cur.execute(f"""SELECT name FROM {table}
                WHERE key = {key}""").fetchone()
            description = self.cur.execute(f"""SELECT description FROM {table}
                WHERE key = {key}""").fetchone()
            direct = self.cur.execute(f"""SELECT direct FROM {table}
                WHERE key = {key}""").fetchone()
            inverted = self.cur.execute(f"""SELECT inverted FROM {table}
                WHERE key = {key}""").fetchone()

            self.image.setPixmap(QPixmap(f'pictures/{table}/{key}.png'))

            self.name.setText(*name)
            self.description.setPlainText(*description)
            self.direct.setHtml(*direct)
            self.inverted.setHtml(*inverted)

            self.window_notes.set_notes(key, table)

            if table != 'senior_arcana':
                self.senior.setCurrentIndex(0)
            if table != 'wands':
                self.wands.setCurrentIndex(0)
            if table != 'cups':
                self.cups.setCurrentIndex(0)
            if table != 'swords':
                self.swords.setCurrentIndex(0)
            if table != 'pentacles':
                self.pentacles.setCurrentIndex(0)

    def show_window(self, window):
        window.show()


class NotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/notes.ui', self)
        self.setWindowTitle('Заметки')
        self.setWindowIcon(QIcon('pictures/icons/notes.ico'))

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        self.btn_save.clicked.connect(self.save)

        self.key = None
        self.table = ''

    def save(self):
        if self.table:
            text = self.text.toPlainText()

            self.cur.execute('UPDATE ' + self.table + ' SET notes = "' + text + '" WHERE key = ' + str(self.key))
            self.db.commit()

    def set_notes(self, key, table):
        self.key = key
        self.table = table

        notes = self.cur.execute(f"""SELECT notes FROM {table}
            WHERE key = {key}""").fetchone()

        self.text.setPlainText(str(*notes))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '', 'Закрыть окно заметок?', QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class DayCardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/day_card.ui', self)
        self.setWindowTitle('Карта дня')
        self.setWindowIcon(QIcon('pictures/icons/tarot.ico'))

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        self.random_card()

        self.btn_new.clicked.connect(self.random_card)

    def random_card(self):
        table = random.choice(['senior_arcana', 'wands', 'cups', 'swords', 'pentacles'])
        if table == 'senior_arcana':
            key = random.randint(0, 21)
        else:
            key = random.randint(1, 14)

        self.image.setPixmap(QPixmap(f'pictures/{table}/{key}.png'))

        name = self.cur.execute(f"""SELECT name FROM {table}
            WHERE key = {key}""").fetchone()
        meaning = self.cur.execute(f"""SELECT day_card FROM {table}
            WHERE key = {key}""").fetchone()

        self.name.setText(*name)
        self.meaning.setPlainText(*meaning)

        self.btn_description.clicked.connect(lambda: self.show_info(table, key))

    def show_info(self, table, key):
        ex.window_meanings.set_data(key, table)
        ex.window_meanings.show()


class LayoutsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/layouts.ui', self)
        self.setWindowTitle('Расклады')
        self.setWindowIcon(QIcon('pictures/icons/tarot.ico'))

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        images = [self.image1, self.image2, self.image3, self.image4, self.image5, self.image6,
                  self.image7, self.image8, self.image9]
        texts = [self.text1, self.text2, self.text3, self.text4, self.text5, self.text6,
                 self.text7, self.text8, self.text9]

        for i in range(1, 10):
            images[i - 1].setPixmap(QPixmap(f'pictures/layouts/{i}.png'))

            data = self.cur.execute(f"""SELECT data FROM layouts
                WHERE key = {i}""").fetchone()
            texts[i - 1].setPlainText(*data)


class InfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/info.ui', self)
        self.setWindowTitle('О Таро')
        self.setWindowIcon(QIcon('pictures/icons/tarot.ico'))

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        texts = [self.data1, self.data2, self.data3, self.data4,
                 self.data5, self.data6, self.data7]

        for i in range(1, 8):
            data = self.cur.execute(f"""SELECT data FROM info
                WHERE key = {i}""").fetchone()
            texts[i - 1].setHtml(*data)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.setWindowTitle('Справочник по картам Таро')
        self.setWindowIcon(QIcon('pictures/icons/tarot.ico'))

        self.window_meanings = MeaningsWindow()
        self.window_day_card = DayCardWindow()
        self.window_layouts = LayoutsWindow()
        self.window_info = InfoWindow()

        self.image.setPixmap(QPixmap(f'pictures/main_window.png'))
        self.btn_meaning.clicked.connect(lambda: self.show_window(self.window_meanings))
        self.btn_day_card.clicked.connect(lambda: self.show_window(self.window_day_card))
        self.btn_layouts.clicked.connect(lambda: self.show_window(self.window_layouts))
        self.btn_info.clicked.connect(lambda: self.show_window(self.window_info))

    def show_window(self, window):
        window.show()

    def closeEvent(self, event):
        app.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
