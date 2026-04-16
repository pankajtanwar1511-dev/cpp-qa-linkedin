# LinkedIn C++ Q&A Auto Poster

**Automated LinkedIn posting system for interactive C++ Q&A content.**

Post engaging C++ questions with automatic answer reveals after 1 hour.

---

## 📋 Overview

This app automates posting **45 C++ Q&A questions** to LinkedIn daily:

1. **Post Question** (Automated) - Share code challenge with question image at 9 PM JST
2. **Post Answer** (Manual) - Add answer comment via LinkedIn UI when ready

**Status:** Questions automated ✅ | Answers manual (API limitation)

---

## 🎯 How It Works

### Simplified Posting Workflow

```
Stage 1: POST QUESTION (AUTOMATED)
┌─────────────────────────────┐
│ Post: XX_content.txt        │
│ Image: XX_question_image.png│
│ Status: [ ] → [Q]           │
│ Time: 9:00 PM JST daily     │
└─────────────────────────────┘
           ↓
Stage 2: POST ANSWER (MANUAL)
┌─────────────────────────────┐
│ Comment via LinkedIn UI     │
│ Copy: XX_answer.txt         │
│ Attach: XX_answer_image.png │
│ Status: [Q] → [X]           │
│ Time: Your choice           │
└─────────────────────────────┘
```

**Why Manual Answers?**
LinkedIn's Community Management API (required for automated comments) is only available to approved business entities, not individual developers.

### Example Post

**Question Post (Stage 1):**
```
Valgrind showed me memory leaks I was certain didn't exist.
I'd tested the code. Everything worked. But every time I ran
Valgrind, there were leaks.

Why does this matter?
• Common resource leak pattern in C++ code
• Undefined behavior that can crash in production
• Core C++ rule: always use virtual destructor for polymorphic base classes

What's the output here? 👇
[Image: Code showing missing virtual destructor]

Comment your answer. I'll explain in comments later.

#cpp #cplusplus #programming
```

**Answer Comment (1 hour later):**
```
**Output:** A, B, ~A (notice ~B is missing!)
Full explanation in the image below 👇
[Image: Detailed explanation with diagrams]
```

---

## 📂 Directory Structure

```
cpp-qa-linkedin/
├── automation/
│   ├── qa_poster.py          # Main Q&A posting script
│   └── linkedin_api_v2.py    # LinkedIn API client (images + comments)
├── config/
│   ├── .env.example          # Credentials template
│   └── .env                  # Your credentials (gitignored)
├── tracker/
│   └── qa_tracker.txt        # Progress tracking (45 posts)
├── logs/
│   ├── qa_history.json       # Post history log
│   ├── pending_comments.json # 1-hour answer queue
│   └── qa_posting.log        # Debug logs
├── .gitignore
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

**Content files** (gitignored - not committed):
- Located in: `data/data/`
- 4 files per post (45 posts = 180 files)
- Excluded from git (large PNG/TXT files)

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Python 3.10+
python3 --version

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup LinkedIn API Credentials

```bash
# Copy example config
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env
```

Required credentials:
- `LINKEDIN_ACCESS_TOKEN` - OAuth 2.0 token with `w_member_social` scope
- `LINKEDIN_USER_ID` - Your LinkedIn URN (e.g., `urn:li:person:abc123`)

### 3. Test Connection

```bash
cd ~/cpp-qa-linkedin
python3 automation/qa_poster.py --test-connection
```

### 4. Post Your First Q&A

**Dry run (test without posting):**
```bash
python3 automation/qa_poster.py --post-question --dry-run
```

**Post for real:**
```bash
python3 automation/qa_poster.py --post-question
```

**Post pending answers:**
```bash
# Run this after 1 hour to post answers
python3 automation/qa_poster.py --post-answers
```

**Auto mode (recommended):**
```bash
# Automatically decides: post question OR answers
python3 automation/qa_poster.py --auto
```

---

## 📊 Tracking Progress

### Tracker File Format

**Location:** `tracker/qa_tracker.txt`

**Status Symbols:**
- `[ ]` - TODO (not posted yet)
- `[Q]` - Question posted, awaiting 1-hour answer
- `[X]` - Complete (both question and answer posted)

**Example:**
```
[ ] Post 1  | Virtual Destructor Memory Leak
[Q] Post 2  | Range-Based For Loop on Temporary
[X] Post 3  | Dangling Reference Bug
```

### Check Progress

```bash
# Count completed posts
grep "^\[X\]" tracker/qa_tracker.txt | wc -l

# Count pending answers
grep "^\[Q\]" tracker/qa_tracker.txt | wc -l

# View next post
grep "^\[ \]" tracker/qa_tracker.txt | head -1
```

---

## 🤖 Automation Options

### Important: Questions Only - Answers Manual!

**The app automates question posting only:**
- Posts question at 9 PM JST → Updates tracker → **EXITS**
- Answers must be posted manually via LinkedIn UI (API limitation)
- Tracker shows [Q] status until you manually add answer and mark [X]

### Option 1: Manual (Recommended for Testing)

```bash
# Post question
python3 automation/qa_poster.py --post-question

# 1 hour later: Post answer
python3 automation/qa_poster.py --post-answers

# OR use auto mode (decides question vs answer automatically)
python3 automation/qa_poster.py --auto
```

### Option 2: Cron Job (Recommended for Production)

**Quick setup using provided script:**
```bash
bash cron-setup.sh
```

**Manual crontab setup:**
```bash
# Edit crontab
crontab -e

