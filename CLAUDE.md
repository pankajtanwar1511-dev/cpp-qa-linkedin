# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Project Overview

**LinkedIn C++ Q&A Auto Poster** - Automated posting system for interactive C++ question/answer content on LinkedIn. Posts engaging C++ challenges and automatically reveals answers 1 hour later as comments.

## Repository Purpose

This is a **separate automation system** from the main PDF carousel posting (autolinkedin). It handles interactive Q&A posts with a unique two-stage workflow:

1. **Stage 1 (Question):** Post C++ code challenge with question image
2. **Wait 1 Hour:** Allow audience engagement
3. **Stage 2 (Answer):** Auto-comment with answer and explanation

## Repository Structure

```
cpp-qa-linkedin/
├── automation/
│   ├── qa_poster.py          # Main Q&A posting script (360 lines)
│   └── linkedin_api_v2.py    # LinkedIn API client with image/comment support (540 lines)
├── config/
│   ├── .env.example          # Credentials template
│   └── .env                  # LinkedIn API credentials (GITIGNORED)
├── tracker/
│   └── qa_tracker.txt        # Progress tracking for 45 posts
├── logs/
│   ├── qa_history.json       # Complete posting history
│   ├── pending_comments.json # Queue of posts awaiting 1-hour answer
│   └── qa_posting.log        # Debug/error logs
├── .gitignore
├── README.md                 # User-facing documentation
├── CLAUDE.md                 # This file - AI assistant context
├── requirements.txt          # Python dependencies
└── .github/
    └── workflows/
        └── post-qa.yml       # (Future) GitHub Actions automation
```

## Key Files Explained

### 1. automation/qa_poster.py

**Main posting automation script**

**Key Classes:**
- `CPPQAPoster` - Main orchestrator class

**Key Methods:**
- `get_next_qa_post()` - Reads tracker, finds next `[ ]` post
- `post_question()` - Stage 1: Posts question with image
- `post_pending_answers()` - Stage 2: Posts answers after 1 hour
- `save_pending_comment()` - Adds post to 1-hour queue
- `mark_question_posted()` - Updates tracker: `[ ]` → `[Q]`
- `mark_answer_posted()` - Updates tracker: `[Q]` → `[X]`

**Command Line Interface:**
```bash
--test-connection      # Test LinkedIn API
--post-question        # Post next question (Stage 1)
--post-answers         # Post pending answers (Stage 2)
--auto                 # Auto-decide: question OR answers
--dry-run              # Test without posting
```

**Workflow Logic:**
```python
# Auto mode decision tree:
1. Check pending_comments.json
2. If any answers ready (1+ hours old):
   → Post those answers
   → Exit
3. Else:
   → Post next question
   → Add to pending queue
   → Exit
```

### 2. automation/linkedin_api_v2.py

**Enhanced LinkedIn API client** (supports PDFs, images, and comments)

**Key Methods:**
- `upload_image()` - Upload PNG/JPG to LinkedIn
- `post_image()` - Create post with image
- `add_comment()` - Add comment to post (with optional image)
- `upload_document()` - Upload PDF (for main carousel system)
- `post_pdf()` - Create post with PDF (for main carousel system)

**API Endpoints Used:**
- `POST /rest/images?action=initializeUpload` - Initialize image upload
- `PUT <uploadUrl>` - Upload image binary
- `POST /rest/posts` - Create LinkedIn post
- `POST /rest/socialActions/{urn}/comments` - Add comment

**Authentication:**
- OAuth 2.0 Bearer token
- Required scope: `w_member_social`
- Credentials in `config/.env`

### 3. tracker/qa_tracker.txt

**Progress tracking file**

**Format:**
```
[ ] Post 1  | Virtual Destructor Memory Leak
[Q] Post 2  | Range-Based For Loop on Temporary
[X] Post 3  | Dangling Reference Bug
```

**Status Symbols:**
- `[ ]` - Not posted yet
- `[Q]` - Question posted, waiting for answer
- `[X]` - Complete (both question + answer posted)

**Next Post Logic:**
```python
# Find first line starting with "[ ]"
for line in tracker:
    if line.startswith('[ ]'):
        return parse_post_number(line)
```

### 4. logs/pending_comments.json

**1-Hour Answer Queue**

**Purpose:** Stores posts that need answers after 1 hour

**Schema:**
```json
[
  {
    "post_num": 1,
    "post_urn": "urn:li:share:7123456789",
    "answer_path": "/path/to/01_answer.txt",
    "answer_image_path": "/path/to/01_answer_image.png",
    "posted_at": "2026-04-16T12:00:00+00:00",
    "comment_at": "2026-04-16T13:00:00+00:00"
  }
]
```

