# Set a variable for the working directory

import os
from . import config
import aqt


# custom path for dev work
if config.Dev:
    addonDir = os.path.join(aqt.mw.pm.addonFolder(), 'bulk_importer_dev')
else:
    if (os.path.exists(os.path.join(aqt.mw.pm.addonFolder(), config.addon_num))):
        addonDir = os.path.join(aqt.mw.pm.addonFolder(), config.addon_num)
    else:
        addonDir = os.path.join(aqt.mw.pm.addonFolder(), 'bulk_importer')
