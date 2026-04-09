#!/bin/bash

cd ~/Desktop/cogrob_ws/rasa/

rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml --enable-api
