import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow


class MeaningsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/meanings.ui', self)
        self.setWindowTitle('Значения карт')

        self.db = sqlite3.connect("db/meanings.db")
        self.cur = self.db.cursor()

        self.senior.currentIndexChanged.connect(lambda: self.set_data(self.senior.currentIndex() - 1, 'senior_arcana'))
        self.wands.currentIndexChanged.connect(lambda: self.set_data(self.wands.currentIndex(), 'wands'))

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
            self.direct.setPlainText(*direct)
            self.inverted.setPlainText(*inverted)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.setWindowTitle('Справочник по картам Таро')

        self.window_meanings = MeaningsWindow()

        self.btn_meaning.clicked.connect(lambda: self.show_window(self.window_meanings))

    def show_window(self, window):
        window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
