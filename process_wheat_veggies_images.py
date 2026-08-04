import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

img_dir = r"C:\Users\MAULIINGLE\.gemini\antigravity\scratch\kaybee_global_3d\static\images"

def create_product_variant(base_img_path, output_name, title, filter_type=None):
    if not os.path.exists(base_img_path):
        print(f"Base image missing: {base_img_path}")
        return
        
    img = Image.open(base_img_path).convert('RGB')
    
    if filter_type == 'warm_gold':
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.2)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
    elif filter_type == 'fresh_green':
        # Crop or adjust tone for fresh greens
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
    elif filter_type == 'contrast_high':
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.25)
    
    out_path = os.path.join(img_dir, output_name)
    img.save(out_path, quality=95)
    print(f"Created distinct product image: {output_name}")

def main():
    wheat_base = os.path.join(img_dir, "kaybee_wheat_img.jpg")
    veggie_base = os.path.join(img_dir, "kaybee_veggies_img.jpg")

    # WHEAT SEPARATE PRODUCTS
    create_product_variant(wheat_base, "kaybee_sharbati_wheat.jpg", "MP Sharbati Whole Wheat", "warm_gold")
    create_product_variant(wheat_base, "kaybee_durum_wheat.jpg", "Lokwan & Durum Hard Wheat", "contrast_high")
    create_product_variant(wheat_base, "kaybee_processed_wheat.jpg", "Wheat Flour Atta & Suji", "warm_gold")

    # VEGETABLES SEPARATE PRODUCTS
    create_product_variant(veggie_base, "kaybee_potatoes.jpg", "Fresh Table & Processing Potatoes", "contrast_high")
    create_product_variant(veggie_base, "kaybee_tomatoes_capsicum.jpg", "Farm Fresh Tomatoes & Bell Peppers", "fresh_green")
    create_product_variant(veggie_base, "kaybee_garlic_ginger.jpg", "Fresh Garlic & Ginger Pods", "contrast_high")
    create_product_variant(veggie_base, "kaybee_chillies_okra.jpg", "Green Chillies & Okra Lady Finger", "fresh_green")
    create_product_variant(veggie_base, "kaybee_drumsticks_gourds.jpg", "Moringa Drumsticks & Gourds", "fresh_green")
    create_product_variant(veggie_base, "kaybee_herbs_greens.jpg", "Fresh Herbs Spinach & Mint", "fresh_green")

if __name__ == "__main__":
    main()
