#!/usr/bin/env python3
"""
Meaningfully reformat all 45 answers with natural line breaks
Break at sentences, clauses, and logical boundaries
Max line length: 90 characters
"""

import re

MAX_LENGTH = 90

def break_at_natural_points(text, max_len=MAX_LENGTH):
    """Break text at natural points: sentences, clauses, conjunctions"""

    if len(text) <= max_len:
        return [text]

    # Try breaking at sentence boundaries first (.  or !  or ?)
    for sep in ['. ', '! ', '? ']:
        if sep in text:
            parts = text.split(sep)
            result = []
            current = ""

            for i, part in enumerate(parts):
                test_line = current + part + (sep if i < len(parts)-1 else '')

                if len(test_line.strip()) <= max_len:
                    current = test_line
                else:
                    if current:
                        result.append(current.strip())
                    current = part + (sep if i < len(parts)-1 else '')

            if current:
                result.append(current.strip())

            if all(len(line) <= max_len for line in result):
                return result

    # Try breaking at comma
    if ', ' in text:
        pos = text.rfind(', ', 0, max_len)
        if pos > max_len // 2:
            return [text[:pos+1].strip()] + break_at_natural_points(text[pos+2:].strip())

    # Try breaking at conjunctions
    for conj in [' but ', ' and ', ' or ', ' because ', ' when ', ' if ', ' which ', ' that ']:
        pos = text.rfind(conj, 0, max_len)
        if pos > max_len // 2:
            return [text[:pos].strip()] + break_at_natural_points(text[pos:].strip())

    # Try breaking after  → or : or -
    for sep in [' → ', ': ', ' - ']:
        pos = text.rfind(sep, 0, max_len)
        if pos > 0:
            return [text[:pos + len(sep)].strip()] + break_at_natural_points(text[pos + len(sep):].strip())

    # Last resort: break at last space
    pos = text.rfind(' ', 0, max_len)
    if pos > 0:
        return [text[:pos].strip()] + break_at_natural_points(text[pos+1:].strip())

    # Can't break nicely, return as-is
    return [text]

def reformat_answer(answer_text):
    """Reformat answer section with meaningful line breaks"""
    lines = answer_text.split('\n')
    result = []

    in_code_block = False
    in_list = False

    for line in lines:
        # Track code blocks - don't touch them
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Empty lines
        if not line.strip():
            result.append(line)
            in_list = False
            continue

        # Headings - keep as-is
        if line.strip().startswith('**') and line.strip().endswith('**') and line.strip().count('**') == 2:
            result.append(line)
            continue

        # List items
        if line.strip().startswith('- '):
            in_list = True
            if len(line) > MAX_LENGTH:
                # Break list item
                indent = line[:line.index('- ')]
                content = line[line.index('- ') + 2:]
                broken = break_at_natural_points(content)
                result.append(indent + '- ' + broken[0])
                for extra in broken[1:]:
                    result.append(indent + '  ' + extra)
            else:
                result.append(line)
            continue

        # Code lines (start with indent or contain specific keywords)
        if line.strip().startswith(('class ', 'void ', 'int ', 'auto ', 'template', 'std::', 'constexpr', '#include', 'return ')):
            result.append(line)
            continue

        # Continuation of list (indented after list item)
        if in_list and line.startswith('  '):
            result.append(line)
            continue

        # Regular text - check length and break if needed
        if len(line) <= MAX_LENGTH:
            result.append(line)
        else:
            # Long line - break it meaningfully
            broken = break_at_natural_points(line.strip())
            result.extend(broken)

    return '\n'.join(result)

def process_file():
    """Process the entire file"""

    with open('data/ALL_45_LINKEDIN_POSTS.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find answer sections
    pattern = r'(### Answer Comment.*?:)\n\n(.*?)(\n---\n)'

    def replace_answer(match):
        header = match.group(1)
        answer = match.group(2)
        separator = match.group(3)

        reformatted = reformat_answer(answer)

        return f"{header}\n\n{reformatted}{separator}"

    # Process all answers
    new_content = re.sub(pattern, replace_answer, content, flags=re.DOTALL)

    # Write back
    with open('data/ALL_45_LINKEDIN_POSTS.md', 'w', encoding='utf-8') as f:
        f.write(new_content)

    return content, new_content

def main():
    print("=" * 90)
    print("Reformatting ALL 45 ANSWERS with meaningful line breaks")
    print(f"Max line length: {MAX_LENGTH} characters")
    print("=" * 90)
    print()

    print("Processing all 45 answer sections...")
    old, new = process_file()

    old_lines = old.split('\n')
    new_lines = new.split('\n')

    print(f"✓ Reformatted 45 answers")
    print(f"  Old: {len(old_lines)} lines")
    print(f"  New: {len(new_lines)} lines")
    print(f"  Added: {len(new_lines) - len(old_lines)} lines (natural breaks)")
    print()
    print("=" * 90)
    print("✅ Done! Now regenerate images: python3 regenerate_answer_images.py")
    print("=" * 90)

if __name__ == '__main__':
    main()
