#!/bin/bash

# Render Start Script for Chandigarh Policy Assistant
echo "🚀 Starting Chandigarh Policy Assistant on Render..."

# Validate environment
python render_env_check.py

# Start the application with gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - fast_hybrid_search_server:app 