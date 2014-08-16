import glob, subprocess
import os, sys, io
import time, hashlib, json

#needs to be equal or smaller than the cron
period=300
outputDir = "share/locale/"
s3Url = "s3://extensions.musescore.org/languages/"

def processTsFile(prefix, langCode, data):
	filename = prefix + '_' + lang_code
	tsFilePath = outputDir + filename + ".ts"
	qmFilePath = outputDir + filename + ".qm"
		
	# generate qm file
	lrelease = subprocess.Popen(['lrelease', tsFilePath, '-qm', qmFilePath])
	lrelease.communicate()
	
	# get qm file size
	file_size = os.path.getsize(qmFilePath)
	file_size = "%.2f" % (float(file_size) / 1024)
	
	#compute Qm file hash
	file = open(qmFilePath)
	hash_file = hashlib.sha1()
	hash_file.update(file.read())
	
	if lang_code not in data:
		data[lang_code] = {}
	#if prefix not in data[lang_code]
	#	data[lang_code][prefix] = {}

	data[lang_code]["file_name"] = filename + ".qm"
	data[lang_code]["name"] = langCodeNameDict[lang_code]
	data[lang_code]["hash"] = str(hash_file.hexdigest())
	data[lang_code]["file_size"] = file_size


#pull ts files from transifex, use .tx/config
pull = subprocess.Popen(['tx', '-q', 'pull', '-a'])
pull.communicate()


tsFilePaths = glob.glob(outputDir + "*.ts")
if "share/locale/mscore_en.ts" in tsFilePaths:
	tsFilePaths.remove("share/locale/mscore_en.ts")

newDetailsFile = False
translationChanged = False


#read languages.json and store language code and name
langCode_file = open("languages.json", "r+")
langCodeNameDict = json.load(langCode_file)  # language code --> name
langCode_file.close()

detailsJson = outputDir + "details.json"
# read details.json or create it
if os.path.isfile(detailsJson):
	json_file = open(outputDir + "details.json", "r+")
	data = json.load(json_file)
	json_file.close()
else:
	newDetailsFile = True
	data = {}
	data["type"] = "Languages"
	data["version"] = "2.0"


for lang_code, languageName in langCodeNameDict.iteritems():
	print lang_code
	filename = 'mscore_' + lang_code
	tsFilePath = outputDir + filename + ".ts"

	lang_time = int(os.path.getmtime(tsFilePath))
	cur_time = int(time.time())
	#print cur_time,lang_time,cur_time-lang_time
	
	# if the file has been updated, update or add entry in details.json
	if cur_time - lang_time < period or newDetailsFile:
		processTsFile("mscore", lang_code, data)
		push_s3 = subprocess.Popen(['s3cmd', 'put', '--acl-public', '--guess-mime-type', qmFilePath, s3Url + filename +'.qm'])
		push_s3.communicate()
		translationChanged = True

json_file = open(outputDir + "details.json", "w")
json_file.write(json.dumps(data, sort_keys=True, indent=4))
json_file.close()

if translationChanged:
	push_json=subprocess.Popen(['s3cmd','put','--acl-public', '--guess-mime-type', outputDir+'details.json', s3Url + 'details.json'])
	push_json.communicate()
	
	
