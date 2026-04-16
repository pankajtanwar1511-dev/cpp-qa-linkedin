#!/usr/bin/env python3
"""
Regenerate all 45 answer images using Pygments for professional syntax highlighting
Matching the exact style of question images
"""

import re
import os
from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import CppLexer
from pygments.token import Token
from pygments.formatters import TerminalFormatter

# VS Code Dark+ color scheme (matching question images)
BG_COLOR = '#2e2e2e'
BLOCK_BG_COLOR = '#252525'  # Slightly darker for block backgrounds
TEXT_COLOR = '#d4d4d4'
HEADING_COLOR = '#ffffff'

# Pygments token colors (VS Code Dark+ theme)
TOKEN_COLORS = {
    Token.Keyword: '#569cd6',           # Blue - class, int, void, return, etc.
    Token.Keyword.Type: '#4ec9b0',      # Cyan - custom types
    Token.Keyword.Namespace: '#4ec9b0', # Cyan - namespace
    Token.Name.Class: '#4ec9b0',        # Cyan - class names
    Token.Name.Function: '#dcdcaa',     # Yellow - function names
    Token.Name.Namespace: '#4ec9b0',    # Cyan - std
    Token.String: '#ce9178',            # Orange - strings
    Token.Number: '#b5cea8',            # Light green - numbers
    Token.Operator: '#d4d4d4',          # White - operators
    Token.Punctuation: '#d4d4d4',       # White - punctuation
    Token.Comment: '#6a9955',           # Green - comments
    Token.Name: '#9cdcfe',              # Light blue - variables
    Token.Literal: '#b5cea8',           # Light green - literals
}

IMAGE_WIDTH = 1400
PADDING = 50
LINE_SPACING = 10
BLOCK_PADDING = 25  # Extra padding inside blocks
BLOCK_SPACING = 20  # Space between blocks

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

def get_token_color(token_type):
    """Get color for a Pygments token"""
    # Find the most specific color match
    while token_type:
        if token_type in TOKEN_COLORS:
            return TOKEN_COLORS[token_type]
        token_type = token_type.parent
    return TEXT_COLOR

def highlight_cpp_code(code):
    """Use Pygments to highlight C++ code and return colored segments"""
    lexer = CppLexer()
    tokens = list(lexer.get_tokens(code))

    colored_segments = []
    for token_type, token_text in tokens:
        # Keep ALL tokens including whitespace to preserve spacing
        color = get_token_color(token_type)
        colored_segments.append((color, token_text))

    return colored_segments

def is_code_line(line):
    """Detect if a line is C++ code"""
    code_indicators = [
        'std::', 'class ', 'struct ', 'template', 'typename', 'constexpr',
        'virtual ', 'void ', 'int ', 'auto ', 'bool ', 'char ',
        'return ', 'new ', 'delete ', '::', '()', '->', '{}', '[]',
        '#include', 'namespace', 'using ', 'public:', 'private:', 'protected:',
        '~', ' = ', ' == ', ' != ', ' < ', ' > '
    ]
    return any(indicator in line for indicator in code_indicators)

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

def parse_line(line, font_normal, font_bold, font_code):
    """Parse a line and return colored segments with fonts"""

    # Empty line
    if not line.strip():
        return []

    # Heading (bold white)
    if line.strip().startswith('**') and line.strip().endswith('**'):
        text = line.strip().strip('*').strip()
        return [(HEADING_COLOR, text, font_bold)]

    # Code line - use Pygments
    if is_code_line(line):
        segments = highlight_cpp_code(line)
        return [(color, text, font_code) for color, text in segments]

    # Regular text
    return [(TEXT_COLOR, line, font_normal)]

