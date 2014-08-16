The python script `tx2s3.py` is run periodically on MuseScore Mac OSX build server.

The script pulls new translations (ts files) from transifex. If some new translations are found, 
it creates qm files and uploads them to S3.
It also compute a hash and the file size of the file and store them in a file (`details.json`) which is also uploaded on S3/
MuseScore can them poll this file to check if there are new translations available.