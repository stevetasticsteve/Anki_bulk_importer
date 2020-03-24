from aqt import mw, QAction
import os, logging
from . import bulk_importer

addonDir = (os.path.join(mw.pm.addonFolder(),'bulk_importer'))
os.chdir(addonDir)
logging.basicConfig(filename='logfile.log',level=logging.DEBUG)

def CLAImporter():
    try:
        logging.debug('\n\nAddon called from menu')
        bulk_importer.run()
    except Exception as e:
        logging.critical(str(e))
    
# create a new menu item, "CLA importer"
action = QAction("Bulk importer", mw)
action.triggered.connect(CLAImporter)
mw.form.menuTools.addAction(action)
