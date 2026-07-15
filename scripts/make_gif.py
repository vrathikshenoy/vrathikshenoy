#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

# Set output path relative to script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_GIF = os.path.join(REPO_DIR, "assets", "boot.gif")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def render_terminal_frame(lines, font_path, font_size=13, width=420, height=260):
    bg_color = (13, 17, 23)      # #0D1117
    text_color = (201, 209, 217)  # #C9D1D9
    blue_color = (88, 166, 255)  # #58A6FF
    cyan_color = (57, 208, 255)  # #39D0FF
    green_color = (63, 185, 80)  # #3FB950
    purple_color = (163, 113, 247) # #A371F7
    
    # Initialize font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    image = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Determine line height
    if hasattr(font, "getbbox"):
        l, t, r, b = font.getbbox("M")
        char_h = b - t + 6
    else:
        char_h = 18
        
    margin_x = 20
    margin_y = 20
    
    for i, line in enumerate(lines):
        y_pos = margin_y + i * char_h
        
        # Parse tokens for syntax coloring
        # We can implement basic token styling:
        # If line contains "[", it's a progress bar. Color it blue/cyan.
        # If line has "✓", color checkmark green.
        # If line has "ACCESS GRANTED", color success green.
        # If line starts with "AI.OS", color purple/cyan.
        
        if line.startswith("AI.OS"):
            # Header
            draw.text((margin_x, y_pos), line, font=font, fill=cyan_color)
        elif "ACCESS GRANTED" in line:
            draw.text((margin_x, y_pos), line, font=font, fill=green_color)
        else:
            # Multi-part line drawing for coloring checkmarks and progress bars
            parts = []
            current_x = margin_x
            
            # Simple splitter to style checkmarks and brackets
            if "✓" in line:
                idx = line.index("✓")
                left_part = line[:idx]
                draw.text((current_x, y_pos), left_part, font=font, fill=text_color)
                # Compute width of left part to draw the green checkmark
                if hasattr(font, "getbbox"):
                    w = font.getbbox(left_part)[2] - font.getbbox(left_part)[0] if left_part else 0
                else:
                    w = font.getsize(left_part)[0] if left_part else 0
                draw.text((current_x + w, y_pos), "✓", font=font, fill=green_color)
            elif "[" in line and "]" in line:
                # Progress bar line: Loading Kernel... [████░░░░░░░░] 30%
                idx_start = line.index("[")
                idx_end = line.index("]") + 1
                
                left_part = line[:idx_start]
                bar_part = line[idx_start:idx_end]
                right_part = line[idx_end:]
                
                draw.text((current_x, y_pos), left_part, font=font, fill=text_color)
                w_left = font.getbbox(left_part)[2] - font.getbbox(left_part)[0] if hasattr(font, "getbbox") else font.getsize(left_part)[0]
                
                # Draw bar in blue
                draw.text((current_x + w_left, y_pos), bar_part, font=font, fill=blue_color)
                w_bar = font.getbbox(bar_part)[2] - font.getbbox(bar_part)[0] if hasattr(font, "getbbox") else font.getsize(bar_part)[0]
                
                # Draw right part (percentage) in cyan
                draw.text((current_x + w_left + w_bar, y_pos), right_part, font=font, fill=cyan_color)
            else:
                # Default draw
                draw.text((margin_x, y_pos), line, font=font, fill=text_color)
                
    return image

def main():
    print("Generating Boot Animation GIF frames...")
    os.makedirs(os.path.dirname(OUTPUT_GIF), exist_ok=True)
    
    # We define the cumulative terminal output for each frame
    frames_data = [
        # Frame 0: Start
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            ">"
        ],
        # Frame 1: Kernel 30%
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████░░░░░░░░] 33%",
            ">"
        ],
        # Frame 2: Kernel 100%
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████████████] 100% ✓",
            ">"
        ],
        # Frame 3: CUDA 66%
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████░░░░] 66%",
            ">"
        ],
        # Frame 4: CUDA 100%
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            ">"
        ],
        # Frame 5: Neural Engine
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            ">"
        ],
        # Frame 6: Load Modules header
        [
            "AI.OS v2.4 // Bootloader",
            "Initializing system...",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            ">"
        ],
        # Frame 7: Module 1
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            ">"
        ],
        # Frame 8: Module 2
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            ">"
        ],
        # Frame 9: Module 3
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            ">"
        ],
        # Frame 10: Module 4
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            ">"
        ],
        # Frame 11: Module 5
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            "  Startup Stack        ✓",
            ">"
        ],
        # Frame 12: Rendering User
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            "  Startup Stack        ✓",
            "",
            "Rendering user dashboard...",
            ">"
        ],
        # Frame 13: Access Granted + Cursor On
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            "  Startup Stack        ✓",
            "",
            "Rendering user dashboard...",
            "ACCESS GRANTED",
            "> █"
        ],
        # Frame 14: Access Granted + Cursor Off
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            "  Startup Stack        ✓",
            "",
            "Rendering user dashboard...",
            "ACCESS GRANTED",
            ">  "
        ],
        # Frame 15: Access Granted + Cursor On
        [
            "AI.OS v2.4 // Bootloader",
            "Loading Kernel...      [████████████] 100% ✓",
            "Loading CUDA modules... [████████████] 100% ✓",
            "Neural Engine...       [████████████] 100% ✓",
            "",
            "Loading sub-modules...",
            "  Computer Vision      ✓",
            "  Generative AI        ✓",
            "  Diffusion Models     ✓",
            "  Research Mode        ✓",
            "  Startup Stack        ✓",
            "",
            "Rendering user dashboard...",
            "ACCESS GRANTED",
            "> █"
        ]
    ]
    
    # Render all frames
    images = []
    for i, frame_lines in enumerate(frames_data):
        img = render_terminal_frame(frame_lines, FONT_PATH, font_size=10, width=420, height=270)
        images.append(img)
        
    # Frame durations in milliseconds
    durations = [
        600,  # F0: Start
        350,  # F1: Kernel 33%
        350,  # F2: Kernel 100%
        350,  # F3: CUDA 66%
        350,  # F4: CUDA 100%
        350,  # F5: Neural Engine
        350,  # F6: Load Modules header
        200,  # F7: CV
        200,  # F8: GenAI
        200,  # F9: Diffusion
        200,  # F10: Research
        200,  # F11: Startup
        600,  # F12: Rendering User
        1500, # F13: Access Granted, Cursor On
        500,  # F14: Cursor Off
        500   # F15: Cursor On
    ]
    
    # Save GIF
    images[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0
    )
    
    print(f"Boot sequence GIF saved to: {OUTPUT_GIF}")

if __name__ == "__main__":
    main()