**Cleanup Logic:**
- Items removed after answer posted
- Checked on every `--post-answers` run
- Only posts comments if current_time >= comment_at

## Content Files Location

**IMPORTANT:** Content files are IN this repository but GITIGNORED!

**Location:** `data/data/` (relative to repo root)

**File Naming:**
- `01_content.txt` - Question caption for Post 1
- `01_question_image.png` - Code screenshot for Post 1
- `01_answer.txt` - Answer comment text for Post 1
- `01_answer_image.png` - Explanation diagram for Post 1
- ... (repeat for posts 02-45)

**Total:** 180 files (45 posts × 4 files each)

**Git Strategy:**
- Content files are GITIGNORED (large PNG/TXT files)
- Not committed to repository
- Stored locally in `data/data/` directory
- Documentation files (`data/*.md`) ARE committed

## Posting Schedule

**Target:** 1 Q&A post per day at **9:00 PM JST**

**Implementation Options:**

### Option 1: Cron Job (Simple)
```bash
# Run at 9 PM JST (12:00 UTC)
0 12 * * * cd ~/cpp-qa-linkedin && python3 automation/qa_poster.py --auto
```

### Option 2: GitHub Actions (Advanced)
```yaml
schedule:
  - cron: '0 12 * * *'  # 9 PM JST
```

**Auto Mode Strategy:**
- Morning runs: Post answers (if any pending from yesterday)
- Evening runs: Post next question
- Naturally staggers question/answer by 1 day

## Workflow Examples

### Typical Day Flow

**Day 1 - 9:00 PM JST:**
```bash
python3 automation/qa_poster.py --auto
# → No pending answers
# → Posts Question 1
# → Tracker: [ ] → [Q]
# → Adds to pending_comments.json (comment_at = 10:00 PM JST)
```

**Day 1 - 10:00 PM JST** (1 hour later):
```bash
python3 automation/qa_poster.py --auto
# → Found pending answer for Post 1
# → Posts Answer 1 as comment
# → Tracker: [Q] → [X]
# → Removes from pending_comments.json
```

**Day 2 - 9:00 PM JST:**
```bash
python3 automation/qa_poster.py --auto
# → No pending answers
# → Posts Question 2
# → Tracker: [ ] → [Q]
# → Adds to pending queue
```

**Timeline:**
- **Post 1:** Question on Day 1 @ 9 PM, Answer on Day 1 @ 10 PM
- **Post 2:** Question on Day 2 @ 9 PM, Answer on Day 2 @ 10 PM
- ... repeat for 45 days

## API Rate Limits

**LinkedIn API Limits:**
- Free tier: 100 requests/day
- Verified app: 500 requests/day

**This App Usage:**
- Question post: 3 API calls (initialize, upload, post)
- Answer comment: 3 API calls (initialize, upload, comment)
- Total per Q&A: 6 API calls
- Well within limits ✅

## Error Handling

**Common Errors:**

1. **Missing content files**
   - Error: `Content file not found`
   - Fix: Check `data/data/` directory exists and contains files

2. **API connection failed**
   - Error: `Connection failed: 401`
   - Fix: Regenerate `LINKEDIN_ACCESS_TOKEN` in config/.env

3. **Image upload failed**
   - Error: `Image upload failed: 413`
   - Fix: Reduce image size (max 5MB)

4. **Comment failed**
   - Error: `Comment failed: 404`
   - Fix: Post URN may be invalid, check logs

**Logging:**
- All errors logged to `logs/qa_posting.log`
- Failed events tracked in `logs/qa_history.json`

## Integration with Main System

**Relationship to autolinkedin:**

| Feature | autolinkedin | cpp-qa-linkedin |
|---------|--------------|------------------|
| **Content** | PDF carousels | Q&A images |
| **Format** | 10-15 slide PDFs | Single question/answer images |
| **Posting** | 1-2 posts/day | 1 post/day |
| **Schedule** | Morning + Evening | Evening only (9 PM JST) |
| **Interaction** | Passive | Interactive (questions) |
| **API** | Documents API | Images + Comments API |
| **Repository** | autolinkedin | cpp-qa-linkedin |

**Both systems:**
- Share same LinkedIn credentials
- Run independently
- Use separate trackers
- Post to same LinkedIn profile

## Development Guidelines

### When Adding Features:

1. **Update tracker format?**
   - Modify `tracker/qa_tracker.txt`
   - Update `get_next_qa_post()` parsing logic

