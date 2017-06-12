The script pulls new translations (ts files) from transifex. If some new translations are found,
it creates qm files and uploads them to S3.
It also compute a hash and the file size of the file and store them in a file (`details.json`) which is also uploaded on S3.

MuseScore Resource Manager can then poll this file to check if there are new translations available.


The python script `tx2s3.py` is run periodically by Travis-CI. The minimum cron period on Travis is once per day.
The `trigger_build.sh` can be used to trigger a build. It can also be used as a model to write a webapp to trigger a build.
