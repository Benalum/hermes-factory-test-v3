#!/usr/bin/env bash
set -euo pipefail

echo "Starting verification for Calculator API..."

# Create and activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the API in the background
# Use nohup to avoid SIGHUP and redirect output to a log file
nohup uvicorn app:app --host 127.0.0.1 --port 8000 > api.log 2>&1 &
API_PID=$!

# Function to kill the API on exit
cleanup() {
    echo "Cleaning up..."
    kill $API_PID || true
    rm -f api.log
}
trap cleanup EXIT

# Wait for the API to be ready
echo "Waiting for API to start..."
MAX_RETRIES=10
COUNT=0
until curl -s http://127.0.0.1:8000/docs > /dev/null; do
    C_COUNT=$((COUNT + 1))
    if [ $C_COUNT -ge $MAX_RETRIES ]; then
        echo "TIMEOUT: API failed to start in $MAX_RETRIES attempts"
        exit 1
    fi
    echo "Retry $C_COUNT/$MAX_RETRIES..."
    sleep 2
    COUNT=$C_COUNT
done

# Run the tests
echo "Running API tests..."
python3 test_api.py

echo "Verification successful!"
