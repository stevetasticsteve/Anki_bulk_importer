version = '1.1'

import sys
import os
import logging

import aqt
import anki

from . import config
from . import run_import


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
        self.home()
        self.setLayout(self.grid)
        self.position = (200, 200) # xy coordinates of top left corner of window
        self.setGeometry(self.position[0], self.position[1], config.window_size[0] + self.position[0],
                         config.window_size[1] + self.position[1])
        self.show()

    def home(self):
        self.grid = aqt.qt.QGridLayout()
        self.grid.setSpacing(10)
        # Pick pictures button
        picbtn = aqt.qt.QPushButton('Load pics', self)
        picbtn.clicked.connect(self.open_pic_files)
        self.grid.addWidget(picbtn, 0, 0)
        # Add blank to pictures button
        addpicbtn = aqt.qt.QPushButton('Add blank', self)
        addpicbtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'add-icon.png')))
        addpicbtn.clicked.connect(self.add_blank_pic)
        self.grid.addWidget(addpicbtn, 0, 1)
        # Add blank to audio
        addaudiobtn = aqt.qt.QPushButton('Add blank', self)
        addaudiobtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'add-icon.png')))
        addaudiobtn.clicked.connect(self.add_blank_audio)
        self.grid.addWidget(addaudiobtn, 0, 5)
        # Pick Audio button
        audiobtn = aqt.qt.QPushButton('Load Audio', self)
        audiobtn.clicked.connect(self.open_audio_files)
        self.playing = 0
        self.grid.addWidget(audiobtn, 0, 3)
        # Play button
        self.playbtn = aqt.qt.QPushButton('', self)
        self.playbtn.setIcon(aqt.qt.QIcon(os.path.join(self.addonDir, 'icons', 'play.png')))
        self.playbtn.clicked.connect(self.play)
        self.grid.addWidget(self.playbtn, 0, 4)
        # Copy button
        copybtn = aqt.qt.QPushButton('Copy 1st row to all', self)
        copybtn.clicked.connect(self.copy_prompt)
        self.grid.addWidget(copybtn, 0, 8)
        # import button
        importbtn = aqt.qt.QPushButton('Import', self)
        importbtn.clicked.connect(self.Anki_import)
        self.grid.addWidget(importbtn, 5, 11)
        # Deck Chooser
        self.deckbtn = aqt.qt.QPushButton('Deck', self)
        self.Deck = aqt.deckchooser.DeckChooser(aqt.mw, self.deckbtn, label=False)
        self.grid.addWidget(self.deckbtn, 5, 10)
        self.deckLabel = aqt.qt.QLabel(self)
        self.deckLabel.setText('Deck:')
        self.deckLabel.setAlignment(aqt.qt.Qt.AlignVCenter | aqt.qt.Qt.AlignRight)
        self.grid.addWidget(self.deckLabel, 5, 9)
        # Audio Copy options
        self.keepOriginal = True
        # Picture preview, using Placeholder image for startup
        self.pic = aqt.qt.QLabel(self)
        self.pic.setScaledContents(True)
        self.pic.setAlignment(aqt.qt.Qt.AlignHCenter)
        self.picSrc = os.path.join(self.addonDir, 'icons', 'placeholder.jpeg')
        self.pixmap = aqt.qt.QPixmap(self.picSrc).scaled(150, 150, aqt.qt.Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        self.grid.addWidget(self.pic, 4, 0, 2, 3)
        # Draw Tables
        self.Table1Data = self.create_model(['Picture'], [])
        self.Table2Data = self.create_model(['Audio'], [])
        self.Table3Data = self.create_model(['Prompt'], [])
        self.Table4Data = self.create_model(['Response'], [])
        self.Table1 = self.draw_table(1, 0, 2, 3, self.Table1Data)
        self.Table1.clicked.connect(self.update_pic)
        self.Table2 = self.draw_table(1, 3, 4, 3, self.Table2Data)
        self.Table3 = self.draw_table(1, 6, 4, 3, self.Table3Data)
        self.Table4 = self.draw_table(1, 9, 4, 3, self.Table4Data)

    def create_model(self, title, data):
        # Creates a model to be used by tableview widget.
        model = (aqt.qt.QStandardItemModel(self))
        model.setHorizontalHeaderLabels(title)
        for i in data:
            item = aqt.qt.QStandardItem(i)
            item.setDropEnabled(False)
            model.appendRow(item)
        return (model)

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

    def close_application(self):
        sys.exit()

    def open_pic_files(self, window):
        # Opens files and displays in table1
        options = aqt.qt.QFileDialog.Options()
        caption = "Load pictures"
        startingFolder = os.path.expanduser('~\pictures')
        file_filter = "Images (*.jpeg *.jpg *JPG *JPEG)"
        file, _ = aqt.qt.QFileDialog.getOpenFileNames(self, caption, startingFolder, file_filter, options=options)
        if len(file) != 0:
            self.picDir = os.path.dirname(file[0])
            logging.debug('User selected picture directory (picDir): ' + str(self.picDir))
            for i in range(self.Table1Data.rowCount()):
                self.Table1Data.removeRow(i)
            for i, j in enumerate(file):
                base = os.path.basename(j)
                item = aqt.qt.QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.Table1Data.setItem(i, item)
        self.Table3and4_length()

    def open_audio_files(self, window):
        # Opens files and displays in table2
        options = aqt.qt.QFileDialog.Options()
        caption = "Load Audio"
        startingFolder = os.path.expanduser('~\music')
        file_filter = "Audio (*.mp3 *.MP3)"
        file, _ = aqt.qt.QFileDialog.getOpenFileNames(self, caption, startingFolder, file_filter, options=options)
        if len(file) != 0:
            self.audioDir = os.path.dirname(file[0])
            for i in range(self.Table2Data.rowCount()):
                self.Table2Data.removeRow(i)
            for i, j in enumerate(file):
                base = os.path.basename(j)
                item = aqt.qt.QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.Table2Data.setItem(i, item)
        self.Table3and4_length()

    def play(self):
        # Play button functionality - play and pause selected audio

        index = self.Table2.selectedIndexes()
        if self.playing == 0:
            if self.Table2Data.rowCount() > 0 and index != []:
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
        index = self.Table1.selectedIndexes()
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

    def Table3and4_length(self):
        # Adds or removes rows to prompt and response to match first tables
        length1 = self.Table1Data.rowCount()
        length2 = self.Table2Data.rowCount()
        length3 = self.Table3Data.rowCount()

        if length1 > length2:
            long = length1
        elif length1 < length2:
            long = length2
        else:
            long = length1

        if length3 < long:
            for i in range(length3, long):
                item = aqt.qt.QStandardItem('')
                item.setDropEnabled(False)
                self.Table3Data.appendRow(item)
                self.Table4Data.appendRow(item)

        elif length3 > long:
            for i in range(length3, long - 1, -1):
                self.Table3Data.removeRow(i)
                self.Table4Data.removeRow(i)

    def add_blank_pic(self):
        # Add new row to Table 1
        item = aqt.qt.QStandardItem('')
        item.setDropEnabled(False)
        item.setEditable(False)
        self.Table1Data.appendRow(item)

    def add_blank_audio(self):
        # Add new row to Table 2
        item = aqt.qt.QStandardItem('')
        item.setDropEnabled(False)
        item.setEditable(False)
        self.Table2Data.appendRow(item)

    def copy_prompt(self):
        # Copy and paste first prompt to all rows
        if self.Table3Data.rowCount() > 0:
            promptObj = self.Table3Data.item(0)
            promptObj.setDropEnabled(False)
            prompt = promptObj.text()
            for i in range(self.Table3Data.rowCount()):
                self.Table3Data.setItem(i, aqt.qt.QStandardItem(prompt))

    # Import into Anki
    def Anki_import(self):
        run_import.run(self)

    def closeEvent(self, event):
        aqt.mw.reset()
        M = anki.media.MediaManager(aqt.mw.col, None)
        M.check()


def run():
    Window(aqt.mw)
