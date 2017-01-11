#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python main.py
        ;;
    test)
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py adapterearthengine.wsgi:application
        ;;
    *)
        exec "$@"
esac
