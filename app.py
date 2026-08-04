import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

# Comprehensive Product Catalog with Dedicated Individual Product Entries & Images
PRODUCTS_DATABASE = [
    # --- 1. FRESH ONIONS ---
    {
        "id": "onions-red",
        "category": "onions",
        "category_label": "Fresh Onions",
        "name": "Export Grade Red Onions",
        "tagline": "Rich color, pungent flavor & long shelf life",
        "description": "Kaybee Global exports premium Indian Red Onions sourced directly from leading agricultural belts. Renowned for rich pungent flavor, uniform grading, and exceptional storage capability.",
        "sizes": ["Small (25-40 mm)", "Medium (40-60 mm)", "Large (60-80 mm)", "Jumbo (80 mm+)"],
        "packaging": ["5 kg Mesh Bags", "10 kg Mesh Bags", "20 kg Mesh Bags", "25 kg Mesh Bags", "50 kg Mesh Bags", "Jute Bags", "PP Bags", "Custom Private Label"],
        "origin": "Maharashtra, India",
        "moq": "12 Metric Tons (20ft FCL)",
        "shelf_life": "60 - 90 Days",
        "hs_code": "07031010",
        "image": "/static/images/kaybee_red_onions.jpg",
        "featured": True,
        "specifications": {
            "Pungency": "High Pungency",
            "Moisture": "< 14%",
            "Grading": "Strictly Sorted & Machine Graded",
            "Certifications": "Phytosanitary, APEDA, GlobalGAP"
        }
    },
    {
        "id": "onions-white",
        "category": "onions",
        "category_label": "Fresh Onions",
        "name": "Premium White Onions",
        "tagline": "Mild flavor, crisp texture & uniform size",
        "description": "Sourced from high-quality farms, our White Onions offer mild sweetness and crispness, perfect for dehydration, salads, and culinary processing.",
        "sizes": ["Medium (40-60 mm)", "Large (60-80 mm)"],
        "packaging": ["10 kg Mesh Bags", "25 kg Mesh Bags", "Customized Retail Packs"],
        "origin": "Gujarat / Maharashtra, India",
        "moq": "14 Metric Tons",
        "shelf_life": "45 - 60 Days",
        "hs_code": "07031010",
        "image": "/static/images/kaybee_white_onions.jpg",
        "featured": True,
        "specifications": {
            "Pungency": "Mild to Medium",
            "Dehydration Quality": "Ideal Dry Matter Content",
            "Certifications": "APEDA, FSSAI, Phytosanitary"
        }
    },
    {
        "id": "onions-pink",
        "category": "onions",
        "category_label": "Fresh Onions",
        "name": "Mild Sweet Pink Onions",
        "tagline": "Mildly sweet taste & high storage stability",
        "description": "Preferred for fresh consumption and export markets, our Pink Onions feature a delicate sweetness and durable storage profile.",
        "sizes": ["Medium (40-60 mm)", "Large (60-80 mm)"],
        "packaging": ["10 kg Mesh Bags", "20 kg Mesh Bags", "Jute Bags"],
        "origin": "Maharashtra, India",
        "moq": "12 Metric Tons",
        "shelf_life": "60 Days",
        "hs_code": "07031010",
        "image": "/static/images/kaybee_pink_onions.jpg",
        "featured": False,
        "specifications": {
            "Flavor": "Mildly Sweet",
            "Storage": "High Storage Stability"
        }
    },

    # --- 2. FRESH VEGETABLES (INDIVIDUAL SEPARATE ITEMS) ---
    {
        "id": "veg-drumsticks",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Moringa Drumsticks (Pods)",
        "tagline": "Peak harvest tender drumstick pods rich in nutrients",
        "description": "Export-grade fresh Moringa Pods (Drumsticks) harvested early morning, hydro-cooled, and packed in ventilated export cartons for international buyers.",
        "packaging": ["5 kg Master Cartons", "Vented Poly Bags"],
        "origin": "Tamil Nadu / Maharashtra, India",
        "moq": "2 Metric Tons (Air Freight)",
        "shelf_life": "14 Days",
        "hs_code": "07099990",
        "image": "/static/images/kaybee_drumsticks.jpg",
        "featured": True,
        "specifications": {
            "Pod Length": "35cm - 50cm Tender",
            "Handling": "Hydro-cooled Air Freight Standard",
            "Certifications": "Phytosanitary Certified"
        }
    },
    {
        "id": "veg-potatoes",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Fresh Table & Processing Potatoes",
        "tagline": "High dry-matter, firm skin & uniform sorting",
        "description": "Premium fresh table potatoes and processing potatoes (for chips and French fries) sourced from Punjab and Gujarat belts.",
        "sizes": ["45mm+", "50mm+", "55mm+"],
        "packaging": ["10 kg Mesh Bags", "25 kg Mesh Bags", "50 kg PP Bags"],
        "origin": "Punjab / Gujarat, India",
        "moq": "25 Metric Tons (40ft Reefer)",
        "shelf_life": "60 - 90 Days",
        "hs_code": "07019000",
        "image": "/static/images/kaybee_potatoes_only.jpg",
        "featured": True,
        "specifications": {
            "Sugar Content": "< 0.1% (Processing Grade)",
            "Skin": "Clean, Firm, Sprout-Free"
        }
    },
    {
        "id": "veg-tomatoes",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Farm Fresh Red Tomatoes",
        "tagline": "Firm red vine tomatoes for export supermarkets",
        "description": "Firm vine-ripened red tomatoes sorted by color and size, packaged in strong corrugated cartons for long sea transit.",
        "packaging": ["5 kg Corrugated Cartons", "Plastic Crates"],
        "origin": "Maharashtra / Karnataka, India",
        "moq": "5 Metric Tons",
        "shelf_life": "18 - 24 Days",
        "hs_code": "07020000",
        "image": "/static/images/kaybee_tomatoes_only.jpg",
        "featured": False,
        "specifications": {
            "Firmness": "High Firmness Grade",
            "Cold Chain": "5°C - 8°C Controlled Reefer"
        }
    },
    {
        "id": "veg-garlic-ginger",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Fresh Garlic Bulbs & Ginger Pods",
        "tagline": "Pungent aroma, firm cloves & long shelf life",
        "description": "High-grade fresh whole garlic bulbs, peeled garlic cloves, and clean ginger roots sourced directly from MP and Rajasthan.",
        "packaging": ["1 kg Mesh Pouch", "5 kg Master Carton", "10 kg Mesh Bag"],
        "origin": "Madhya Pradesh / Rajasthan, India",
        "moq": "10 Metric Tons",
        "shelf_life": "90 Days",
        "hs_code": "07032000",
        "image": "/static/images/kaybee_garlic_ginger_only.jpg",
        "featured": True,
        "specifications": {
            "Clove Structure": "Tight & Firm Bulbs",
            "Purity": "Root Trimmed & Machine Cleaned"
        }
    },
    {
        "id": "veg-green-chillies",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "G4 Export Green Chillies",
        "tagline": "Pungent G4 chillies with bright green color",
        "description": "Fresh spicy G4 green chillies harvested at peak crispness, residue-controlled for EU MRL compliance.",
        "packaging": ["4 kg Corrugated Cartons", "Styrofoam Thermocol Boxes"],
        "origin": "Andhra Pradesh / Maharashtra, India",
        "moq": "2 Metric Tons (Air Freight)",
        "shelf_life": "14 Days",
        "hs_code": "07096010",
        "image": "/static/images/kaybee_green_chillies.jpg",
        "featured": False,
        "specifications": {
            "Length": "6cm - 10cm",
            "Residue Standard": "EU MRL Residue Controlled"
        }
    },
    {
        "id": "veg-okra",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Fresh Okra (Lady Finger)",
        "tagline": "Tender green Okra free of fibers",
        "description": "Tender green Lady Finger (Okra) harvested early morning and air-shipped to European and Gulf wholesale distributors.",
        "packaging": ["4 kg Master Box", "Perforated Poly Bags"],
        "origin": "Gujarat / Maharashtra, India",
        "moq": "2 Metric Tons",
        "shelf_life": "10 - 12 Days",
        "hs_code": "07099990",
        "image": "/static/images/kaybee_okra.jpg",
        "featured": False,
        "specifications": {
            "Length": "8cm - 12cm Tender",
            "Color": "Vibrant Dark Green"
        }
    },
    {
        "id": "veg-brinjal",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Fresh Purple Brinjal (Eggplant)",
        "tagline": "Glossy purple skin, firm flesh & seedless interior",
        "description": "Export quality Ravaiya and long purple eggplants, packed under cold chain logistics for international fresh markets.",
        "packaging": ["5 kg Corrugated Cartons"],
        "origin": "Maharashtra, India",
        "moq": "3 Metric Tons",
        "shelf_life": "14 Days",
        "hs_code": "07093000",
        "image": "/static/images/kaybee_brinjal.jpg",
        "featured": False,
        "specifications": {
            "Skin": "Glossy Purple",
            "Texture": "Firm Flesh"
        }
    },
    {
        "id": "veg-gourds",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Bottle Gourd & Bitter Gourd Range",
        "tagline": "Farm fresh Bottle, Bitter, Ridge & Sponge Gourds",
        "description": "A complete range of fresh Indian gourds including tender Bottle Gourd, Bitter Gourd (Karela), Ridge Gourd, and Sponge Gourd.",
        "packaging": ["5 kg Master Cartons"],
        "origin": "Maharashtra / Gujarat, India",
        "moq": "3 Metric Tons",
        "shelf_life": "14 Days",
        "hs_code": "07099990",
        "image": "/static/images/kaybee_gourds_only.jpg",
        "featured": False,
        "specifications": {
            "Freshness": "Peak Harvest Tender Pods",
            "Certifications": "Phytosanitary Certified"
        }
    },
    {
        "id": "veg-coriander-mint",
        "category": "vegetables",
        "category_label": "Fresh Vegetables",
        "name": "Fresh Coriander & Mint Leaves",
        "tagline": "Aromatic fresh green Herbs & Curry Leaves",
        "description": "Farm-fresh aromatic Coriander leaves, Pudina (Mint), Curry Leaves, and Spinach hydro-cooled and air-shipped to international supermarkets.",
        "packaging": ["Clamshell Trays", "Pre-cooled Vented Cartons"],
        "origin": "Maharashtra, India",
        "moq": "1 Metric Ton (Air Freight)",
        "shelf_life": "7 - 10 Days",
        "hs_code": "07099910",
        "image": "/static/images/kaybee_coriander_mint.jpg",
        "featured": False,
        "specifications": {
            "Aroma": "100% Natural Fresh Aroma",
            "Handling": "Pre-chilled Hydro-cooled"
        }
    },

    # --- 3. WHEAT & GRAINS (INDIVIDUAL SEPARATE ITEMS) ---
    {
        "id": "wheat-sharbati",
        "category": "wheat",
        "category_label": "Wheat & Grains",
        "name": "MP Sharbati Golden Whole Wheat",
        "tagline": "Golden grains, sweet taste & superior milling quality",
        "description": "Known as the golden grain of India, MP Sharbati wheat is harvested from rain-fed fields of Madhya Pradesh, yielding soft, sweet, golden flour.",
        "packaging": ["25 kg BOPP Laminated", "50 kg PP Woven Bags", "Jute Sacks"],
        "origin": "Madhya Pradesh, India",
        "moq": "24 Metric Tons (40ft FCL)",
        "shelf_life": "12 Months",
        "hs_code": "10019910",
        "image": "/static/images/kaybee_sharbati_only.jpg",
        "featured": True,
        "specifications": {
            "Protein Content": "13% - 14%",
            "Gluten": "30% - 32%",
            "Moisture": "< 11.5%",
            "Grain Color": "Lustrous Golden Yellow"
        }
    },
    {
        "id": "wheat-durum",
        "category": "wheat",
        "category_label": "Wheat & Grains",
        "name": "Lokwan & Durum Hard Export Wheat",
        "tagline": "High vitreous hard amber wheat for pasta & semolina",
        "description": "High vitreous count Durum wheat and Lokwan wheat varieties preferred by industrial flour mills, semolina manufacturers, and pasta producers.",
        "packaging": ["50 kg PP Woven Bags", "Bulk Container Liners"],
        "origin": "Madhya Pradesh / Maharashtra, India",
        "moq": "25 Metric Tons",
        "shelf_life": "12 Months",
        "hs_code": "10011900",
        "image": "/static/images/kaybee_durum_only.jpg",
        "featured": True,
        "specifications": {
            "Vitreous Kernel": "> 80%",
            "Hectoliter Weight": "> 78 kg/hl",
            "Protein": "12.5%+"
        }
    },
    {
        "id": "wheat-flour",
        "category": "wheat",
        "category_label": "Wheat & Grains",
        "name": "Whole Wheat Atta & Refined Maida",
        "tagline": "Whole Wheat Atta, Refined Maida, Suji & Wheat Bran",
        "description": "Kaybee Global exports fine roller-milled Whole Wheat Atta, Refined Flour (Maida), Semolina (Suji/Rava), Broken Wheat (Dalia), and Wheat Bran for animal feed.",
        "packaging": ["1 kg / 5 kg Retail Bags", "25 kg / 50 kg PP Bags"],
        "origin": "India",
        "moq": "20 Metric Tons",
        "shelf_life": "6 - 9 Months",
        "hs_code": "11010000",
        "image": "/static/images/kaybee_atta_flour.jpg",
        "featured": False,
        "specifications": {
            "Ash Content": "< 0.5% (Maida), < 1.5% (Atta)",
            "Water Absorption": "> 65%"
        }
    },

    # --- 4. FRESH FRUITS ---
    {
        "id": "fruits-mangoes",
        "category": "fruits",
        "category_label": "Fresh Export Fruits",
        "name": "Ratnagiri Alphonso & Kesar Mangoes",
        "tagline": "GI-Tagged King of Mangoes with heavenly aroma",
        "description": "Premium Ratnagiri Alphonso and Gir Kesar mangoes harvested at peak maturity. VHT (Vapor Heat Treatment) and Irradiation certified for USA, EU, and Gulf markets.",
        "packaging": ["3.5 kg Air Export Cartons", "5 kg Telescopic Corrugated Boxes"],
        "origin": "Ratnagiri & Devgad (Maharashtra), Gir (Gujarat)",
        "moq": "2 Metric Tons (Air Freight) / 10 Tons (Sea Reefer)",
        "shelf_life": "14 - 18 Days",
        "hs_code": "08045020",
        "image": "/static/images/kaybee_mangoes.jpg",
        "featured": True,
        "specifications": {
            "Brix Level": "18° - 22° Brix",
            "Treatment": "VHT / Irradiation Certified"
        }
    },
    {
        "id": "fruits-pomegranates",
        "category": "fruits",
        "category_label": "Fresh Export Fruits",
        "name": "Bhagwa Ruby Red Pomegranates",
        "tagline": "Deep crimson soft-seeded arils & high antioxidants",
        "description": "Kaybee Global exports world-famous Bhagwa variety pomegranates known for glossy dark red skin, juicy soft seeds, and long shelf life.",
        "packaging": ["3.5 kg Master Box", "4.5 kg Corrugated Export Box"],
        "origin": "Solapur, Maharashtra, India",
        "moq": "5 Metric Tons",
        "shelf_life": "45 - 60 Days",
        "hs_code": "08109010",
        "image": "/static/images/kaybee_pomegranates.jpg",
        "featured": True,
        "specifications": {
            "Color": "Deep Glossy Ruby Red",
            "Seed Quality": "Soft Seeded & High Juice Yield"
        }
    },
    {
        "id": "fruits-grapes",
        "category": "fruits",
        "category_label": "Fresh Export Fruits",
        "name": "Thompson Green & Black Jumbo Grapes",
        "tagline": "Crisp, seedless, high Brix table grapes",
        "description": "Export-quality Thompson Seedless Green Grapes and Black Jumbo Grapes cultivated in Nashik, packed in protective clamshell trays under cold chain logistics.",
        "packaging": ["5 kg Master Carton", "500g Clamshell Punnet Trays"],
        "origin": "Nashik, Maharashtra, India",
        "moq": "12 Metric Tons (40ft Reefer)",
        "shelf_life": "30 - 45 Days",
        "hs_code": "08061000",
        "image": "/static/images/kaybee_grapes.jpg",
        "featured": True,
        "specifications": {
            "Berry Size": "16mm - 18mm+",
            "Brix Level": "16°+ Brix"
        }
    },

    # --- 5. RICE ---
    {
        "id": "rice-basmati-1121",
        "category": "rice",
        "category_label": "Premium Export Rice",
        "name": "1121 Extra Long Grain Basmati Rice",
        "tagline": "World's longest grain basmati with heavenly aroma",
        "description": "Kaybee Global's flagship 1121 Basmati Rice elongates up to 2.5 times upon cooking. Perfect for royal biryanis, fine dining, and international gourmet cuisine.",
        "packaging": ["1 kg Non-Woven Pouch", "5 kg / 10 kg Pet Bags", "20 kg Jute Bag", "25 kg / 50 kg PP Bags"],
        "origin": "Punjab & Haryana, India",
        "moq": "20 Metric Tons",
        "shelf_life": "24 Months",
        "hs_code": "10063020",
        "image": "/static/images/kaybee_rice_basmati.jpg",
        "featured": True,
        "specifications": {
            "Average Grain Length": "8.35 mm+",
            "Purity": "95%",
            "Moisture": "< 12.5%"
        }
    },
    {
        "id": "rice-non-basmati",
        "category": "rice",
        "category_label": "Premium Export Rice",
        "name": "Sona Masoori & IR64 Rice",
        "tagline": "Lightweight, aromatic daily staple & parboiled export rice",
        "description": "High quality non-basmati varieties including Sona Masoori raw/parboiled and IR64 5%/25% broken for volume international buyers.",
        "packaging": ["25 kg PP Woven Bags", "50 kg BOPP Bags"],
        "origin": "Andhra Pradesh / Telangana, India",
        "moq": "25 Metric Tons",
        "shelf_life": "24 Months",
        "hs_code": "10063090",
        "image": "/static/images/kaybee_rice_sona.jpg",
        "featured": False,
        "specifications": {
            "Grain Type": "Medium & Short Grain",
            "Broken Percentage": "5% / 25% Options"
        }
    },

    # --- 6. SPICES ---
    {
        "id": "spices-assorted",
        "category": "spices",
        "category_label": "Indian Spices",
        "name": "Pure Indian Whole & Ground Spices",
        "tagline": "High curcumin, potent aroma & international spice board standards",
        "description": "Kaybee Global exports authentic Indian spices sourced directly from spice capitals. Lab tested for curcumin content, volatile oils, and zero adulteration.",
        "packaging": ["100g / 500g Retail Pouches", "10 kg Vacuum Bags", "25 kg Jute / PP Bags"],
        "origin": "Kerala / Tamil Nadu / Rajasthan, India",
        "moq": "3 Metric Tons",
        "shelf_life": "18 - 24 Months",
        "hs_code": "09103030",
        "image": "/static/images/kaybee_spices_img.jpg",
        "featured": True,
        "specifications": {
            "Curcumin Content": "Up to 5% (Turmeric)",
            "Purity": "99.5% Machine Cleaned"
        }
    }
]