# Add this line (9 PM JST = 12:00 UTC):
0 12 * * * cd ~/cpp-qa-linkedin && python3 automation/qa_poster.py --post-question >> logs/cron.log 2>&1
```

**How it works:**
```
9:00 PM JST - Cron job runs
├─ Posts next question automatically
├─ Updates tracker: [ ] → [Q]
└─ App exits ✅

Manual (your choice) - Add answer via LinkedIn:
├─ Go to LinkedIn post
├─ Add comment with answer text + image
└─ Update tracker: [Q] → [X] (optional)
```

### Option 3: GitHub Actions (Advanced)

Create `.github/workflows/post-qa.yml`:

```yaml
name: Post C++ Q&A Questions

on:
  schedule:
    - cron: '0 12 * * *'  # Daily at 9 PM JST (12:00 UTC)
  workflow_dispatch:

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python3 automation/qa_poster.py --post-question
        env:
          LINKEDIN_ACCESS_TOKEN: ${{ secrets.LINKEDIN_ACCESS_TOKEN }}
          LINKEDIN_USER_ID: ${{ secrets.LINKEDIN_USER_ID }}
```

**Note:** This workflow file already exists at `.github/workflows/post-qa.yml` and is active.

---

## 📝 Content File Requirements

Each Q&A post requires **4 files** in `data/data/`:

| File | Purpose | Example |
|------|---------|---------|
| `NN_content.txt` | Question caption | Story + "What's the output?" |
| `NN_question_image.png` | Code screenshot | C++ code with bug |
| `NN_answer.txt` | Answer comment text | "Output: A, B, ~A..." |
| `NN_answer_image.png` | Explanation diagram | Full solution with notes |

**File naming:**
- `01_content.txt`, `01_question_image.png`, etc. (for Post 1)
- `02_content.txt`, `02_question_image.png`, etc. (for Post 2)
- ... up to `45_*`

---

## 🔧 Advanced Usage

### Command Reference

```bash
# Test connection
python3 automation/qa_poster.py --test-connection

# Post next question (dry run)
python3 automation/qa_poster.py --post-question --dry-run

# Post next question (real)
python3 automation/qa_poster.py --post-question

# Post pending answers
python3 automation/qa_poster.py --post-answers

# Auto mode (question OR answers)
python3 automation/qa_poster.py --auto

# View help
python3 automation/qa_poster.py --help
```

### Pending Comments Queue

**File:** `logs/pending_comments.json`

Stores posts waiting for 1-hour answer:

```json
[
  {
    "post_num": 1,
    "post_urn": "urn:li:share:123456789",
    "answer_path": "/path/to/01_answer.txt",
    "answer_image_path": "/path/to/01_answer_image.png",
    "posted_at": "2026-04-16T00:00:00+00:00",
    "comment_at": "2026-04-16T01:00:00+00:00"
  }
]
```

### Post History Log

**File:** `logs/qa_history.json`

Tracks all posting events:

```json
[
  {
    "timestamp": "2026-04-16T00:00:00+00:00",
    "calendar_date_jst": "2026-04-16",
    "post_number": 1,
    "topic": "Virtual Destructor Memory Leak",
    "event_type": "question_posted",
    "success": true,
    "post_urn": "urn:li:share:123456789"
  }
]
```

---

## 🔍 Troubleshooting

### Issue: "Connection failed"
**Solution:** Check `config/.env` credentials

### Issue: "Content file not found"
**Solution:** Ensure files exist in `data/data/` directory

### Issue: "Failed to upload image"
**Solution:**
- Check image file format (PNG/JPG)
- Verify file size < 5MB
- Check LinkedIn API rate limits

### Issue: "Comment failed"
**Solution:**
- Verify post URN is correct
- Check if 1 hour has actually passed
- Ensure w_member_social permission granted

---

## 📈 Content Statistics

- **Total Posts:** 45 C++ Q&A challenges
- **Format:** Question image (800x600px) + Answer diagram (1200x800px)
- **Topics:**
  - Memory management bugs
  - RAII and resource safety
  - Move semantics and performance
  - Template metaprogramming
  - C++20 features
  - Concurrency pitfalls
  - STL gotchas

---

## 🔐 Security Notes

- **Never commit `.env` file** (already in `.gitignore`)
- **Never share access tokens** publicly
- **Rotate tokens** if compromised
- **Use secrets** for GitHub Actions (not hardcoded)

---

## 📚 Related Projects

- **autolinkedin** - Main PDF carousel posting system
- **linkedin_posts_qa/data** - Q&A content files (images + text)

---

## 🛠️ Development

### Running Tests

```bash
# Test with dry run
python3 automation/qa_poster.py --post-question --dry-run
python3 automation/qa_poster.py --post-answers --dry-run
```

### Debugging

```bash
# Check logs
tail -f logs/qa_posting.log

# Check pending queue
cat logs/pending_comments.json | python3 -m json.tool

# Check history
cat logs/qa_history.json | python3 -m json.tool
```

---

## 📧 Support

Questions or issues? Check:
1. Tracker file status
2. Log files in `logs/`
3. LinkedIn API documentation

---

## 📄 License

MIT License - Feel free to use and modify

---

**Created:** April 2026
**Status:** Active - Ready to post
**Posts Remaining:** 45/45

🚀 Happy Posting!
