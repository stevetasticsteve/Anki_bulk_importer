import aqt
import anki

import logging
import os
import re
import shutil

def create_card():
    card = aqt.mw.col.models.new('CLA')
    card['flds'] = [
        {'name': 'Prompt', 'ord': 0, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []},
        {'name': 'Picture', 'ord': 1, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []},
        {'name': 'Audio', 'ord': 2, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []},
        {'name': 'Response', 'ord': 3, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []},
        {'name': 'Hint', 'ord': 4, 'sticky': False, 'rtl': False, 'font': 'Arial', 'size': 20, 'media': []}]
    card['tmpls'] = [{'name': 'CLA Card', 'ord': 0, 'qfmt': '{{Prompt}}\n<br>\n{{Picture}}\n\n',
                          'afmt': '{{Response}}{{Audio}}\n<br>\n{{Picture}}', 'did': None, 'bqfmt': '',
                          'bafmt': ''}]
    card['req'] = [0, 'any', 3]
    card['sortf'] = 3
    card['css'] = '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n ' \
                  'background-color: white;\n}\n\nimg{\n width: auto;\n height: auto;\n max-width: 600px;\n ' \
                  'max-height: 600px;\n}\n'
    card['type'] = 0
    return card

def run(self):
    length1 = self.pictureTableData.rowCount()
    logging.debug('Import proceeding')
    self.picImport = []
    self.audioImport = []
    self.promptImport = []
    self.responseImport = []
    mediaDir = re.sub("(?i)\.(anki2)$", ".media", aqt.mw.col.path)
    logging.debug('Media folder (mediaDir): ' + (str(mediaDir)))
    # Picture import
    for row in range(self.pictureTableData.rowCount()):
        if self.pictureTableData.item(row) and self.pictureTableData.item(row).text() != "":
            picBase = self.pictureTableData.item(row).text()
            logging.debug('Read from picture row: ' + str(picBase))
            picPath = os.path.join(self.picDir, picBase)
            picAnki = '<img src="' + picBase + '">'
            self.picImport.append(picAnki)
            logging.debug(str(picAnki) + ' appended as picture')
            if os.path.exists(os.path.join(mediaDir, picBase)):
                logging.warning('Picture already exists, not importing')
            else:
                pixmap = aqt.qt.QPixmap(picPath)
                pixmap_resized = pixmap.scaled(720, 405, aqt.qt.Qt.KeepAspectRatio)
                pixmap_resized.save(os.path.join(mediaDir, picBase))
                logging.debug(
                    'Picture save successfile = ' + str(pixmap_resized.save(os.path.join(mediaDir, picBase))))
        else:
            self.picImport.append('')
            logging.debug('Blank picture row, \'\' appended as picture')

        # Audio import
        if self.audioTableData.item(row) and self.audioTableData.item(row).text() != '':
            audioBase = self.audioTableData.item(row).text()
            logging.debug('Read from audio row: ' + str(audioBase))
            audioPath = os.path.join(self.audioDir, audioBase)
            audioAnki = "[sound:" + audioBase + "]"
            self.audioImport.append(audioAnki)
            logging.debug(str(audioAnki) + ' appended as audio')
            try:
                if self.keepOriginal == True:  # Loop to enable destructive copy/paste. Unused, value set to True under __init))
                    shutil.copyfile(audioPath, '_' + audioBase)
                    copyAudio = os.path.join(self.addonDir, '_' + audioBase)
                    shutil.move(audioPath, mediaDir)
                    os.rename(copyAudio, audioBase)
                    shutil.move(os.path.join(self.addonDir, audioBase), self.audioDir)
                elif self.keepOriginal == False:
                    shutil.move(audioSrc, mediaDir)
            except shutil.Error:
                logging.warning('File already exists: ' + str(audioBase))
                os.remove(copyAudio)
                None
        else:
            self.audioImport.append('')
            logging.debug('Blank audio row, \'\' appended as audio')

        if self.promptTableData.item(row):
            promptcontents = self.promptTableData.item(row)
            self.promptImport.append(promptcontents.text())
            logging.debug(str(promptcontents.text()) + ' appended as prompt')
        else:
            self.promptImport.append('')
            logging.debug('Blank prompt row, \'\' appended as prompt')
        if self.responseTableData.item(row):
            responsecontents = self.responseTableData.item(row)
            self.responseImport.append(responsecontents.text())
            logging.debug(str(responsecontents.text()) + ' appended as response')
        else:
            self.responseImport.append('')
            logging.debug('Blank response row, \'\' appended as response')

    if '' in self.promptImport:
        aqt.qt.QMessageBox.warning(self, 'Warning', 'Every row requires a prompt, enter a prompt')
        return None
    elif '' in self.picImport or '' in self.audioImport or '' in self.responseImport:
        logging.info('Blank rows detected, warning issued')
        check = aqt.qt.QMessageBox.question(self, 'Blank fields', 'Some fields are blank, do you want to continue?')
        if check == aqt.qt.QMessageBox.No:
            logging.info('User cancelled import')
            return None
        elif check == aqt.qt.QMessageBox.Yes:
            logging.info('User proceeding with blanks')

    filePath = os.path.join(self.addonDir, 'ifile.txt')
    ifile = open(filePath, 'w')
    logging.debug('Temporary file created for import: ' + str(filePath))
    line = []
    logging.debug('Preparing to append to database pictures: ' + str(self.picImport))
    logging.debug('Preparing to append database prompts: ' + str(self.promptImport))
    logging.debug('Preparing to append database audio: ' + str(self.audioImport))
    logging.debug('Preparing to append database responses: ' + str(self.responseImport))

    countFile = os.path.join(self.addonDir, 'Import_counter.txt')
    # Tag creation and storage
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

    # Temporary file creation
    for i in range(len(self.picImport)):
        logging.debug('Index = ' + str(i))
        line.append(
            self.promptImport[i] + ',' + self.picImport[i] + ',' + self.audioImport[i] + ',' + self.responseImport[
                i] + ',' + ',' + Tag + '\n')
    ifile.writelines(line)
    ifile.close()
    logging.debug('Temporary file complete')

    # Load Anki importer
    importer = anki.importing.Importers[0][1]
    importer = importer(aqt.mw.col, filePath)

    # Set model to CLA, create if absent
    if aqt.mw.col.models.byName('CLA') == None:
        logging.info('No CLA card, creating one')
        newModel = create_card()

        aqt.mw.col.models.add(newModel)
        importer.model = newModel
    claModel = aqt.mw.col.models.byName('CLA')
    logging.debug('Model = ' + str(claModel))
    importer.model = claModel

    # Importer options and target deck
    importer.importMode = 2  # Needs to be 2 to overwrite (prompts are often the same)
    importer.allowHTML = True
    importer.open()
    DeckID = self.Deck.selectedId()
    if DeckID != importer.model['did']:
        importer.model['did'] = DeckID
        aqt.mw.col.models.save(importer.model)

    # Importer execution and followup
    importer.run()
    summaryMsg = str(length1) + ' card(s) created in ' + self.Deck._deckName + ' deck.'
    summary = aqt.qt.QMessageBox.about(self, 'Results', summaryMsg)
    os.remove(filePath)
    logging.debug('Temporary file deleted')
    self.close()