import os
import requests
import time

products = [
    {"keywords": "moringa,vegetable", "filename": "kaybee_drumsticks.jpg"},
    {"keywords": "potatoes,farm", "filename": "kaybee_potatoes_only.jpg"},
    {"keywords": "tomatoes,fresh", "filename": "kaybee_tomatoes_only.jpg"},
    {"keywords": "garlic,ginger", "filename": "kaybee_garlic_ginger_only.jpg"},
    {"keywords": "chillies,green", "filename": "kaybee_green_chillies.jpg"},
    {"keywords": "okra,vegetable", "filename": "kaybee_okra.jpg"},
    {"keywords": "eggplant,vegetable", "filename": "kaybee_brinjal.jpg"},
    {"keywords": "gourd,vegetable", "filename": "kaybee_gourds_only.jpg"},
    {"keywords": "coriander,mint", "filename": "kaybee_coriander_mint.jpg"},
    {"keywords": "wheat,grains", "filename": "kaybee_sharbati_only.jpg"},
    {"keywords": "durum,wheat", "filename": "kaybee_durum_only.jpg"},
    {"keywords": "wheat,flour", "filename": "kaybee_atta_flour.jpg"},
    {"keywords": "basmati,rice", "filename": "kaybee_rice_img.jpg"}
]

output_dir = r"C:\Users\MAULIINGLE\.gemini\antigravity\scratch\kaybee_global_3d\static\images"

def download_image(keywords, filename):
    url = f"https://loremflickr.com/800/600/{keywords}"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        if response.status_code == 200:
            with open(os.path.join(output_dir, filename), 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"Error downloading {keywords}: {e}")
    return False

print("Starting free image download via LoremFlickr...")
for product in products:
    print(f"Downloading {product['filename']} for keywords: {product['keywords']}...")
    if download_image(product['keywords'], product['filename']):
        print(f"  [SUCCESS] Saved {product['filename']}")
    else:
        print(f"  [FAILED] Could not download image")
    time.sleep(1.5)

print("\nFinished downloading free images!")
