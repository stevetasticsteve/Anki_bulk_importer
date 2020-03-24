# CLA Importer Anki addon

An Add-on for [Anki](https://apps.ankiweb.net/) that provides a user friendly front end for Anki's import function for 
creating multimedia cards easily in batches. Each card will have a text prompt and image on the front and audio with a text 
response on the back.

![screenshot](importer_screen.png)

- Images and audio can be previewed, no need to rename files to something recognisable
- Images and audio can be moved around so they match, no need to order them in a file explorer
- Images are automatically scaled to be suitable for a flashcard (Not HD!)
- Images and audio are added to Anki's collections.media folder
- Cards are created using a 'CLA card' template

## Getting started:
### Prerequisites
- [Anki 2.1](https://apps.ankiweb.net/)

### Installing
Clone or download the whole folder and place it in Anki's add-on folder. Next time Anki boots CLA importer will be
available under tools.

OS | Defailt add-on folder location
-----------------------------------
Windows | C:\Users\user\AppData\Roaming\Anki2\addons21
Mac OS  | /L/home/steve/.local/share/Anki2/addons21ibrary/Application Support/Anki2
Linux   | /home/user/.local/share/Anki2/addons21/

*AppData in Windows and .local in MacOS and Linux are hidden folders*


### How it works:

CLA importer will take the information you give it by arranging the four tables and create a temporary text file to import.
It then uses Anki's importer to create cards.
Images are copied, resized to 600 pixels and moved into the collection.media folder of your current Anki user.
Audio is copied and moved to the collection.media folder.

The original image and audio files can then be moved or deleted, Anki has copies of them itself and will continue to 
function.
Imports are tagged with an import number - this enables filtering in the Anki Broswer to pull up a desired batch for
editing or deletion after a mistaken import.