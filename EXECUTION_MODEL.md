# Execution Model: Cron Job Approach

## Overview

The LinkedIn C++ Q&A Auto Poster uses a **stateless cron job approach** rather than running continuously. This document explains how the 1-hour delay works without keeping the app running.

---

## Key Concept: Stateless Execution

**The app does NOT wait for 1 hour!**

- Each run is independent
- State is stored in JSON files
- Cron scheduler handles timing
- App exits after each run

---

## State Persistence

### Files Used for State

| File | Purpose | When Modified |
|------|---------|---------------|
| `tracker/qa_tracker.txt` | Track post status (`[ ]` → `[Q]` → `[X]`) | Question/Answer posted |
| `logs/pending_comments.json` | Queue of posts awaiting 1-hour comment | Question posted (add), Answer posted (remove) |
| `logs/qa_history.json` | Complete event log | Every post/comment |
| `logs/qa_posting.log` | Debug/error logs | Every run |

### Pending Comments Queue Structure

**File:** `logs/pending_comments.json`

```json
[
  {
    "post_num": 1,
    "post_urn": "urn:li:share:7185046789123456789",
    "answer_path": "/home/pankaj/cpp-qa-linkedin/data/data/01_answer.txt",
    "answer_image_path": "/home/pankaj/cpp-qa-linkedin/data/data/01_answer_image.png",
    "posted_at": "2026-04-16T12:00:00+00:00",
    "comment_at": "2026-04-16T13:00:00+00:00"
  }
]
```

**Key fields:**
- `post_urn` - LinkedIn's unique post ID (used to add comment later)
- `comment_at` - Timestamp when answer should be posted (UTC)
- App checks: `current_time >= comment_at` before posting

---

## Detailed Execution Flow

### Day 1 - Question Posting

**Time:** 9:00 PM JST (12:00 UTC)
**Cron:** `0 12 * * * ... --auto`

```
┌─────────────────────────────────────────┐
│ CRON TRIGGERS: 9:00 PM JST              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 1. App starts: qa_poster.py --auto      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. Check pending_comments.json          │
│    → Empty (no pending answers)         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. Read tracker/qa_tracker.txt          │
│    → Find first [ ] post (Post 1)       │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. Read content files:                  │
│    - data/data/01_content.txt           │
│    - data/data/01_question_image.png    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. POST TO LINKEDIN                     │
│    ├─ Upload question image             │
│    ├─ Create post with caption          │
│    └─ Receive post_urn from LinkedIn    │
│       (e.g., urn:li:share:7185046...)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 6. Save to pending queue:               │
│    {                                    │
│      "post_num": 1,                     │
│      "post_urn": "urn:li:share:...",    │
│      "comment_at": "13:00:00+00:00"     │
│    }                                    │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 7. Update tracker:                      │
│    [ ] Post 1 → [Q] Post 1              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 8. Log to qa_history.json               │
│    (event_type: "question_posted")      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 9. APP EXITS ✅                          │
│    (NOT waiting! Cron will run again)   │
└─────────────────────────────────────────┘
```

**Files modified:**
- `tracker/qa_tracker.txt` ([ ] → [Q])
- `logs/pending_comments.json` (added 1 item)
- `logs/qa_history.json` (logged event)
- `logs/qa_posting.log` (debug log)

---

### Day 1 - Answer Posting (1 Hour Later)

**Time:** 10:00 PM JST (13:00 UTC)
**Cron:** `0 13 * * * ... --auto`

```
┌─────────────────────────────────────────┐
│ CRON TRIGGERS: 10:00 PM JST             │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 1. App starts: qa_poster.py --auto      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 2. Check pending_comments.json          │
│    → Found 1 item (Post 1)              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 3. Check timestamp:                     │
│    current_time: 13:00:00 UTC           │
│    comment_at:   13:00:00 UTC           │
│    → READY! (13:00 >= 13:00) ✅         │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 4. Read answer files:                   │
│    - data/data/01_answer.txt            │
│    - data/data/01_answer_image.png      │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 5. POST COMMENT TO LINKEDIN             │
│    ├─ Upload answer image               │
│    ├─ Create comment on post_urn        │
│    │   (using stored URN from step 1)   │
│    └─ LinkedIn adds comment to post     │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 6. Update tracker:                      │
│    [Q] Post 1 → [X] Post 1              │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 7. Remove from pending queue:           │
│    pending_comments.json → []           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 8. Log to qa_history.json               │
│    (event_type: "answer_posted")        │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│ 9. APP EXITS ✅                          │
└─────────────────────────────────────────┘
```

**Files modified:**
- `tracker/qa_tracker.txt` ([Q] → [X])
- `logs/pending_comments.json` (removed 1 item)
- `logs/qa_history.json` (logged event)
- `logs/qa_posting.log` (debug log)

---

### Day 2 - Next Question

**Time:** 9:00 PM JST (12:00 UTC)
**Cron:** `0 12 * * * ... --auto`

Same flow as Day 1, but:
- Finds `[ ] Post 2` in tracker
- Posts Question 2
- Cycles continue for 45 days

---

## Timeline Visualization

