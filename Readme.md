# Anki bulk importer

An Add-on for [Anki](https://apps.ankiweb.net/) that provides a user-friendly front end for Anki's import function for 
creating multimedia cards easily in batches. Each card will have a text prompt and image on the front and audio with a 
text response on the back.

This add-on was designed for language learners who need to created batches (20 a day is our goal) of cards that
emphasise hearing spoken language over interacting with written language.
Our team is busy learning a remote, unwritten language and thus we need to create all our own practice material.

**Confirmed working in Anki Version 2.1.0beta36**

![screenshot](icons/importer_screen.png)

- Images and audio can be previewed, no need to rename files to something recognisable
- Images and audio can be moved around so they match, no need to order them in a file explorer
- Images are automatically scaled to be suitable for a flashcard (Not HD!)
- Images and audio are added to Anki's collections.media folder
- Cards are created using a 'CLA card' template (CLA stands for Culture and Language Aquisition)

Once imported you are free to move or delete the source files as copies are now contained in Anki's media folder.

## Getting started:
### Prerequisites
- [Anki 2.1](https://apps.ankiweb.net/)

### Installing
Open Anki, navigate to tools/Add-ons. Click 'get Add-ons' and enter the code **1312111882**. Anki will download the add-on.
 Reboot Anki and bulk importer will be available under tools.

Alternatively download bulk_importer.ankiaddon (a zip file) from this repository. Unzip it into Anki's add-on folder in
 a folder named bulk_importer. Next time Anki boots bulk importer will be available under tools.

OS | Default add-on folder location
-- | --------------------------------
Windows | C:\Users\user\AppData\Roaming\Anki2\addons21
Mac OS  | /home/user/.local/share/Anki2/addons21ibrary/Application Support/Anki2
Linux   | /home/user/.local/share/Anki2/addons21/

*AppData in Windows and .local in MacOS and Linux are hidden folders*

## License
This project is licensed under the GPL-3.0 License - see 
[License](https://github.com/stevetasticsteve/Anki_bulk_importer/blob/master/LICENSE)
for details.
You are free to use, edit and redistribute this add-on.

## Authors
* **Steve Stanley**, Missionary involved in language learning - Initial work