def create_answer_image(post_num, answer_text):
    """Create answer image with Pygments syntax highlighting and visual blocks"""

    # Load fonts
    font_normal = load_font(24)
    font_bold = load_bold_font(28)
    font_code = load_font(22)

    # Split into lines
    raw_lines = answer_text.split('\n')

    # Parse all lines and organize into blocks
    blocks = []  # List of (heading, lines) tuples
    current_heading = None
    current_lines = []
    in_code_block = False

    for line in raw_lines:
        # Detect code block markers
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Heading (starts a new block)
        if line.strip().startswith('**') and line.strip().endswith('**'):
            # Save previous block
            if current_heading or current_lines:
                blocks.append((current_heading, current_lines))

            # Start new block
            current_heading = line.strip().strip('*').strip()
            current_lines = []
            continue

        # Empty line
        if not line.strip():
            current_lines.append([])
            continue

        # Inside code block - use Pygments
        if in_code_block:
            segments = highlight_cpp_code(line)
            current_lines.append([(color, text, font_code) for color, text in segments])
            continue

        # C++ code line (but outside code block) - use Pygments carefully
        if is_code_line(line) and ('::' in line or 'virtual' in line or 'constexpr' in line):
            segments = highlight_cpp_code(line)
            current_lines.append([(color, text, font_code) for color, text in segments])
        else:
            # Regular text - don't use Pygments, keep as-is
            current_lines.append([(TEXT_COLOR, line, font_normal)])

    # Save last block
    if current_heading or current_lines:
        blocks.append((current_heading, current_lines))

    # Calculate heights for each block
    draw_temp = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    block_heights = []

    for heading, lines in blocks:
        block_height = BLOCK_PADDING  # Top padding

        # Heading height
        if heading:
            bbox = draw_temp.textbbox((0, 0), heading, font=font_bold)
            block_height += (bbox[3] - bbox[1]) + LINE_SPACING * 2

        # Lines height
        for line_segments in lines:
            if not line_segments:
                block_height += 15  # Empty line
            else:
                _, _, font = line_segments[0]
                bbox = draw_temp.textbbox((0, 0), 'Test', font=font)
                block_height += (bbox[3] - bbox[1]) + LINE_SPACING

        block_height += BLOCK_PADDING  # Bottom padding
        block_heights.append(block_height)

    # Calculate total image height
    total_height = PADDING
    total_height += sum(block_heights)
    total_height += BLOCK_SPACING * (len(blocks) - 1)  # Spacing between blocks
    total_height += PADDING

    # Create image
    img = Image.new('RGB', (IMAGE_WIDTH, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Draw blocks
    y = PADDING

    for (heading, lines), block_height in zip(blocks, block_heights):
        # Draw block background (rounded rectangle would be nice, but let's use simple rect)
        block_x1 = PADDING
        block_y1 = y
        block_x2 = IMAGE_WIDTH - PADDING
        block_y2 = y + block_height

        draw.rectangle([block_x1, block_y1, block_x2, block_y2], fill=BLOCK_BG_COLOR)

        # Draw heading
        y_content = y + BLOCK_PADDING
        if heading:
            draw.text((PADDING + BLOCK_PADDING, y_content), heading, font=font_bold, fill=HEADING_COLOR)
            bbox = draw.textbbox((0, 0), heading, font=font_bold)
            y_content += (bbox[3] - bbox[1]) + LINE_SPACING * 2

        # Draw lines
        for line_segments in lines:
            if not line_segments:
                y_content += 15  # Empty line
                continue

            x = PADDING + BLOCK_PADDING

            # Draw each colored segment
            for color, text, font in line_segments:
                if text:
                    draw.text((x, y_content), text, font=font, fill=color)
                    bbox = draw.textbbox((0, 0), text, font=font)
                    x += (bbox[2] - bbox[0])

            # Move to next line
            _, _, font = line_segments[0]
            bbox = draw.textbbox((0, 0), 'Test', font=font)
            y_content += (bbox[3] - bbox[1]) + LINE_SPACING

        # Move to next block
        y = block_y2 + BLOCK_SPACING

    return img

def main():
    print("=" * 80)
    print("Regenerating ALL 45 answer images with Pygments syntax highlighting")
    print("Professional IDE-quality highlighting matching question images")
    print("=" * 80)
    print()

    # Extract answers
    print("Step 1: Extracting answers from master document...")
    print("-" * 80)
    answers = extract_answers_from_master()
    print(f"✓ Extracted {len(answers)} answers")
    print()

    # Generate images
    print("Step 2: Generating images with Pygments highlighter...")
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
            import traceback
            traceback.print_exc()

    print()
    print("=" * 80)
    print(f"✅ Successfully regenerated {len(answers)}/45 answer images!")
    print(f"   Style: Pygments C++ lexer (VS Code Dark+ theme)")
    print(f"   Width: {IMAGE_WIDTH}px")
    print("=" * 80)

if __name__ == '__main__':
    main()