2. **Change posting logic?**
   - Modify `qa_poster.py`
   - Update `--auto` decision tree
   - Test with `--dry-run` first

3. **Add API functionality?**
   - Extend `linkedin_api_v2.py`
   - Add error handling
   - Update README examples

4. **Change schedule?**
   - Update cron jobs
   - Modify GitHub Actions workflow
   - Update README documentation

### Testing Checklist:

```bash
# 1. Test connection
python3 automation/qa_poster.py --test-connection

# 2. Dry run question
python3 automation/qa_poster.py --post-question --dry-run

# 3. Real question post (test with Post 1)
python3 automation/qa_poster.py --post-question

# 4. Check pending queue
cat logs/pending_comments.json

# 5. Wait 1 hour, then dry run answer
python3 automation/qa_poster.py --post-answers --dry-run

# 6. Real answer post
python3 automation/qa_poster.py --post-answers

# 7. Verify tracker updated
grep "Post 1" tracker/qa_tracker.txt
# Should show: [X] Post 1 | ...
```

## Security Considerations

**Sensitive Files:**
- `config/.env` - GITIGNORED ✅
- `logs/*.json` - GITIGNORED ✅
- `logs/*.log` - GITIGNORED ✅

**Public Files:**
- All code in `automation/`
- Tracker file (no sensitive data)
- README and documentation

**GitHub Secrets (for Actions):**
- `LINKEDIN_ACCESS_TOKEN`
- `LINKEDIN_USER_ID`

## Metrics and Analytics

**Track via logs/qa_history.json:**

```python
# Example analysis:
import json
with open('logs/qa_history.json') as f:
    history = json.load(f)

# Success rate
total = len(history)
successful = sum(1 for h in history if h['success'])
print(f"Success rate: {successful/total*100:.1f}%")

# Posts per day
from collections import Counter
dates = [h['calendar_date_jst'] for h in history]
print(Counter(dates))
```

## Future Enhancements

**Potential Features:**

1. **Analytics Integration**
   - Fetch post engagement metrics
   - Track likes, comments, shares
   - Identify top-performing topics

2. **Smart Scheduling**
   - Analyze best posting times
   - Adjust based on audience engagement
   - A/B test question formats

3. **Answer Delay Variations**
   - Configurable delay (30 min, 2 hours, etc.)
   - Based on question difficulty
   - Based on engagement level

4. **Multi-Platform**
   - Cross-post to Twitter/X
   - Adapt format for other platforms
   - Unified posting dashboard

## Troubleshooting Guide

### Issue: "All posts complete" but tracker shows TODO

**Cause:** Tracker file corrupted or incorrectly formatted

**Fix:**
```bash
# Check tracker format
head -50 tracker/qa_tracker.txt

# Ensure lines start with "[ ]", "[Q]", or "[X]"
# Ensure format: [X] Post N | Topic Title
```

### Issue: Answers not posting after 1 hour

**Cause:** pending_comments.json timestamp issue

**Fix:**
```bash
# Check pending queue
cat logs/pending_comments.json | python3 -m json.tool

# Verify comment_at timestamp is in past
# If stuck, manually edit or delete pending item
```

### Issue: Duplicate posts

**Cause:** Tracker not updated after posting

**Fix:**
```bash
# Check if post marked in tracker
grep "Post N" tracker/qa_tracker.txt

# Manually update if needed:
# [ ] → [Q] after question posted
# [Q] → [X] after answer posted
```

## Quick Reference

**Most Common Commands:**
```bash
# Daily posting (9 PM JST)
cd ~/cpp-qa-linkedin
python3 automation/qa_poster.py --auto

# Check status
grep "^\[ \]" tracker/qa_tracker.txt | head -1  # Next post
grep "^\[Q\]" tracker/qa_tracker.txt | wc -l    # Awaiting answers
grep "^\[X\]" tracker/qa_tracker.txt | wc -l    # Completed
cat logs/pending_comments.json                   # Pending queue

# Troubleshooting
tail -50 logs/qa_posting.log                     # Recent logs
python3 automation/qa_poster.py --test-connection  # Test API
```

**File Locations:**
- Code: `~/cpp-qa-linkedin/`
- Content: `~/cpp-qa-linkedin/data/data/`
- Logs: `~/cpp-qa-linkedin/logs/`

---

**Last Updated:** April 16, 2026
**Status:** Active - Ready to post 45 Q&A posts
**Current Progress:** 0/45 posts complete
**Next Post:** Post 1 - Virtual Destructor Memory Leak
