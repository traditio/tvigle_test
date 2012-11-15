#!/bin/bash
if [ -f "tvigle_test.db" ]
then
    rm tvigle_test.db
fi
python migrations/manage.py version_control sqlite:///tvigle_test.db migrations
python migrations/manage.py upgrade sqlite:///tvigle_test.db migrations