#!/usr/bin/env python3
import sys
import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Set output path relative to script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
SOURCE_IMG = "/home/vrathik/Downloads/46716333.jpg"
OUTPUT_GIF = os.path.join(REPO_DIR, "assets", "portrait.gif")
OUTPUT_STATIC = os.path.join(REPO_DIR, "assets", "profile.png")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

def preprocess_image(img_path, target_width=75):
    # Load and crop to square
    img = Image.open(img_path)
    w, h = img.size
    min_dim = min(w, h)
    
    # Center crop
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    img_cropped = img.crop((left, top, left + min_dim, top + min_dim))
    
    # Character aspect ratio correction (width of character is ~0.6 of height)
    char_aspect = 0.55
    target_height = int(target_width / char_aspect)
    
    # Resize to the character grid size
    img_resized = img_cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)
    return img_resized

def compute_ascii_grid(pil_img):
    # Convert PIL Image to numpy array (RGB)
    img_np = np.array(pil_img)
    # Grayscale
    gray = np.array(pil_img.convert("L"))
    
    # Apply contrast boosting (histogram equalization or simple stretch)
    p_min, p_max = np.percentile(gray, (5, 95))
    gray_stretched = np.clip((gray - p_min) * (255.0 / (p_max - p_min)), 0, 255).astype(np.uint8)
    
    # Calculate gradients using Sobel filters to detect edges and directions
    # Import cv2 dynamically inside function to keep dependencies isolated if needed
    import cv2
    sobelx = cv2.Sobel(gray_stretched, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray_stretched, cv2.CV_64F, 0, 1, ksize=3)
    
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    angle = np.arctan2(sobely, sobelx) * (180.0 / np.pi)
    angle[angle < 0] += 180
    
    # Character palettes
    # Intensity-based palette (dark background, so high brightness = denser character)
    # Background is #0D1117 (dark), text is #58A6FF (bright blue)
    intensity_chars = " .:-=+*#%@"
    
    height, width = gray_stretched.shape
    ascii_grid = []
    magnitudes_grid = []
    
    for y in range(height):
        row_chars = []
        row_mags = []
        for x in range(width):
            mag = magnitude[y, x]
            ang = angle[y, x]
            val = gray_stretched[y, x]
            
            # Save magnitudes for thresholding later
            row_mags.append(mag)
            
            # If there's a strong edge, use directional characters
            if mag > 80:
                if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                    char = "|"  # Horizontal edge -> Vertical stroke (perpendicular to gradient direction)
                elif 22.5 <= ang < 67.5:
                    char = "/"  # Diagonal stroke
                elif 67.5 <= ang < 112.5:
                    char = "-"  # Vertical edge -> Horizontal stroke
                else:
                    char = "\\"  # Diagonal stroke
            else:
                # Shading based on intensity
                char_idx = int(val / 256.0 * len(intensity_chars))
                char = intensity_chars[char_idx]
                
            row_chars.append(char)
        ascii_grid.append(row_chars)
        magnitudes_grid.append(row_mags)
        
    return ascii_grid, np.array(magnitudes_grid), gray_stretched

def render_ascii_to_image(ascii_grid, font_path, font_size=12, text_color=(88, 166, 255), bg_color=(13, 17, 23)):
    # Initialize font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Get character sizes
    # We use a dummy string of 100 characters to compute average width/height
    dummy_text = "M" * 100
    if hasattr(font, "getbbox"):
        l, t, r, b = font.getbbox("M")
        char_w = r - l
        char_h = b - t + 3 # add some line spacing
    else:
        char_w, char_h = font.getsize("M")
        char_h += 3
        
    grid_h = len(ascii_grid)
    grid_w = len(ascii_grid[0])
    
    img_w = grid_w * char_w + 20
    img_h = grid_h * char_h + 20
    
    # Create background image
    image = Image.new("RGB", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Draw text lines
    for y in range(grid_h):
        line_str = "".join(ascii_grid[y])
        draw.text((10, 10 + y * char_h), line_str, font=font, fill=text_color)
        
    return image

def generate_progressive_frames(ascii_grid, magnitudes, gray_img):
    frames = []
    h, w = gray_img.shape
    
    # Define 10 stages of reveal
    for stage in range(11):
        frame_grid = []
        for y in range(h):
            row = []
            for x in range(w):
                mag = magnitudes[y, x]
                val = gray_img[y, x]
                char = ascii_grid[y][x]
                
                # Check mapping for each stage
                if stage == 0:
                    row.append(" ")
                elif stage == 1:
                    if mag > 180 and char in ["|", "/", "-", "\\"]:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage == 2:
                    if mag > 120 and char in ["|", "/", "-", "\\"]:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage == 3:
                    if char in ["|", "/", "-", "\\"]:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage == 4:
                    if char in ["|", "/", "-", "\\"] or val < 60:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage == 5:
                    if char in ["|", "/", "-", "\\"] or val < 120:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage == 6:
                    if char in ["|", "/", "-", "\\"] or val < 180:
                        row.append(char)
                    else:
                        row.append(" ")
                elif stage >= 7:
                    row.append(char)
            frame_grid.append(row)
            
        # Terminal status overlay
        if stage in [0, 1, 2]:
            frame_grid[-1][:8] = list("> INIT  ")
        elif stage in [3, 4, 5]:
            frame_grid[-1][:8] = list("> LOAD  ")
        elif stage in [6, 7]:
            frame_grid[-1][:8] = list("> RNDR  ")
        elif stage == 8:
            frame_grid[-1][:12] = list("> READY    █")
        elif stage in [9, 10]:
            if stage == 9:
                frame_grid[-1][:12] = list("> READY    █")
            else:
                frame_grid[-1][:12] = list("> READY     ")
                
        frames.append(frame_grid)
        
    return frames

def main():
    print("Initializing ASCII Portrait Generation Pipeline...")
    os.makedirs(os.path.dirname(OUTPUT_GIF), exist_ok=True)
    
    # Preprocess (target width 80 characters for profile README alignment)
    img_resized = preprocess_image(SOURCE_IMG, target_width=80)
    
    # Compute full grid
    ascii_grid, magnitudes, gray_img = compute_ascii_grid(img_resized)
    
    # Generate progressive frames
    print("Generating progressive frame buffers...")
    frame_grids = generate_progressive_frames(ascii_grid, magnitudes, gray_img)
    
    # Render to images
    print("Rendering text grids to image frames...")
    rendered_frames = []
    for i, grid in enumerate(frame_grids):
        text_color = (88, 166, 255) if i < 8 else (57, 208, 255)
        img_frame = render_ascii_to_image(grid, FONT_PATH, font_size=10, text_color=text_color)
        rendered_frames.append(img_frame)
        
    # Save static profile image (the final frame)
    rendered_frames[-2].save(OUTPUT_STATIC)
    print(f"Static profile image saved to: {OUTPUT_STATIC}")
    
    # Save animated GIF
    durations = [
        600,  # Empty prompt
        150,  # Edge outline 1
        150,  # Edge outline 2
        150,  # Edge outline 3
        150,  # Shading 1
        150,  # Shading 2
        150,  # Shading 3
        150,  # Full 1
        1000, # Ready with cursor
        500,  # Blink off
        500   # Blink on
    ]
    
    rendered_frames[0].save(
        OUTPUT_GIF,
        save_all=True,
        append_images=rendered_frames[1:],
        duration=durations,
        loop=0
    )
    print(f"Progressive ASCII portrait GIF saved to: {OUTPUT_GIF}")

if __name__ == "__main__":
    main()
