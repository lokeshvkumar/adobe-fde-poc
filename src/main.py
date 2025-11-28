import json
import os
import argparse
from dotenv import load_dotenv
from PIL import Image
from src.models import CampaignBrief
from src.generator import ImageGenerator
from src.processor import ImageProcessor

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Adobe FDE Creative Pipeline")
    parser.add_argument("--brief", required=True, help="Path to campaign brief JSON")
    args = parser.parse_args()

    # 1. Ingestion & Validation
    try:
        with open(args.brief, 'r') as f:
            data = json.load(f)
        brief = CampaignBrief(**data)
        print(f"✅ Loaded Campaign: {brief.campaign_name}")
    except Exception as e:
        print(f"❌ Error parsing brief: {e}")
        return

    # Initialize Services
    generator = ImageGenerator()
    processor = ImageProcessor()

    # 2. Processing Loop
    for product in brief.products:
        print(f"\n📦 Processing Product: {product.product_name}")
        
        # Create Output Directory
        product_dir = os.path.join("output", product.product_name)
        os.makedirs(product_dir, exist_ok=True)

        for ratio in brief.aspect_ratios:
            filename = f"{ratio.replace(':','-')}.png"
            output_path = os.path.join(product_dir, filename)
            
            # 3. Check for existing local asset (Reuse strategy)
            local_asset_path = os.path.join("assets", product.product_name, filename)
            
            img_obj = None

            if os.path.exists(local_asset_path):
                print(f"   Found local asset for {ratio}. Using it.")
                img_obj = Image.open(local_asset_path)
            else:
                # 4. Generate if missing
                print(f"   Generating new asset for {ratio}...")
                image_url = generator.generate_asset(
                    product.visual_description, 
                    brief.region, 
                    brief.target_audience,
                    ratio
                )
                if image_url:
                    img_obj = processor.download_image(image_url)

            # 5. Apply Post-Processing (Text Overlay)
            if img_obj:
                print(f"   Applying campaign message: '{brief.campaign_message}'")
                final_img = processor.overlay_text(img_obj, brief.campaign_message)
                
                # Save
                final_img.save(output_path)
                print(f"   ✅ Saved to {output_path}")

if __name__ == "__main__":
    main()