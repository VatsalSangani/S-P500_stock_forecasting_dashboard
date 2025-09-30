#!/bin/bash
# =========================================================
# sync_s3.sh - Sync S&P 500 dashboard data from S3 → EC2
# =========================================================

# Exit on error
set -e

# S3 bucket name
BUCKET_NAME="sp500-dashboard-data"

# Local project data directory (inside EC2 repo)
LOCAL_DIR="$HOME/SP500_Dashboard/data"

echo "🔄 Syncing data from s3://$BUCKET_NAME to $LOCAL_DIR ..."

# Make sure local data directory exists
mkdir -p "$LOCAL_DIR/processed"
mkdir -p "$LOCAL_DIR/forecasts"
mkdir -p "$LOCAL_DIR/fundamentals"

# Sync processed stock data
aws s3 sync "s3://$BUCKET_NAME/processed" "$LOCAL_DIR/processed" --exact-timestamps

# Sync forecast files
aws s3 sync "s3://$BUCKET_NAME/forecasts" "$LOCAL_DIR/forecasts" --exact-timestamps

# Sync fundamentals
aws s3 sync "s3://$BUCKET_NAME/fundamentals" "$LOCAL_DIR/fundamentals" --exact-timestamps

echo "✅ Sync complete!"
echo "You can now run the dashboard with: python app.py"