```
Day 1:
09:00 PM JST ┃ CRON → Post Question 1 → Save to pending queue → EXIT
             ┃ tracker: [ ] Post 1 → [Q] Post 1
             ┃ pending_comments.json: [Post 1 URN + comment_at: 10 PM]
             ┃
10:00 PM JST ┃ CRON → Check pending → Found Post 1 (ready) → Comment → EXIT
             ┃ tracker: [Q] Post 1 → [X] Post 1
             ┃ pending_comments.json: []
             ┃
Day 2:
09:00 PM JST ┃ CRON → Post Question 2 → Save to pending queue → EXIT
             ┃ tracker: [ ] Post 2 → [Q] Post 2
             ┃
10:00 PM JST ┃ CRON → Check pending → Found Post 2 (ready) → Comment → EXIT
             ┃ tracker: [Q] Post 2 → [X] Post 2
             ┃
...repeat for 45 days
```

---

## Why This Works Without Waiting

### Traditional Approach (BAD - Not Used)
```python
# Don't do this!
post_question()
time.sleep(3600)  # Wait 1 hour (app keeps running)
post_answer()
```

**Problems:**
- App must run for 1+ hour continuously
- Wastes resources
- Can crash during wait period
- Difficult to monitor

### Stateless Cron Approach (GOOD - What We Use)
```python
# What we actually do:

# Run 1 (9 PM):
post_question()
save_to_json(post_urn, comment_at="10 PM")
exit(0)  # App ends

# Run 2 (10 PM - separate cron job):
pending = load_from_json()
if current_time >= pending['comment_at']:
    post_answer(pending['post_urn'])
    remove_from_json(pending)
exit(0)  # App ends
```

**Advantages:**
- ✅ No continuous running
- ✅ Each run is independent
- ✅ Easy to monitor with cron logs
- ✅ Can manually trigger if needed
- ✅ State survives app crashes

---

## Auto Mode Decision Logic

When you run `python3 qa_poster.py --auto`, it decides what to do:

```python
def auto_mode():
    # 1. Check for pending answers first
    pending = load_pending_comments()

    for item in pending:
        if current_time >= item['comment_at']:
            # Found answer ready to post
            post_answer(item)
            return  # EXIT (don't post new question)

    # 2. No pending answers ready, post next question
    next_post = find_next_unposted()
    post_question(next_post)
    # EXIT
```

**This is why auto mode works:**
- 9 PM run: No pending → Posts question
- 10 PM run: Pending found → Posts answer (doesn't post new question)

---

## Cron Configuration

### Recommended Setup

```bash
# Add to crontab (run: crontab -e)

# Post questions and answers (9 PM and 10 PM JST = 12:00 and 13:00 UTC)
0 12 * * * cd ~/cpp-qa-linkedin && python3 automation/qa_poster.py --auto >> logs/cron.log 2>&1
0 13 * * * cd ~/cpp-qa-linkedin && python3 automation/qa_poster.py --auto >> logs/cron.log 2>&1
```

### Quick Setup Script

```bash
bash ~/cpp-qa-linkedin/cron-setup.sh
```

---

## Monitoring and Debugging

### Check Pending Queue

```bash
# View pending comments
cat ~/cpp-qa-linkedin/logs/pending_comments.json | python3 -m json.tool

# Count pending
cat ~/cpp-qa-linkedin/logs/pending_comments.json | python3 -c "import sys, json; print(len(json.load(sys.stdin)))"
```

### Check Tracker Status

```bash
cd ~/cpp-qa-linkedin

# Next post to publish
grep "^\[ \]" tracker/qa_tracker.txt | head -1

# Waiting for answers
grep "^\[Q\]" tracker/qa_tracker.txt

# Completed
grep "^\[X\]" tracker/qa_tracker.txt | wc -l
```

### Check Cron Logs

```bash
# View recent cron output
tail -50 ~/cpp-qa-linkedin/logs/cron.log

# View posting log
tail -50 ~/cpp-qa-linkedin/logs/qa_posting.log

# View full history
cat ~/cpp-qa-linkedin/logs/qa_history.json | python3 -m json.tool
```

---

## Troubleshooting

### Issue: Answers not posting after 1 hour

**Check:**
```bash
# 1. Verify pending queue has items
cat logs/pending_comments.json

# 2. Check timestamp format
python3 -c "
import json
from datetime import datetime, timezone
with open('logs/pending_comments.json') as f:
    pending = json.load(f)
    for item in pending:
        comment_at = datetime.fromisoformat(item['comment_at'])
        now = datetime.now(timezone.utc)
        print(f\"Post {item['post_num']}: {(now - comment_at).total_seconds() / 60:.0f} minutes since ready\")
"

# 3. Check if cron is running
crontab -l | grep cpp-qa-linkedin
```

### Issue: Duplicate posts

**Cause:** Tracker not updating after question posted

**Fix:**
```bash
# Manually update tracker
sed -i 's/\[ \] Post N /\[Q\] Post N /' tracker/qa_tracker.txt
```

---

## Summary

**Key Takeaways:**

1. **App does NOT wait** - Uses cron jobs for timing
2. **State in JSON files** - Survives app restarts
3. **post_urn is the key** - LinkedIn's unique post ID links question to answer
4. **Two cron jobs** - One at 9 PM (question), one at 10 PM (answer)
5. **Auto mode** - Smart decision: answer if pending, else question

**The "1-hour delay" is actually:**
- Save timestamp in JSON: `comment_at = now + 1 hour`
- Cron runs 1 hour later
- Check: `current_time >= comment_at`
- Post answer if ready

No continuous waiting required! 🎉
