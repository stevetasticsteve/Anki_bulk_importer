# Copyright: Stephen Stanley <stephen_stanley@ntmpng.org>
# -*- coding: utf-8 -*-
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

version = '1.022'

import sys, os, shutil, logging, re

from aqt.qt import *
from anki.sound import play, clearAudioQueue
import aqt
from aqt import mw
from aqt.importing import ImportDialog
import anki.importing as importing
import aqt.deckchooser
from anki.models import ModelManager
from anki.media import MediaManager

class window(QDialog):

    def __init__(self,mw):
        QDialog.__init__(self,mw)
        self.addonDir = (os.path.join(mw.pm.addonFolder(),'CLA Importer'))
        os.chdir(self.addonDir)   
        logging.debug('CLA importer Window opened')
        logging.debug('CwDir: ' + str(os.getcwd()))
        logging.debug('Addon Directory (self.addonDir): ' + str(self.addonDir))
        self.mw = mw
        self.setWindowTitle('CLA Importer v.%s' % version)
        self.setWindowIcon(QIcon(os.path.join(self.addonDir, 'Py_Logo.png')))
        self.home()
        self.setLayout(self.grid)
        self.setGeometry(0, 50, 600, 300)
        self.show()

    def home(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        #Pick pictures button
        picbtn = QPushButton('Load pics',self)
        picbtn.clicked.connect(self.open_pic_files)
        self.grid.addWidget(picbtn, 0,0)
        #Add blank to pictures button
        addpicbtn = QPushButton('Add blank',self)
        addpicbtn.setIcon(QIcon(os.path.join(self.addonDir,'add-icon.png')))
        addpicbtn.clicked.connect(self.add_blank_pic)
        self.grid.addWidget(addpicbtn, 0,1)
        #Add blank to audio
        addaudiobtn = QPushButton('Add blank',self)
        addaudiobtn.setIcon(QIcon(os.path.join(self.addonDir,'add-icon.png')))
        addaudiobtn.clicked.connect(self.add_blank_audio)
        self.grid.addWidget(addaudiobtn, 0,5)
        #Pick Audio button
        audiobtn = QPushButton('Load Audio',self)
        audiobtn.clicked.connect(self.open_audio_files)
        self.playing = 0
        self.grid.addWidget(audiobtn, 0,3)
        #Play button
        self.playbtn = QPushButton('', self)
        self.playbtn.setIcon(QIcon(os.path.join(self.addonDir,'play.png')))
        self.playbtn.clicked.connect(self.play)
        self.grid.addWidget(self.playbtn, 0,4)
        #Copy button
        copybtn = QPushButton('Copy 1st row to all',self)
        copybtn.clicked.connect(self.copy_prompt)
        self.grid.addWidget(copybtn, 0,8)
        #import button
        importbtn = QPushButton('Import', self)
        importbtn.clicked.connect(self.Anki_import)
        self.grid.addWidget(importbtn, 5,11)
        #Deck Chooser
        self.deckbtn = QPushButton('Deck', self)
        self.Deck = aqt.deckchooser.DeckChooser(mw, self.deckbtn, label=False)
        self.grid.addWidget(self.deckbtn, 5,10)
        self.deckLabel = QLabel(self)
        self.deckLabel.setText('Deck:')
        self.deckLabel.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.grid.addWidget(self.deckLabel, 5,9)
        #Audio Copy options
        self.keepOriginal = True
        #Picture preview, using Placeholder image for startup
        self.pic = QLabel(self)
        self.pic.setScaledContents(True)
        self.pic.setAlignment(Qt.AlignHCenter)
        self.picSrc = os.path.join(self.addonDir,'placeholder.jpeg')
        self.pixmap = QPixmap(self.picSrc).scaled(150, 150, Qt.KeepAspectRatio)
        self.pic.setPixmap(self.pixmap)
        self.grid.addWidget(self.pic,4,0,2,3)
        #Draw Tables
        self.Table1Data = self.create_model(['Picture'],[])
        self.Table2Data = self.create_model(['Audio'],[])
        self.Table3Data = self.create_model(['Prompt'],[])
        self.Table4Data = self.create_model(['Response'],[])
        self.Table1 = self.draw_table(1,0,2,3, self.Table1Data)
        self.Table1.clicked.connect(self.update_pic)
        self.Table2 = self.draw_table(1,3,4,3, self.Table2Data)
        self.Table3 = self.draw_table(1,6,4,3, self.Table3Data)
        self.Table4 = self.draw_table(1,9,4,3, self.Table4Data)

    def create_model(self, title, data):
        #Creates a model to be used by tableview widget.
        model = (QStandardItemModel(self))
        model.setHorizontalHeaderLabels(title)
        for i in data:
            item=QStandardItem(i)
            item.setDropEnabled(False)
            model.appendRow(item)
        return(model)
            
    def draw_table(self, row0, column0, row1, column1, model):
        #Draws a tableview, requires a model to be passed in.
        self.table = QTableView(self)
        self.table.setModel(model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setSelectionMode(self.table.SingleSelection)
        self.table.setDragDropMode(self.table.InternalMove)
        self.table.setDragDropOverwriteMode(False)
        self.table.setDropIndicatorShown(True)
        self.grid.addWidget(self.table,row0,column0,row1,column1)
        return self.table
        
    def close_application(self):
        sys.exit()

    def open_pic_files(self, window):
        #Opens files and displays in table1
        options = QFileDialog.Options()
        caption = "Load pictures"
        startingFolder = os.path.expanduser('~\pictures')
        file_filter = "Images (*.jpeg *.jpg *JPG *JPEG)"
        file, _ = QFileDialog.getOpenFileNames(self,caption, startingFolder,file_filter, options=options)  
        if len(file) != 0:
            self.picDir = os.path.dirname(file[0])
            logging.debug('User selected picture directory (picDir): ' + str(self.picDir))
            for i in range(self.Table1Data.rowCount()):
                self.Table1Data.removeRow(i)
            for i,j in enumerate(file):
                base = os.path.basename(j)
                item = QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.Table1Data.setItem(i,item)
        self.Table3and4_length()
                
    def open_audio_files(self, window):
        #Opens files and displays in table2
        options = QFileDialog.Options()
        caption = "Load Audio"
        startingFolder = os.path.expanduser('~\music')
        file_filter = "Audio (*.mp3 *.MP3)"
        file, _ = QFileDialog.getOpenFileNames(self,caption, startingFolder,file_filter, options=options)  
        if len(file) != 0:
            self.audioDir = os.path.dirname(file[0])
            for i in range(self.Table2Data.rowCount()):
                self.Table2Data.removeRow(i)
            for i,j in enumerate(file):
                base = os.path.basename(j)
                item = QStandardItem(base)
                item.setDropEnabled(False)
                item.setEditable(False)
                self.Table2Data.setItem(i,item)
        self.Table3and4_length()

    def play(self):
        #Play button functionality - play and pause selected audio
        
        index = self.Table2.selectedIndexes()
        if self.playing == 0:
            if self.Table2Data.rowCount() > 0 and index != []:
                try:
                    filename = index[0].data()
                    audio = os.path.join(self.audioDir, filename)
                    play(audio)
                    self.playing =1
                    self.playbtn.setIcon(QIcon(os.path.join(self.addonDir,'pause.png')))
                except (AttributeError,FileNotFoundError):
                    return None

        elif self.playing ==1:
            clearAudioQueue()
            self.playing=0
            self.playbtn.setIcon(QIcon(os.path.join(self.addonDir,'play.png')))

    def update_pic(self):
        #Updates thumbnail image when image selected
        index = self.Table1.selectedIndexes()
        filename = index[0].data()
        logging.debug('User selected image: ' + str(filename))
        try:
            if filename == '':
                logging.debug('loop entered')
                self.picSrc = os.path.join(self.addonDir,'no-image.png')
                logging.debug('No image Thumbnail = ' + str(self.picSrc))
                self.pixmap = QPixmap(self.picSrc).scaled(50, 50)
                self.pic.setPixmap(self.pixmap)
            else:
                newpic = os.path.join(self.picDir, filename)
                logging.debug('Thumbnail = ' +str(newpic))
                self.picSrc = newpic
                self.pixmap = QPixmap(self.picSrc).scaled(200, 200, Qt.KeepAspectRatio)
                self.pic.setPixmap(self.pixmap)
        except (TypeError, AttributeError):
            self.picSrc = os.path.join(self.addonDir,'no-image.png')
            logging.debug('No image Thumbnail = ' + str(self.picSrc))
            self.pixmap = QPixmap(self.picSrc).scaled(50, 50)
            self.pic.setPixmap(self.pixmap)

    def Table3and4_length(self):
        #Adds or removes rows to prompt and response to match first tables
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
                item = QStandardItem('')
                item.setDropEnabled(False)
                self.Table3Data.appendRow(item)
                self.Table4Data.appendRow(item)

        elif length3 > long:
            for i in range(length3, long-1, -1):
                self.Table3Data.removeRow(i)
                self.Table4Data.removeRow(i)


    def add_blank_pic(self):
        #Add new row to Table 1
        item = QStandardItem('')
        item.setDropEnabled(False)
        item.setEditable(False)
        self.Table1Data.appendRow(item)

    def add_blank_audio(self):
        #Add new row to Table 2
        item = QStandardItem('')
        item.setDropEnabled(False)
        item.setEditable(False)
        self.Table2Data.appendRow(item)

    def copy_prompt(self):
        #Copy and paste first prompt to all rows
        if self.Table3Data.rowCount() > 0:
            promptObj = self.Table3Data.item(0)
            promptObj.setDropEnabled(False)
            prompt = promptObj.text()
            for i in range(self.Table3Data.rowCount()):
                self.Table3Data.setItem(i,QStandardItem(prompt))

        
    #Import into Anki
    def Anki_import(self):
       
        length1 = self.Table1Data.rowCount()
        length2 = self.Table2Data.rowCount()
        length3 = self.Table3Data.rowCount()
        logging.debug('Import called; Table lengths: {}, {}, {}, {}'.format(str(length1), str(length2), str(length3), str(length3)))
        if length1 == 0:
            QMessageBox.about(self,'Warning',"There needs to be an equal number of items in each field, insert blank rows if required.")
            logging.info('Blank import called, doing nothing')
            return None
        if length1 != length2 or length2 != length3 or length1 != length3:
            QMessageBox.about(self,'Warning',"There needs to be an equal number of items in each field, insert blank rows if required.")
            logging.info('Uneven import called, warning given')
            return None
        logging.debug('Import proceeding')
        self.picImport = []
        self.audioImport = []
        self.promptImport = []
        self.responseImport = []
        mediaDir = re.sub("(?i)\.(anki2)$", ".media", mw.col.path)
        logging.debug('Media folder (mediaDir): ' + (str(mediaDir)))
        #Picture import
        for row in range(self.Table1Data.rowCount()):
            if self.Table1Data.item(row) and self.Table1Data.item(row).text() != "":
                picBase = self.Table1Data.item(row).text()
                logging.debug('Read from picture row: ' + str(picBase))
                picPath = os.path.join(self.picDir, picBase)
                picAnki = '<img src="' + picBase + '">'
                self.picImport.append(picAnki)
                logging.debug(str(picAnki) + ' appended as picture')
                if os.path.exists(os.path.join(mediaDir,picBase)):
                    logging.warning('Picture already exists, not importing')
                else:
                    pixmap = QPixmap(picPath)
                    pixmap_resized = pixmap.scaled(720,405, Qt.KeepAspectRatio)
                    pixmap_resized.save(os.path.join(mediaDir,picBase))
                    logging.debug('Picture save successfile = ' + str(pixmap_resized.save(os.path.join(mediaDir,picBase))))
            else:
                self.picImport.append('')
                logging.debug('Blank picture row, \'\' appended as picture')
                
            #Audio import
            if self.Table2Data.item(row) and self.Table2Data.item(row).text() != '':
                audioBase = self.Table2Data.item(row).text()
                logging.debug('Read from audio row: ' + str(audioBase))
                audioPath = os.path.join(self.audioDir,audioBase)
                audioAnki = "[sound:" + audioBase + "]"
                self.audioImport.append(audioAnki)
                logging.debug(str(audioAnki) + ' appended as audio')
                try:
                    if self.keepOriginal == True:   #Loop to enable destructive copy/paste. Unused, value set to True under __init))
                        shutil.copyfile(audioPath, '_' + audioBase)
                        copyAudio = os.path.join(self.addonDir, '_' + audioBase)
                        shutil.move(audioPath,mediaDir)
                        os.rename(copyAudio, audioBase)
                        shutil.move(os.path.join(self.addonDir,audioBase), self.audioDir)
                    elif self.keepOriginal == False:
                        shutil.move(audioSrc,mediaDir)
                except shutil.Error:
                     logging.warning('File already exists: ' +str(audioBase))
                     os.remove(copyAudio)
                     None
            else:
                self.audioImport.append('')
                logging.debug('Blank audio row, \'\' appended as audio')
                
            if self.Table3Data.item(row):
                promptcontents = self.Table3Data.item(row)
                self.promptImport.append(promptcontents.text())
                logging.debug(str(promptcontents.text()) + ' appended as prompt')
            else:
                self.promptImport.append('')
                logging.debug('Blank prompt row, \'\' appended as prompt')
            if self.Table4Data.item(row):
                responsecontents = self.Table4Data.item(row)
                self.responseImport.append(responsecontents.text())
                logging.debug(str(responsecontents.text()) + ' appended as response')
            else:
                self.responseImport.append('')
                logging.debug('Blank response row, \'\' appended as response')

        if '' in self.promptImport:
            QMessageBox.warning(self,'Warning', 'Every row requires a prompt, enter a prompt')
            return None
        elif '' in self.picImport or '' in self.audioImport or '' in self.responseImport:
            logging.info('Blank rows detected, warning issued')
            check = QMessageBox.question(self, 'Blank fields', 'Some fields are blank, do you want to continue?')
            if check == QMessageBox.No:
                logging.info('User cancelled import')
                return None
            elif check ==QMessageBox.Yes:
                logging.info('User proceeding with blanks')


        filePath = os.path.join(self.addonDir, 'ifile.txt')
        ifile = open(filePath,'w')
        logging.debug('Temporary file created for import: ' + str(filePath))
        line = []
        logging.debug('Preparing to append to database pictures: ' +str(self.picImport))
        logging.debug('Preparing to append database prompts: ' +str(self.promptImport))
        logging.debug('Preparing to append database audio: ' +str(self.audioImport))
        logging.debug('Preparing to append database responses: ' +str(self.responseImport))

        countFile = os.path.join(self.addonDir, 'Import_counter.txt')
        #Tag creation and storage
        if os.path.exists(countFile):
            countOb = open(countFile, 'r')
            count = countOb.read()
            countOb.close()
            countOb = open(countFile, 'w')
            count = int(count)
            count += 1
            iNum = count
            countOb.write(str(count))
            countOb.close()

        elif os.path.exists(countFile) == False:
            count = 1
            iNum = 1
            countOb = open(countFile, 'w')
            countOb.write(str(count))
            countOb.close()

        Tag = 'Import#' + str(iNum)
        logging.debug('Tag = ' + Tag)

        #Temporary file creation
        for i in range(len(self.picImport)):
            logging.debug('Index = ' + str(i))
            line.append(self.promptImport[i] + ',' + self.picImport[i] + ',' + self.audioImport[i] + ',' + self.responseImport[i] + ',' + ',' + Tag +'\n')
        ifile.writelines(line)
        ifile.close()
        logging.debug('Temporary file complete')

        #Load Anki importer
        importer = importing.Importers[0][1]
        importer = importer(mw.col, filePath)

        #Set model to CLA, create if absent
        if mw.col.models.byName('CLA') == None:
            logging.info('No CLA card, creating one')
            newModel = mw.col.models.new('CLA')
            newModel['flds'] = [{'name': 'Prompt', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Picture', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Audio', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Response', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}, {'name': 'Hint', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}]
            newModel['tmpls'] = [{'name': 'CLA Card', 'ord': 0, 'qfmt': '{{Prompt}}\n<br>\n{{Picture}}\n\n', 'afmt': '{{Response}}{{Audio}}\n<br>\n{{Picture}}', 'did': None, 'bqfmt': '', 'bafmt': ''}]
            newModel['req'] = [0, 'any', 3]
            newModel['sortf'] = 3
            newModel['css'] = '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n\nimg{\n width: auto;\n height: auto;\n max-width: 600px;\n max-height: 600px;\n}\n'
            newModel['type'] = 0
            mw.col.models.add(newModel)
            importer.model = newModel      
        claModel = mw.col.models.byName('CLA')
        logging.debug('Model = ' + str(claModel))
        importer.model = claModel

        #Importer options and target deck
        importer.importMode = 2  #Needs to be 2 to overwrite (prompts are often the same)
        importer.allowHTML = True 
        importer.open()
        DeckID = self.Deck.selectedId()   
        if DeckID != importer.model['did']:
            importer.model['did'] = DeckID
            mw.col.models.save(importer.model)

        #Importer execution and followup    
        importer.run()
        summaryMsg = str(length1) + ' card(s) created in ' + self.Deck._deckName + ' deck.'
        summary = QMessageBox.about(self,'Results', summaryMsg)    
        os.remove(filePath)
        logging.debug('Temporary file deleted')
        self.close()

    def closeEvent(self, event):
        mw.reset()
        M = MediaManager(mw.col, None)
        M.check()
        
def run():
    window(mw)


