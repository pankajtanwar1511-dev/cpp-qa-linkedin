#!/usr/bin/env python3
"""
Extract all 45 answers from ALL_45_LINKEDIN_POSTS.md and restore to individual files
"""

import re
import os

def extract_answers_from_master():
    """Extract all answers from the master document"""

    master_file = 'data/ALL_45_LINKEDIN_POSTS.md'

    with open(master_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all POST sections (## POST N:)
    post_pattern = r'## POST (\d+):.*?\n(.*?)(?=\n## POST|\n## 🎉|$)'
    posts = re.findall(post_pattern, content, re.DOTALL)

    answers = {}

    for post_num, post_content in posts:
        # Find answer section within this post
        answer_pattern = r'### Answer Comment.*?:\n\n(.*?)(?=\n---\n|$)'
        answer_match = re.search(answer_pattern, post_content, re.DOTALL)

        if answer_match:
            answer_text = answer_match.group(1).strip()
            answers[int(post_num)] = answer_text
            print(f"✓ Extracted answer for Post {post_num} ({len(answer_text)} chars)")
        else:
            print(f"✗ Could not find answer for Post {post_num}")

    return answers

def write_answers_to_files(answers):
    """Write extracted answers to individual files"""

    data_dir = 'data/data'

    for post_num, answer_text in sorted(answers.items()):
        # Format filename as 01, 02, ..., 45
        filename = f"{post_num:02d}_answer.txt"
        filepath = os.path.join(data_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(answer_text)

        file_size = os.path.getsize(filepath)
        print(f"✓ Wrote {filepath} ({file_size} bytes)")

def main():
    print("=" * 60)
    print("Restoring all 45 answer files from master document")
    print("=" * 60)
    print()

    print("Step 1: Extracting answers from ALL_45_LINKEDIN_POSTS.md")
    print("-" * 60)
    answers = extract_answers_from_master()
    print()

    print(f"Extracted {len(answers)} answers")
    print()

    print("Step 2: Writing answers to individual files")
    print("-" * 60)
    write_answers_to_files(answers)
    print()

    print("=" * 60)
    print(f"✅ Successfully restored {len(answers)}/45 answer files!")
    print("=" * 60)

if __name__ == '__main__':
    main()
