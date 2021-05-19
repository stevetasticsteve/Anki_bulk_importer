import aqt
import os
import logging

from . import bulk_importer
from . import config
from . import path

os.chdir(path.addonDir)

logging.basicConfig(filename="logfile.log", level=logging.ERROR)


def CLAImporter():
    try:
        logging.debug("\n\nAddon called from menu")
        bulk_importer.run()
    except Exception as e:
        logging.critical(str(e))
        raise


# create a new menu item, "CLA importer"
if config.Dev:
    action = aqt.QAction("Bulk importer (development)", aqt.mw)
else:
    action = aqt.QAction("Bulk importer", aqt.mw)
action.triggered.connect(CLAImporter)
aqt.mw.form.menuTools.addAction(action)
