import os
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw, ImageFont

img_dir = r"C:\Users\MAULIINGLE\.gemini\antigravity\scratch\kaybee_global_3d\static\images"

def make_custom_product_image(output_filename, title_text, color_accent):
    canvas = Image.new('RGB', (800, 600), color='#0F0C1B')
    draw = ImageDraw.Draw(canvas)

    # Draw luxury radial gradient
    for r in range(380, 0, -2):
        factor = r / 380.0
        color = (
            int(color_accent[0] * (1 - factor) + 15 * factor),
            int(color_accent[1] * (1 - factor) + 12 * factor),
            int(color_accent[2] * (1 - factor) + 27 * factor)
        )
        draw.ellipse([400 - r, 300 - r, 400 + r, 300 + r], fill=color)

    # Gold Borders
    draw.rectangle([12, 12, 788, 588], outline='#E5CB9E', width=4)

    # Try fonts
    try:
        font_title = ImageFont.truetype("arial.ttf", 34)
        font_brand = ImageFont.truetype("arial.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 18)
    except:
        font_title = font_brand = font_sub = ImageFont.load_default()

    # KAYBEE GLOBAL BRAND BADGE
    draw.ellipse([350, 90, 450, 190], outline='#E5CB9E', width=3, fill='#1A152E')
    draw.text((400, 140), "KBG", fill='#E5CB9E', font=font_brand, anchor='mm')

    # TITLE & PRODUCT SPECIFICATIONS
    draw.text((400, 260), title_text.upper(), fill='#FFFFFF', font=font_title, anchor='mm')
    draw.text((400, 320), "PREMIUM INDIAN EXPORT PRODUCE", fill='#E5CB9E', font=font_sub, anchor='mm')
    draw.text((400, 360), "APEDA & PHYTOSANITARY CERTIFIED", fill='#48BB78', font=font_sub, anchor='mm')

    # BOTTOM BADGE
    draw.rectangle([180, 440, 620, 495], fill='#1A152E', outline='#E5CB9E', width=2)
    draw.text((400, 4675//10), "100% FARM FRESH DIRECT COLD-CHAIN", fill='#E5CB9E', font=font_sub, anchor='mm')

    out_path = os.path.join(img_dir, output_filename)
    canvas.save(out_path, quality=95)
    print(f"Generated custom product image: {output_filename}")

def main():
    items = [
        ("kaybee_drumsticks.jpg", "Moringa Drumsticks (Pods)", (56, 161, 105)),
        ("kaybee_potatoes_only.jpg", "Fresh Table Potatoes", (180, 140, 80)),
        ("kaybee_tomatoes_only.jpg", "Farm Fresh Red Tomatoes", (220, 50, 50)),
        ("kaybee_garlic_ginger_only.jpg", "Fresh Garlic & Ginger", (200, 200, 200)),
        ("kaybee_green_chillies.jpg", "G4 Export Green Chillies", (40, 180, 70)),
        ("kaybee_okra.jpg", "Fresh Okra (Lady Finger)", (50, 160, 60)),
        ("kaybee_brinjal.jpg", "Fresh Purple Brinjal (Eggplant)", (120, 40, 160)),
        ("kaybee_gourds_only.jpg", "Bottle & Bitter Gourds", (70, 170, 90)),
        ("kaybee_coriander_mint.jpg", "Fresh Coriander & Mint", (30, 160, 80)),
        ("kaybee_sharbati_only.jpg", "MP Sharbati Whole Wheat", (229, 203, 158)),
        ("kaybee_durum_only.jpg", "Lokwan & Durum Wheat", (210, 170, 100)),
        ("kaybee_atta_flour.jpg", "Fresh Wheat Atta & Suji", (230, 210, 170)),
    ]

    for filename, title, color in items:
        make_custom_product_image(filename, title, color)

if __name__ == "__main__":
    main()
