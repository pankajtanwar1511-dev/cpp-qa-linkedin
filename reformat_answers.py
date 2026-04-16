#!/usr/bin/env python3
"""
Reformat all answer sections in ALL_45_LINKEDIN_POSTS.md to avoid long lines
Maximum line length: 90 characters (based on benchmark)
"""

import re
import textwrap

MAX_LINE_LENGTH = 90

def wrap_line(line, max_width=MAX_LINE_LENGTH, subsequent_indent=''):
    """Intelligently wrap a long line"""
    if len(line) <= max_width:
        return [line]

    # Special cases - don't wrap
    if line.strip().startswith('```'):
        return [line]
    if line.strip().startswith('**') and line.strip().endswith('**'):
        return [line]  # Keep headings on one line
    if line.strip().startswith('- '):
        # Wrap list items
        prefix = line[:line.index('- ') + 2]
        content = line[line.index('- ') + 2:]
        wrapped = textwrap.fill(content, width=max_width,
                               initial_indent=prefix,
                               subsequent_indent=prefix)
        return wrapped.split('\n')

    # Wrap regular text
    wrapped = textwrap.fill(line, width=max_width,
                           break_long_words=False,
                           break_on_hyphens=False,
                           subsequent_indent=subsequent_indent)
    return wrapped.split('\n')

def reformat_answer_section(answer_text):
    """Reformat an answer section to avoid long lines"""
    lines = answer_text.split('\n')
    reformatted_lines = []

    in_code_block = False

    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            reformatted_lines.append(line)
            continue

        # Don't wrap inside code blocks
        if in_code_block:
            reformatted_lines.append(line)
            continue

        # Empty lines
        if not line.strip():
            reformatted_lines.append(line)
            continue

        # Check line length
        if len(line) <= MAX_LINE_LENGTH:
            reformatted_lines.append(line)
        else:
            # Wrap long line
            wrapped = wrap_line(line)
            reformatted_lines.extend(wrapped)

    return '\n'.join(reformatted_lines)

def reformat_master_document():
    """Reformat all answer sections in the master document"""

    with open('data/ALL_45_LINKEDIN_POSTS.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all answer sections
    pattern = r'(### Answer Comment.*?:)\n\n(.*?)(?=\n---\n)'

    def replace_answer(match):
        header = match.group(1)
        answer_text = match.group(2)

        # Reformat the answer
        reformatted = reformat_answer_section(answer_text)

        return f"{header}\n\n{reformatted}"

    # Replace all answer sections
    new_content = re.sub(pattern, replace_answer, content, flags=re.DOTALL)

    # Write back
    with open('data/ALL_45_LINKEDIN_POSTS.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

    return content, new_content

def analyze_changes(old_content, new_content):
    """Analyze what changed"""
    old_lines = old_content.split('\n')
    new_lines = new_content.split('\n')

    print(f"Old lines: {len(old_lines)}")
    print(f"New lines: {len(new_lines)}")
    print(f"Added lines: {len(new_lines) - len(old_lines)}")

def main():
    print("=" * 80)
    print("Reformatting ALL_45_LINKEDIN_POSTS.md")
    print(f"Maximum line length: {MAX_LINE_LENGTH} characters")
    print("=" * 80)
    print()

    print("Processing...")
    old_content, new_content = reformat_master_document()

    print("✓ Reformatted all 45 answer sections")
    print()

    analyze_changes(old_content, new_content)

    print()
    print("=" * 80)
    print("✅ Done! Now regenerate images with: python3 regenerate_answer_images.py")
    print("=" * 80)

if __name__ == '__main__':
    main()