TRADE_DESTINATIONS = [
    {"name": "Middle East (Jebel Ali / Dubai)", "code": "DXB", "coords": [25.2048, 55.2708], "transit_days": "4-6 Days", "container_rate_usd": 1200},
    {"name": "Europe (Rotterdam / Hamburg)", "code": "RTM", "coords": [51.9244, 4.4777], "transit_days": "18-22 Days", "container_rate_usd": 2800},
    {"name": "North America (New York / Los Angeles)", "code": "NYC", "coords": [40.7128, -74.0060], "transit_days": "25-30 Days", "container_rate_usd": 4200},
    {"name": "Southeast Asia (Singapore / Port Klang)", "code": "SIN", "coords": [1.3521, 103.8198], "transit_days": "7-10 Days", "container_rate_usd": 1100},
    {"name": "Africa (Mombasa / Durban)", "code": "MBA", "coords": [-4.0435, 39.6682], "transit_days": "12-15 Days", "container_rate_usd": 2100},
    {"name": "Australia (Sydney / Melbourne)", "code": "SYD", "coords": [-33.8688, 151.2093], "transit_days": "16-20 Days", "container_rate_usd": 2400}
]

COMPANY_INFO = {
    "name": "KayBee Global",
    "slogan": "Connecting Culture, Creating Value",
    "address": "Sr. 50, Office no.1 15/1, Samarth Sankul, Near Bank of Maharashtra, Narhe Road, Pune, Maharashtra 411041.",
    "phone": "+91 7499417458",
    "email": "info@kaybeeglobal.com",
    "website": "www.kaybeeglobal.com",
    "socials": {
        "twitter": "https://x.com/KayBeeGlobal1",
        "youtube": "https://www.youtube.com/@KayBeeGlobal"
    }
}

