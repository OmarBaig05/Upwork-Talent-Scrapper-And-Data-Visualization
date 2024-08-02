import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
import csv
import threading
from bonousTask import main

class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        loadUi("./.ui/mainPage.ui", self)
        # Command to remove the default Windows Frame Design.
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # Command to make the background of Window transparent.
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # These 2 lines are used to put functions on close and minimize buttons.
        self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
        self.CrossButton.clicked.connect(lambda: self.close())

        self.stop_btn.clicked.connect(self.stop_loading)
        self.start_btn.clicked.connect(self.start_loading)  # Connect the "Start" button to load data
        self.resume_btn.clicked.connect(self.resume_loading)
        self.scraper_btn.clicked.connect(self.open_scraper_page)

    def open_scraper_page(self):
        self.scraper_page = ScraperPage()  # Create an instance of the ScraperPage
        self.scraper_page.show()  # Show the ScraperPage window
        self.close()  # Close the mainPage window

    def load_table(self):
        with open('../ScrapedData/upwork_1data1-500.csv', "r", encoding="utf-8") as fileInput:
            roww = 0
            data = list(csv.reader(fileInput))

            self.tableWidget.setRowCount(len(data))
            for row in data:
                for col, item in enumerate(row):
                    self.tableWidget.setItem(roww, col, QtWidgets.QTableWidgetItem(item))
                roww += 1

    # Helper method to stop loading
    def stop_loading(self):
        self.load_data = False

    # Helper method to start loading
    def start_loading(self):
        self.load_data = True
        # Start the data loading thread
        data_loader_thread = threading.Thread(target=self.load_data_thread)
        data_loader_thread.start()

    # Helper method to resume loading
    def resume_loading(self):
        self.start_loading()

    # This method will be executed in a separate thread to load data
    def load_data_thread(self):
        while self.load_data:
            self.load_table()
class ScraperPage(QMainWindow):
    def __init__(self):
        try:
            super(ScraperPage, self).__init__()
            loadUi("./.ui/scraperPage.ui", self)
            # Command to remove the default Windows Frame Design.
            self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
            # Command to make the background of Window transparent.
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.MinimizeButton.clicked.connect(lambda: self.showMinimized())
            self.CrossButton.clicked.connect(lambda: self.close())

            self.ShowData.clicked.connect(self.LoadExtractedData)
            # Add any additional functionality specific to the scraper page here
            self.mainPage_btn.clicked.connect(self.open_main_page)

            
            self.start_btn.clicked.connect(self.startScraping)

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def open_main_page(self):
        self.main_page = Mainwindow()  # Create an instance of the main page
        self.main_page.show()  # Show the main page window
        self.close()  # Close the scraper page
    def startScraping(self):
        c1 = self.class1.text()
        c2 = self.class2.text()
        c3 = self.class3.text()
        c4 = self.class4.text()
        t1 = self.tag1.text()
        t2 = self.tag2.text()
        t3 = self.tag3.text()
        t4 = self.tag4.text()
        url = self.URLHolder.text()

        main(c1,c2,c3,c4, t1,t2,t3,t4,url)

    def LoadExtractedData(self):
        with open('./ExtractedData/data.csv', "r", encoding="utf-8") as fileInput:
            roww = 0
            data = list(csv.reader(fileInput))

            self.tableWidget.setRowCount(len(data))
            for row in data:
                for col, item in enumerate(row):
                    self.tableWidget.setItem(roww, col, QtWidgets.QTableWidgetItem(item))
                roww += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())
