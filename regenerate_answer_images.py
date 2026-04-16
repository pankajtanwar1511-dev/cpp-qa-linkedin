#!/usr/bin/env python3
"""
Regenerate all 45 answer images with proper width to avoid truncation
"""

import re
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Image settings
BG_COLOR = '#1a1a1a'  # Dark background
TEXT_COLOR = '#ffffff'  # White text
CODE_COLOR = '#a8c5ff'  # Light blue for code
KEYWORD_COLOR = '#8be9fd'  # Cyan for keywords
HEADING_COLOR = '#ffffff'  # White for headings
COMMENT_COLOR = '#6272a4'  # Gray for comments

# Wider canvas to prevent truncation
IMAGE_WIDTH = 1400  # Increased from ~1200
PADDING = 40
LINE_SPACING = 8

def load_font(size):
    """Load monospace font for code"""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf',
        '/System/Library/Fonts/Courier.dfont',
        'C:\\Windows\\Fonts\\consola.ttf',
    ]

    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()

def load_bold_font(size):
    """Load bold font for headings"""
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf',
    ]

    for path in font_paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    return load_font(size)

def extract_answers_from_master():
    """Extract all answers from the master document"""
    master_file = 'data/ALL_45_LINKEDIN_POSTS.md'

    with open(master_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all POST sections
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

    return answers

def format_line_with_colors(line):
    """Determine color for a line based on content"""
    line_stripped = line.strip()

    # Headings (bold white)
    if line_stripped.startswith('**') and line_stripped.endswith('**'):
        return ('bold', HEADING_COLOR, line_stripped.strip('*').strip())

    # Code blocks (light blue)
    if line_stripped.startswith('```') or line_stripped in ['```', '```cpp', '```python']:
        return ('code', CODE_COLOR, line_stripped)

    # Code keywords
    if any(kw in line for kw in ['virtual', 'const', 'std::', 'class', 'int', 'void', 'return', 'constexpr', 'template', 'auto']):
        return ('code', CODE_COLOR, line)

    # Comments
    if '//' in line:
        return ('normal', TEXT_COLOR, line)

    # Regular text
    return ('normal', TEXT_COLOR, line)

def wrap_text_intelligently(text, font, max_width):
    """Wrap text to fit within max_width"""
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))

    lines = []
    for paragraph in text.split('\n'):
        if not paragraph.strip():
            lines.append('')
            continue

        # Check if line fits
        bbox = draw.textbbox((0, 0), paragraph, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            lines.append(paragraph)
        else:
            # Wrap at word boundaries
            words = paragraph.split()
            current_line = ''

            for word in words:
                test_line = current_line + ' ' + word if current_line else word
                bbox = draw.textbbox((0, 0), test_line, font=font)
                test_width = bbox[2] - bbox[0]

                if test_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

    return lines

def create_answer_image(post_num, answer_text):
    """Create answer image for a post"""

    # Load fonts
    font_normal = load_font(22)
    font_bold = load_bold_font(26)
    font_code = load_font(20)

    # Split into lines
    raw_lines = answer_text.split('\n')

    # Wrap lines and determine formatting
    formatted_lines = []
    max_text_width = IMAGE_WIDTH - (2 * PADDING)

    in_code_block = False

    for line in raw_lines:
        # Detect code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            formatted_lines.append(('code', CODE_COLOR, line, font_code))
            continue

        # Format based on type
        fmt_type, color, text = format_line_with_colors(line)

        if fmt_type == 'bold':
            font = font_bold
        elif fmt_type == 'code' or in_code_block:
            font = font_code
        else:
            font = font_normal

        # Wrap if needed
        wrapped = wrap_text_intelligently(text, font, max_text_width)

        for wrapped_line in wrapped:
            formatted_lines.append((fmt_type, color, wrapped_line, font))

    # Calculate image height
    total_height = PADDING
    for _, _, _, font in formatted_lines:
        bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), 'Test', font=font)
        total_height += (bbox[3] - bbox[1]) + LINE_SPACING
    total_height += PADDING

    # Create image
    img = Image.new('RGB', (IMAGE_WIDTH, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw text
    y = PADDING
    for fmt_type, color, text, font in formatted_lines:
        if text.strip():  # Only draw non-empty lines
            draw.text((PADDING, y), text, font=font, fill=color)

        bbox = draw.textbbox((0, 0), text if text else 'X', font=font)
        y += (bbox[3] - bbox[1]) + LINE_SPACING

    return img

def main():
    print("=" * 70)
    print("Regenerating all 45 answer images (wider to prevent truncation)")
    print("=" * 70)
    print()

    # Extract answers
    print("Step 1: Extracting answers from master document...")
    print("-" * 70)
    answers = extract_answers_from_master()
    print(f"✓ Extracted {len(answers)} answers")
    print()

    # Generate images
    print("Step 2: Generating images...")
    print("-" * 70)

    output_dir = 'data/data'

    for post_num in sorted(answers.keys()):
        answer_text = answers[post_num]

        try:
            img = create_answer_image(post_num, answer_text)

            filename = f"{post_num:02d}_answer_image.png"
            filepath = os.path.join(output_dir, filename)

            img.save(filepath)

            file_size = os.path.getsize(filepath)
            print(f"✓ Post {post_num:02d}: {filepath} ({img.width}x{img.height}px, {file_size//1024}KB)")

        except Exception as e:
            print(f"✗ Post {post_num:02d}: ERROR - {e}")

    print()
    print("=" * 70)
    print(f"✅ Successfully regenerated {len(answers)}/45 answer images!")
    print(f"   New width: {IMAGE_WIDTH}px (prevents truncation)")
    print("=" * 70)

if __name__ == '__main__':
    main()
