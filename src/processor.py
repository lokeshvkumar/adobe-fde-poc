import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

class ImageProcessor:
    def download_image(self, url):
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def overlay_text(self, image, text):
        """Adds campaign message with a semi-transparent text box."""
        draw = ImageDraw.Draw(image, "RGBA")
        width, height = image.size

        # Dynamic font size based on image width
        fontsize = int(width / 20)
        
        # Attempt to load a standard font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", fontsize)
        except IOError:
            font = ImageFont.load_default()

        # Text positioning (Bottom Center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) / 2
        y = height - (height * 0.15) # 15% from bottom

        # Draw semi-transparent background box for readability
        padding = 20
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(0, 0, 0, 128) # Black with 50% opacity
        )

        # Draw White Text
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        return image