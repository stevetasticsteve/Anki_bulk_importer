from aqt import mw, QAction
import os, logging
from . import bulk_importer
from . import config

if config.Dev:
    addonDir = (os.path.join(mw.pm.addonFolder(),'bulk_importer_dev'))
else:
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
if config.Dev:
    action = QAction("Bulk importer (development)", mw)
else:
    action = QAction("Bulk importer", mw)
action.triggered.connect(CLAImporter)
mw.form.menuTools.addAction(action)
