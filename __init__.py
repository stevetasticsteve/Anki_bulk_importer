from aqt import mw, QAction
import os, logging
from . import CLA_Importer

addonDir = (os.path.join(mw.pm.addonFolder(),'CLA Importer'))
os.chdir(addonDir)
logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

def CLAImporter():
    try:
        logging.debug('\n\nAddon called from menu')
        CLA_Importer.run()
    except Exception as e:
        logging.critical(str(e))
    
# create a new menu item, "CLA importer"
action = QAction("CLA importer", mw)
action.triggered.connect(CLAImporter)
mw.form.menuTools.addAction(action)
