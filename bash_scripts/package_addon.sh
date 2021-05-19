#!/bin/bash

# run with parent directory as working dir. Packages addon for upload to anki web

zip -r ./bulk_importer.ankiaddon *
zip -d ./bulk_importer.ankiaddon *.sh