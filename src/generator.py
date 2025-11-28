import os
from openai import OpenAI

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_asset(self, product_desc, region, audience, aspect_ratio):
        """Generates an image using DALL-E 3 based on aspect ratio."""
        
        # DALL-E 3 specific resolution mapping
        size_map = {
            "1:1": "1024x1024",
            "16:9": "1792x1024",
            "9:16": "1024x1792"
        }
        
        # Fallback to square if ratio is unknown
        size = size_map.get(aspect_ratio, "1024x1024")

        prompt = (
            f"Professional advertising product photography of {product_desc}. "
            f"Background context: {region}, appealing to {audience}. "
            f"Style: Modern, eye-catching, brand-focused with product prominently displayed."
            f"High quality, commercial lighting, photorealistic."
        )

        print(f"   >>> Calling OpenAI DALL-E 3 ({size}) & prompt is: ({prompt})...")
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1,
            )
            return response.data[0].url
        except Exception as e:
            print(f"   !!! Error generating image: {e}")
            return None