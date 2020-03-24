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

Once imported you are free to move or delete the source files as copies are now contained in Anki's media folder.

## Getting started:
### Prerequisites
- [Anki 2.1](https://apps.ankiweb.net/)

### Installing
Clone or download the whole folder and place it in Anki's add-on folder. Next time Anki boots CLA importer will be
available under tools.

OS | Defailt add-on folder location
-- | --------------------------------
Windows | C:\Users\user\AppData\Roaming\Anki2\addons21
Mac OS  | /L/home/steve/.local/share/Anki2/addons21ibrary/Application Support/Anki2
Linux   | /home/user/.local/share/Anki2/addons21/

*AppData in Windows and .local in MacOS and Linux are hidden folders*

## License
This project is licensed under the GPL-3.0 License - see [License](https://github.com/stevetasticsteve/CLA_importer/blob/master/LICENSE)
for details.
You are free to use, edit and redistribute this add-on.