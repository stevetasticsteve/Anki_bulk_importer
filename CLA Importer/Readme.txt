##############################################
###                                        ###
###        CLA Importer Anki Addon         ###
###                                        ###
##############################################

May 2018
Copyright: Stephen Stanley <stephen_stanley@ntmpng.org>
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


Overview:

CLA importer is an Addon for Anki 2.1. Upon installation a new menu item 'CLA Importer' will appear under Anki's
tools menu. This will open the CLA importer window.
The purpose of CLA importer is to create multimedia CLA cards easily in batches. 4 selction areas correspond to 4
field to import into Anki 'Picture' for images, 'audio' for language recording,'prompt' for a question and 'response'
for the answer to the question.

An example would be a 'picture' = picture of a dog, 'audio' = voice recording of a language helper, 'prompt' = em wanem
samting?, response = 'em i dok'.

The importer window provides a place to load all the audio and image files, then drag into the correct order (so audio and
image match) and then writing of the prompt and response.
Clicking import will then create a card for each row using a 'CLA Card' template.


Installation:

REQUIRES Anki 2.1
Anki 2.1 is currently in beta (it's being tested). Download the latest version here https://apps.ankiweb.net/downloads/beta/
This Addon is not compatible with Anki 2.0 (the version you get if you download regular Anki) and compatibilty with 2.0
is not planned.

The addon is packaged as a zip file. Locate the Anki addons21 folder:
(default) Windows: C:\Users\*current user*\AppData\Roaming\Anki2\addons21  (note, AppData is usually a hidden folder)
(default) Mac: /Library/Application Support/Anki2

Unzip the contents of the zipped folder to a new folder named CLA Importer in the addons21 folder: \Anki2\addons21\CLA Importer
Anki will scan the addon folder at startup. Next time Anki is started you should see CLA Importer under the tools menu.


How it works:

CLA importer will take the information you give it by arranging the four tables and create a temporary text file to import.
It then uses Anki's importer to create cards.
Images are copied, resized to 600 pixels and moved into the collection.media folder of your current Anki user.
Audio is copied and moved to the collection.media folder.

The original image and audio files can then be moved or deleted, Anki has copies of them itself and will continue to 
function.
Imports are tagged with an import number - this enables filtering in the Anki Broswer to pull up a desired batch for
editing or deletion after a mistaken import.


Bug reports and suggestions:

Send by email to stephen_stanley@ntmpng.org

To help me debug it would be helpful if you did the following: 
Open __init__.py in a text editor.
go to line 7 logging.basicConfig(filename='logfile.log',level=logging.INFO)
change to    logging.basicConfig(filename='logfile.log',level=logging.DEBUG)
Use CLA Importer again and repeat the steps that caused the bug.
Email a description of the bug, the circumstances that caused it and logfile.log
