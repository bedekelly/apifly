#!/bin/bash

# Recommended: use a reverse proxy to handle external traffic.
HOST=127.0.0.1
PORT=5000

# In general, use (2*CPU_CORES + 1) worker threads.
WORKER_THREADS=9

# Run gunicorn to multiplex requests across multiple threads.
gunicorn app:flask_app  \
	 -b $HOST:$PORT \
	 --workers=$WORKER_THREADS
