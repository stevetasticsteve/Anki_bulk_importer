import sys
import os
import logging

import aqt
import anki

from . import config
from . import run_import

# todo if you load 6 pictures, then load 1 picture you don't just get 1 picture, you get several. Same with audio

version = '1.1'


class Window(aqt.qt.QDialog):
    def __init__(self, mw):
        aqt.qt.QDialog.__init__(self, aqt.mw)
        if config.Dev:
            self.addonDir = (os.path.join(aqt.mw.pm.addonFolder(), 'bulk_importer_dev'))
        else:
            self.addonDir = (os.path.join(aqt.mw.pm.addonFolder(), 'bulk_importer'))
        os.chdir(self.addonDir)
        logging.debug('Bulk importer Window opened')
        logging.debug('CwDir: ' + str(os.getcwd()))
        logging.debug('Addon Directory (self.addonDir): ' + str(self.addonDir))
        self.mw = mw
        if config.Dev:
            self.setWindowTitle('Bulk Importer Development version')
        else:
            self.setWindowTitle('Bulk Importer v.%s' % version)
        self.setWindowIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'Py_Logo.png')))

        # Layout the main window in a grid (row, column). The grid is 5 x 11
        self.grid = aqt.qt.QGridLayout()
        self.grid.setSpacing(10)

        # grid locations
        self.promptColumn = 0
        self.pictureColumn = 3
        self.responseColumn = 6
        self.audioColumn = 9

        self.topBtnRow = 0
        self.tableRow = 1
        self.bottomBtnRow = 5

        # Load pictures button
        picbtn = aqt.qt.QPushButton('Load pics', self)
        picbtn.clicked.connect(self.open_pic_files)
        # Pick Audio button
        audiobtn = aqt.qt.QPushButton('Load Audio', self)
        audiobtn.clicked.connect(self.open_audio_files)
        self.playing = 0
        # Play button
        self.playbtn = aqt.qt.QPushButton('', self)
        self.playbtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'play.png')))
        self.playbtn.clicked.connect(self.play)
        # Copy button
        copybtn = aqt.qt.QPushButton('Copy 1st row to all', self)
        copybtn.clicked.connect(self.copy_prompt)
        # import button
        importbtn = aqt.qt.QPushButton('Import', self)
        importbtn.clicked.connect(self.Anki_import)
        # Deck Chooser
        self.deckbtn = aqt.qt.QPushButton('Deck', self)
        self.Deck = aqt.deckchooser.DeckChooser(aqt.mw, self.deckbtn, label=False)
        self.deckLabel = aqt.qt.QLabel(self)
        self.deckLabel.setText('Deck:')
        self.deckLabel.setAlignment(aqt.qt.Qt.AlignVCenter | aqt.qt.Qt.AlignRight)
        # Audio Copy options
        self.keepOriginal = True
        # Picture preview, using Placeholder image for startup
        self.pic = aqt.qt.QLabel(self)
        self.pic.setScaledContents(True)
        self.pic.setAlignment(aqt.qt.Qt.AlignHCenter)
        self.picSrc = os.path.join(self.addonDir, 'icons', 'placeholder.jpeg')
        self.pixmap = aqt.qt.QPixmap(self.picSrc).scaled(150, 150, aqt.qt.Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        # Draw Tables
        self.pictureTableData = self.create_model(['Picture'], [])
        self.audioTableData = self.create_model(['Audio'], [])
        self.promptTableData = self.create_model(['Prompt'], [])
        self.responseTableData = self.create_model(['Response'], [])
        self.pictureTable = self.draw_table(self.tableRow, self.pictureColumn, 2, 3, self.pictureTableData)
        self.pictureTable.clicked.connect(self.update_pic)
        self.audioTable = self.draw_table(self.tableRow, self.audioColumn, 4, 3, self.audioTableData)
        self.promptTable = self.draw_table(self.tableRow, self.promptColumn, 4, 3, self.promptTableData)
        self.responseTable = self.draw_table(self.tableRow, self.responseColumn, 4, 3, self.responseTableData)

        # add widgets to grid, starting Top left. Left to right, row by row
        self.grid.addWidget(copybtn, self.topBtnRow, self.promptColumn)
        self.grid.addWidget(picbtn, self.topBtnRow, self.pictureColumn)
        self.grid.addWidget(audiobtn, self.topBtnRow, self.audioColumn)
        self.grid.addWidget(self.playbtn, self.topBtnRow, self.audioColumn + 1)
        # (tables were added with the draw_table method)
        self.grid.addWidget(self.pic, 4, 3, 2, 3)
        self.grid.addWidget(self.deckLabel, self.bottomBtnRow, self.audioColumn)
        self.grid.addWidget(self.deckbtn, self.bottomBtnRow, self.audioColumn + 1)
        self.grid.addWidget(importbtn, self.bottomBtnRow, self.audioColumn + 2)
        self.setLayout(self.grid)

        # Set window geometry
        self.position = (200, 200)  # xy coordinates of top left corner of window
        self.setGeometry(self.position[0], self.position[1], config.window_size[0] + self.position[0],
                         config.window_size[1] + self.position[1])
        self.show()

    def create_model(self, title, data):
        # Creates a model to be used by tableview widget.
        model = (aqt.qt.QStandardItemModel(self))
        model.setHorizontalHeaderLabels(title)
        for i in data:
            item = aqt.qt.QStandardItem(i)
            item.setDropEnabled(False)
            model.appendRow(item)
        return model

    def draw_table(self, row0, column0, row1, column1, model):
        # Draws a tableview, requires a model to be passed in.
        self.table = aqt.qt.QTableView(self)
        self.table.setModel(model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(aqt.qt.QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        self.table.setDragDropMode(self.table.InternalMove)
        self.table.setDragDropOverwriteMode(False)
        self.table.setDropIndicatorShown(True)
        self.grid.addWidget(self.table, row0, column0, row1, column1)
        return self.table

    @staticmethod
    def close_application():
        sys.exit()

    def open_pic_files(self):
        # Opens files and displays in table1
        options = aqt.qt.QFileDialog.Options()
        caption = "Load pictures"
        startingFolder = os.path.expanduser('~\pictures')
        file_filter = "Images (*.jpeg *.jpg *JPG *JPEG)"
        file, _ = aqt.qt.QFileDialog.getOpenFileNames(self, caption, startingFolder, file_filter, options=options)
        if len(file) != 0:
            self.picDir = os.path.dirname(file[0])
            logging.debug('User selected picture directory (picDir): ' + str(self.picDir))
            for i in range(self.pictureTableData.rowCount()):
                self.pictureTableData.removeRow(i)
            for i, j in enumerate(file):
                base = os.path.basename(j)
                item = aqt.qt.QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.pictureTableData.setItem(i, item)
        self.equalize_rows()

    def open_audio_files(self):
        # Opens files and displays in table2
        options = aqt.qt.QFileDialog.Options()
        caption = "Load Audio"
        startingFolder = os.path.expanduser('~\music')
        file_filter = "Audio (*.mp3 *.MP3)"
        file, _ = aqt.qt.QFileDialog.getOpenFileNames(self, caption, startingFolder, file_filter, options=options)
        if len(file) != 0:
            self.audioDir = os.path.dirname(file[0])
            for i in range(self.audioTableData.rowCount()):
                self.audioTableData.removeRow(i)
            for i, j in enumerate(file):
                base = os.path.basename(j)
                item = aqt.qt.QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.audioTableData.setItem(i, item)
        self.equalize_rows()

    def play(self):
        # Play button functionality - play and pause selected audio

        index = self.audioTable.selectedIndexes()
        if self.playing == 0:
            if self.audioTableData.rowCount() > 0 and index != []:
                try:
                    filename = index[0].data()
                    audio = os.path.join(self.audioDir, filename)
                    anki.sound.play(audio)
                    self.playing = 1
                    self.playbtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'pause.png')))
                except (AttributeError, FileNotFoundError):
                    return None

        elif self.playing == 1:
            anki.sound.clearAudioQueue()
            self.playing = 0
            self.playbtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'play.png')))

    def update_pic(self):
        # Updates thumbnail image when image selected
        index = self.pictureTable.selectedIndexes()
        filename = index[0].data()
        logging.debug('User selected image: ' + str(filename))
        try:
            if filename == '':
                logging.debug('loop entered')
                self.picSrc = os.path.join(self.addonDir, 'icons', 'no-image.png')
                logging.debug('No image Thumbnail = ' + str(self.picSrc))
                self.pixmap = aqt.qt.QPixmap(self.picSrc).scaled(50, 50)
                self.pic.setPixmap(self.pixmap)
            else:
                newpic = os.path.join(self.picDir, filename)
                logging.debug('Thumbnail = ' + str(newpic))
                self.picSrc = newpic
                self.pixmap = aqt.qt.QPixmap(self.picSrc).scaled(200, 200, aqt.qt.Qt.KeepAspectRatio)
                self.pic.setPixmap(self.pixmap)
        except (TypeError, AttributeError):
            self.picSrc = os.path.join(self.addonDir, 'icons', 'no-image.png')
            logging.debug('No image Thumbnail = ' + str(self.picSrc))
            self.pixmap = aqt.qt.QPixmap(self.picSrc).scaled(50, 50)
            self.pic.setPixmap(self.pixmap)

    def equalize_rows(self):
        # Adds or removes rows to prompt and response to match first tables

        # find total number of rows, and also find the final non-blank row for audio and pictures
        total_picture_rows = self.pictureTableData.rowCount()  # total number of rows including blanks on end
        picture_rows = total_picture_rows  # number of rows excluding blanks on end
        for i in range(total_picture_rows - 1, 0, -1):  # picture_rows -1 to account for 0 indexing
            if self.pictureTableData.item(i).text() == '':
                picture_rows -= 1  # will loop to find the final row containing non blank data
            else:
                break
        total_audio_rows = self.audioTableData.rowCount()  # total number of rows including blanks
        audio_rows = total_audio_rows  # number of rows excluding blanks on end
        for i in range(total_audio_rows - 1, 0, -1):  # audio_rows -1 accounts for 0 indexing
            if self.audioTableData.item(i).text() == '':
                audio_rows -= 1
            else:
                break
        prompt_rows = self.promptTableData.rowCount()

        # find the longest table
        if picture_rows > audio_rows:
            long = picture_rows
        elif picture_rows < audio_rows:
            long = audio_rows
        else:  # length is equal, so use either value
            long = picture_rows

        # add blank rows to prompt and response to match longest table
        if prompt_rows < long:  # add rows to prompt and response until rows equal
            for i in range(prompt_rows, long):
                item = aqt.qt.QStandardItem('')
                item.setDropEnabled(False)
                self.promptTableData.appendRow(item)
                self.responseTableData.appendRow(item)
        elif prompt_rows > long:  # remove rows from prompt and response until rows equal
            for i in range(prompt_rows, long - 1, -1):
                self.promptTableData.removeRow(i)
                self.responseTableData.removeRow(i)

        # add or remove blank rows to audio to match longest table
        if total_audio_rows < long:
            for i in range(total_audio_rows, long):
                item = aqt.qt.QStandardItem('')
                item.setDropEnabled(False)
                self.audioTableData.appendRow(item)
        elif total_audio_rows > long:
            for i in range(total_audio_rows, long - 1, -1):
                self.audioTableData.removeRow(i)

        # add or remove blank rows to picture to match longest table
        if total_picture_rows < long:
            for i in range(total_picture_rows, long):
                item = aqt.qt.QStandardItem('')
                item.setDropEnabled(False)
                self.pictureTableData.appendRow(item)
        elif total_picture_rows > long:
            for i in range(total_picture_rows, long - 1, -1):
                self.pictureTableData.removeRow(i)

    def copy_prompt(self):
        # Copy and paste first prompt to all rows
        if self.promptTableData.rowCount() > 0:
            promptObj = self.promptTableData.item(0)
            promptObj.setDropEnabled(False)
            prompt = promptObj.text()
            for i in range(self.promptTableData.rowCount()):
                self.promptTableData.setItem(i, aqt.qt.QStandardItem(prompt))

    # Import into Anki
    def Anki_import(self):
        run_import.run(self)

    def closeEvent(self):
        aqt.mw.reset()
        M = anki.media.MediaManager(aqt.mw.col, None)
        M.check()


def run():
    Window(aqt.mw)
