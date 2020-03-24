# CLA Importer Anki addon

March 2020
Copyright: Stephen Stanley <stephen_stanley@ntmpng.org>
License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


### Overview:

CLA importer is an Addon for [Anki](https://apps.ankiweb.net/)
The purpose of CLA importer is to create multimedia cards easily in batches. Each card has a text prompt and image on the front and audio with a text response on the back.
Four columns represent each of the four fields. Images and audio can be previewed and dragged rows can be dragged around to match audio to image.  


### Installation:

REQUIRES Anki 2.1
Anki 2.1 is currently in beta (it's being tested). Download the latest version here https://apps.ankiweb.net/downloads/beta/
This Addon is not compatible with Anki 2.0 (the version you get if you download regular Anki) and compatibilty with 2.0
is not planned.

The addon is packaged as a zip file. Locate the Anki addons21 folder:
(default) Windows: C:\Users\*current user*\AppData\Roaming\Anki2\addons21  (note, AppData is usually a hidden folder)
(default) Mac: /Library/Application Support/Anki2

Unzip the contents of the zipped folder to a new folder named CLA Importer in the addons21 folder: \Anki2\addons21\CLA Importer
Anki will scan the addon folder at startup. Next time Anki is started you should see CLA Importer under the tools menu.


### How it works:

CLA importer will take the information you give it by arranging the four tables and create a temporary text file to import.
It then uses Anki's importer to create cards.
Images are copied, resized to 600 pixels and moved into the collection.media folder of your current Anki user.
Audio is copied and moved to the collection.media folder.

The original image and audio files can then be moved or deleted, Anki has copies of them itself and will continue to 
function.
Imports are tagged with an import number - this enables filtering in the Anki Broswer to pull up a desired batch for
editing or deletion after a mistaken import.