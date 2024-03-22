# SEP
# Serenity Emoji Preview
# written with the help of Google Gemini
from PIL import Image, ImageFont, ImageDraw
import os
import sys

recursive = 0
total_width = 0

def scale_and_arrange_images(folder_path, scale_factor=30, font_size=20, shadowOffset=2, subcall=0, seperatingLine=5, images=[], filenames=[]):
  global total_width
  """
  Scales up PNG images in a folder, arranges them horizontally, and saves a combined image.

  Args:
    folder_path: Path to the folder containing PNG images.
    scale_factor: Factor to scale each image by.
    font_size: Size of the font used to display filenames.
  """
  font = ImageFont.truetype("arial.ttf", font_size)

  # Load and resize images
  for filename in os.listdir(folder_path):
    current_path = os.path.join(folder_path, filename)
    if (os.path.isdir(current_path) and recursive):
      scale_and_arrange_images(current_path, scale_factor, font_size, shadowOffset, 1, seperatingLine, images, filenames)  # Recursive call
    else:
      if filename.endswith(".png"):
        if (filename != "combined.png"):
          image_path = os.path.join(folder_path, filename)
          img = Image.open(image_path)
          width, height = img.size
          resized_width = int(width * scale_factor)
          resized_height = int(height * scale_factor)
          resized_img = img.resize((resized_width, resized_height))
          images.append(resized_img)
          filename = os.path.splitext(filename)[0]
          filenames.append(filename)
          total_width += resized_width + seperatingLine
          print(image_path + "- " + str(total_width))
  
  if (subcall == 0):
    # Create a new image to hold all resized images
    max_height = max(img.size[1] for img in images)
    combined_img = Image.new("RGBA", (total_width, max_height+font_size*2))
    x_offset = 0

    # Add images and filenames to the combined image
    for i, img in enumerate(images):
      combined_img.paste(img, (x_offset, 0))
      draw = ImageDraw.Draw(combined_img)
      text_width = draw.textlength(filenames[i], font=font)  # Capture just the width
      text_height = font_size  # Approximate height based on font size
      draw.text((x_offset+shadowOffset + (img.size[0] - text_width) // 2, max_height+shadowOffset), filenames[i], font=font, fill=(0, 0, 0))
      draw.text((x_offset + (img.size[0] - text_width) // 2, max_height), filenames[i], font=font, fill=(255, 255, 255))
      draw.line((x_offset,0, x_offset,max_height), fill=(0,0,255), width=seperatingLine)
      x_offset += img.size[0]

    # Save the combined image
    combined_image_path = os.path.join(folder_path, "combined.png")
    combined_img.save(combined_image_path)
    print(f"Combined image saved to: {combined_image_path}")

# Example usagetry:
try:
    folder_path = sys.argv[1]
    try:
       if (sys.argv[2] is not None):
          recursive = 1
    except IndexError:
          recursive = 0
    scale_and_arrange_images(folder_path)
except IndexError:
    print("No path provided!")
