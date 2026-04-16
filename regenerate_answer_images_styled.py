#!/usr/bin/env python3
"""
Regenerate all 45 answer images with beautiful IDE-style syntax highlighting
Matching the style of question images
"""

import re
import os
from PIL import Image, ImageDraw, ImageFont

# Color scheme matching question images (VS Code Dark+ style)
BG_COLOR = '#2e2e2e'  # Dark background (matching question images)
TEXT_COLOR = '#d4d4d4'  # Light gray for regular text
HEADING_COLOR = '#ffffff'  # White for headings

# Code syntax highlighting colors (matching question images)
KEYWORD_COLOR = '#569cd6'  # Blue for keywords (class, int, void, return, etc.)
TYPE_COLOR = '#4ec9b0'  # Cyan for types
STRING_COLOR = '#ce9178'  # Orange for strings
NUMBER_COLOR = '#b5cea8'  # Light green for numbers
OPERATOR_COLOR = '#d4d4d4'  # White for operators
COMMENT_COLOR = '#6a9955'  # Green for comments
FUNCTION_COLOR = '#dcdcaa'  # Yellow for functions
CONSTANT_COLOR = '#4fc1ff'  # Bright cyan for constants

# Image settings
IMAGE_WIDTH = 1400
PADDING = 50
LINE_SPACING = 10

# C++ keywords
CPP_KEYWORDS = {
    'class', 'struct', 'public', 'private', 'protected', 'virtual', 'const',
    'int', 'void', 'bool', 'char', 'float', 'double', 'auto', 'typename',
    'template', 'return', 'if', 'else', 'for', 'while', 'do', 'switch',
    'case', 'break', 'continue', 'new', 'delete', 'nullptr', 'static',
    'constexpr', 'inline', 'namespace', 'using', 'typedef', 'enum',
    'std', 'true', 'false', 'this', 'override', 'final', 'explicit'
}

def load_font(size):
    """Load monospace font"""
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

def colorize_cpp_code(line):
    """Apply syntax highlighting to C++ code line"""
    # Simple but effective syntax highlighter
    colored_segments = []

    # Handle comments first
    if '//' in line:
        code_part = line[:line.index('//')]
        comment_part = line[line.index('//'):]
        # Colorize code part, then add comment
        if code_part:
            colored_segments.extend(colorize_cpp_code(code_part))
        colored_segments.append((COMMENT_COLOR, comment_part))
        return colored_segments

    # Split by whitespace but keep track of positions
    tokens = line.split()
    current_pos = 0

    for token in tokens:
        # Find the token's position in the line
        token_start = line.find(token, current_pos)

        # Add whitespace before token
        if token_start > current_pos:
            colored_segments.append((TEXT_COLOR, line[current_pos:token_start]))

        # Colorize the token
        if token in CPP_KEYWORDS:
            colored_segments.append((KEYWORD_COLOR, token))
        elif token.startswith('"') and token.endswith('"'):
            colored_segments.append((STRING_COLOR, token))
        elif token.isdigit():
            colored_segments.append((NUMBER_COLOR, token))
        elif '::' in token:
            # Handle namespace::function
            parts = token.split('::')
            for i, part in enumerate(parts):
                if i > 0:
                    colored_segments.append((OPERATOR_COLOR, '::'))
                colored_segments.append((TYPE_COLOR, part))
        elif token.startswith('~'):
            # Destructor
            colored_segments.append((OPERATOR_COLOR, '~'))
            colored_segments.append((FUNCTION_COLOR, token[1:]))
        elif any(op in token for op in ['(', ')', '{', '}', '[', ']', '<', '>', ';']):
            # Contains operators
            colored_segments.append((TEXT_COLOR, token))
        else:
            # Default color
            colored_segments.append((TEXT_COLOR, token))

        current_pos = token_start + len(token)

    # Add any remaining whitespace
    if current_pos < len(line):
        colored_segments.append((TEXT_COLOR, line[current_pos:]))

    return colored_segments if colored_segments else [(TEXT_COLOR, line)]

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

def create_answer_image(post_num, answer_text):
    """Create beautiful answer image with syntax highlighting"""

    # Load fonts
    font_normal = load_font(24)  # Slightly larger
    font_bold = load_bold_font(28)
    font_code = load_font(22)

    # Split into lines
    raw_lines = answer_text.split('\n')

    # Parse and format lines
    formatted_lines = []
    in_code_block = False

    for line in raw_lines:
        # Empty lines
        if not line.strip():
            formatted_lines.append([])
            continue

        # Detect code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue  # Skip the ``` markers

        # Headings (bold white)
        if line.strip().startswith('**') and line.strip().endswith('**'):
            text = line.strip().strip('*').strip()
            formatted_lines.append([(HEADING_COLOR, text, font_bold)])
            continue

        # Code lines or inside code block
        if in_code_block or any(kw in line for kw in ['std::', 'class ', 'void ', 'int ', 'virtual ', 'const ', 'template', 'return ', 'delete ', 'new ', '::', '()', '->', 'constexpr']):
            # Apply syntax highlighting
            colored_segments = colorize_cpp_code(line)
            formatted_line = [(color, text, font_code) for color, text in colored_segments]
            formatted_lines.append(formatted_line)
        else:
            # Regular text
            formatted_lines.append([(TEXT_COLOR, line, font_normal)])

    # Calculate image height
    draw_temp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    total_height = PADDING

    for line_segments in formatted_lines:
        if not line_segments:
            total_height += 15  # Empty line
        else:
            # Get height from first segment's font
            _, _, font = line_segments[0]
            bbox = draw_temp.textbbox((0, 0), 'Test', font=font)
            total_height += (bbox[3] - bbox[1]) + LINE_SPACING

    total_height += PADDING

    # Create image
    img = Image.new('RGB', (IMAGE_WIDTH, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw text
    y = PADDING

    for line_segments in formatted_lines:
        if not line_segments:
            y += 15  # Empty line
            continue

        x = PADDING

        # Draw each colored segment
        for color, text, font in line_segments:
            if text:
                draw.text((x, y), text, font=font, fill=color)
                bbox = draw.textbbox((0, 0), text, font=font)
                x += (bbox[2] - bbox[0])

        # Move to next line
        _, _, font = line_segments[0]
        bbox = draw.textbbox((0, 0), 'Test', font=font)
        y += (bbox[3] - bbox[1]) + LINE_SPACING

    return img

def main():
    print("=" * 80)
    print("Regenerating ALL 45 answer images with beautiful IDE-style highlighting")
    print("Matching the style of question images")
    print("=" * 80)
    print()

    # Extract answers
    print("Step 1: Extracting answers from master document...")
    print("-" * 80)
    answers = extract_answers_from_master()
    print(f"✓ Extracted {len(answers)} answers")
    print()

    # Generate images
    print("Step 2: Generating images with syntax highlighting...")
    print("-" * 80)

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
    print("=" * 80)
    print(f"✅ Successfully regenerated {len(answers)}/45 answer images!")
    print(f"   Style: IDE-like syntax highlighting (matching question images)")
    print(f"   Width: {IMAGE_WIDTH}px")
    print("=" * 80)

if __name__ == '__main__':
    main()
