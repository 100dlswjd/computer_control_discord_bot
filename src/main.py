import sys

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QCloseEvent
from ui.main_form import Ui_MainWindow
import My_class.bot_class as bot_class

from threading import Thread, Event

class Mainwindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self.start_flag = False
        
        self.program_event = Event()
        self.program_event.clear()

        self.bot_token = ""
        self.pushButton_start.clicked.connect(self.btn_start_handler)

        
        self.bot_exit_event = Event()
        self.bot_exit_event.set()
        

    def thread_proc(self):
        while not self.program_event.is_set():
            self.program_event.wait(0.1)
            while not self.bot_exit_event.is_set():
                self.discord_bot.start()
                self.bot_exit_event.wait(0.1)
        
    def btn_start_handler(self):
        self.start_flag = not self.start_flag
        self.bot_token = self.lineEdit_bot_token.text()
        if self.start_flag:
            self.program_start()
            
        else:
            self.program_stop()

    def program_start(self):
        self.bot_exit_event.clear()
        self.pushButton_start.setText("프로그램 종료")
        self.lineEdit_bot_token.setEnabled(False)
        self.discord_bot = bot_class.discord_bot(self.bot_token)
        self.bot_thread = Thread(target = self.thread_proc)
        self.bot_thread.start()

    def program_stop(self):
        self.bot_exit_event.set()
        self.lineEdit_bot_token.setEnabled(True)
        self.discord_bot.stop()
        self.close()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        self.bot_exit_event.set()
        self.program_event.set()
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()