@app.route('/')
def index():
    return render_template('index.html', company=COMPANY_INFO, products=PRODUCTS_DATABASE, destinations=TRADE_DESTINATIONS)

@app.route('/api/products')
def get_products():
    category = request.args.get('category', 'all')
    if category != 'all':
        filtered = [p for p in PRODUCTS_DATABASE if p['category'] == category]
        return jsonify(filtered)
    return jsonify(PRODUCTS_DATABASE)

@app.route('/api/products/<product_id>')
def get_product_detail(product_id):
    product = next((p for p in PRODUCTS_DATABASE if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/rfq/calculate', methods=['POST'])
def calculate_rfq():
    data = request.json or {}
    product_id = data.get('product_id', 'onions-red')
    quantity_tons = float(data.get('quantity_tons', 20))
    destination = data.get('destination', 'DXB')
    incoterm = data.get('incoterm', 'FOB')
    packaging = data.get('packaging', 'Standard Mesh Bags')

    product = next((p for p in PRODUCTS_DATABASE if p['id'] == product_id), PRODUCTS_DATABASE[0])
    dest_info = next((d for d in TRADE_DESTINATIONS if d['code'] == destination), TRADE_DESTINATIONS[0])

    base_price_per_ton = 450
    if 'basmati' in product_id or 'rice' in product_id:
        base_price_per_ton = 1150
    elif 'spices' in product_id:
        base_price_per_ton = 2400
    elif 'fruits' in product_id or 'mangoes' in product_id or 'pomegranates' in product_id:
        base_price_per_ton = 1600
    elif 'wheat' in product_id:
        base_price_per_ton = 380

    subtotal_goods = quantity_tons * base_price_per_ton
    containers_needed = max(1, int(quantity_tons // 18) + (1 if quantity_tons % 18 > 0 else 0))
    freight_cost = containers_needed * dest_info['container_rate_usd'] if incoterm == 'CIF' else 0
    insurance_cost = subtotal_goods * 0.015 if incoterm == 'CIF' else 0
    total_quote = subtotal_goods + freight_cost + insurance_cost

    return jsonify({
        "quote_id": f"KBG-RFQ-{uuid.uuid4().hex[:6].upper()}",
        "product_name": product['name'],
        "quantity_tons": quantity_tons,
        "containers_count": containers_needed,
        "container_type": "40ft Reefer" if product['category'] in ['vegetables', 'fruits', 'onions'] else "20ft Heavy FCL",
        "incoterm": incoterm,
        "destination": dest_info['name'],
        "transit_days": dest_info['transit_days'],
        "subtotal_goods_usd": round(subtotal_goods, 2),
        "freight_cost_usd": round(freight_cost, 2),
        "insurance_usd": round(insurance_cost, 2),
        "total_quote_usd": round(total_quote, 2),
        "currency": "USD",
        "company_contact": COMPANY_INFO['email']
    })

@app.route('/api/pay/process', methods=['POST'])
def process_payment():
    data = request.json or {}
    amount = data.get('amount', 500.0)
    currency = data.get('currency', 'USD')
    payment_method = data.get('payment_method', 'card')
    buyer_name = data.get('buyer_name', 'Global Trade Partner')
    buyer_email = data.get('buyer_email', 'buyer@trade.com')
    order_ref = data.get('order_ref', f"KBG-ORD-{uuid.uuid4().hex[:8].upper()}")

    transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "status": "SUCCESS",
        "transaction_id": transaction_id,
        "order_ref": order_ref,
        "amount": amount,
        "currency": currency,
        "payment_method": payment_method.upper(),
        "timestamp": timestamp,
        "buyer_name": buyer_name,
        "buyer_email": buyer_email,
        "message": "Payment authorization successful.",
        "swift_code": "MAHBIN41PUN",
        "bank_account": "KayBee Global Exports A/C 60494174581",
        "company": COMPANY_INFO
    })

if __name__ == '__main__':
    print("Starting KayBee Global 3D Import Export Web Application on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
