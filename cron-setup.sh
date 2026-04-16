#!/bin/bash
# LinkedIn C++ Q&A Posting - Cron Setup Script
#
# This script helps you set up automated posting via cron jobs
# Run this script to add cron jobs: bash cron-setup.sh

echo "=========================================="
echo "LinkedIn C++ Q&A Auto Poster - Cron Setup"
echo "=========================================="
echo ""
echo "This will add one cron job:"
echo "  • Post questions at 9:00 PM JST (12:00 UTC)"
echo ""
echo "Note: Answers must be posted manually via LinkedIn UI"
echo "      (LinkedIn Community Management API not available for individuals)"
echo ""
echo "Approach: Using --auto mode (smart decision logic)"
echo ""

# Get current crontab
CURRENT_CRON=$(crontab -l 2>/dev/null)

# Define new cron job
APP_DIR="$HOME/cpp-qa-linkedin"
CRON_JOB_QUESTION="0 12 * * * cd $APP_DIR && python3 automation/qa_poster.py --post-question >> logs/cron.log 2>&1"

# Check if jobs already exist
if echo "$CURRENT_CRON" | grep -q "cpp-qa-linkedin"; then
    echo "⚠️  LinkedIn Q&A cron jobs already configured!"
    echo ""
    echo "Current cron jobs:"
    crontab -l | grep cpp-qa-linkedin
    echo ""
    read -p "Do you want to replace them? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    # Remove old jobs
    CURRENT_CRON=$(echo "$CURRENT_CRON" | grep -v "cpp-qa-linkedin")
fi

# Add new job
NEW_CRON="$CURRENT_CRON
# LinkedIn C++ Q&A Auto Poster (Questions Only)
$CRON_JOB_QUESTION"

# Install new crontab
echo "$NEW_CRON" | crontab -

echo "✅ Cron job installed successfully!"
echo ""
echo "Scheduled job:"
echo "  📅 9:00 PM JST (12:00 UTC) - Post questions (automated)"
echo ""
echo "Remember: Post answers manually via LinkedIn UI"
echo ""
echo "Verify with: crontab -l"
echo "Check logs at: $APP_DIR/logs/cron.log"
echo ""
echo "To remove these jobs: crontab -e (then delete the lines)"
