#!/bin/bash
source ~/.profile
export PATH=$PATH:/usr/local/bin
cd ~/updateTranslation

echo "Updating translation on s3..."
python tx2s3.py
echo "Translation updated"
