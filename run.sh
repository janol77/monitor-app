#!/bin/bash
find . -name "*.pyc" -exec rm -rf {} \;
clear
cd app
python -m server
