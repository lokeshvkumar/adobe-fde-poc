from typing import List
from pydantic import BaseModel, field_validator

class Product(BaseModel):
    product_name: str
    visual_description: str

class CampaignBrief(BaseModel):
    campaign_name: str
    products: List[Product]
    aspect_ratios: List[str]
    # ... existing fields ...
    campaign_message: str

    @field_validator('campaign_message')
    def check_prohibited_content(cls, v):
        prohibited_words = ["competitor", "illegal", "free", "guaranteed"]
        if any(word in v.lower() for word in prohibited_words):
            raise ValueError("Campaign message contains prohibited legal terms.")
        return v