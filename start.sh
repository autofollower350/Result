#!/bin/bash

# Setup Chrome in /tmp
mkdir -p /tmp/chrome
wget -q https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.113/linux64/chrome-linux64.zip
unzip -q chrome-linux64.zip
mv chrome-linux64/* /tmp/chrome/

# Setup Chromedriver in /tmp
wget -q -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.113/linux64/chromedriver-linux64.zip
unzip -o chromedriver.zip
mv chromedriver-linux64/chromedriver /tmp/chrome/chromedriver
chmod +x /tmp/chrome/chromedriver

# Export paths for use in main.py
export CHROME_BIN=/tmp/chrome/chrome
export CHROMEDRIVER_PATH=/tmp/chrome/chromedriver

# Run bot
python3 main.py
