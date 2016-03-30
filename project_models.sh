#!/bin/bash

python manage.py project_models 2 > $(date '+%d_%m_%Y').dat
