#!/bin/bash
sudo pigpiod
python3 -m pytest Data_logger_test.py
python3 -m pytest upload_test.py