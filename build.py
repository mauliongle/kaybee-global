import os
import shutil
from app import app, COMPANY_INFO, PRODUCTS_DATABASE, TRADE_DESTINATIONS
from flask import render_template

def build():
    print("Starting static build...")
    public_dir = os.path.join(os.path.dirname(__file__), 'public')
    
    # Clean and recreate public dir
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)
    
    # Copy static assets
    print("Copying static assets...")
    shutil.copytree(os.path.join(os.path.dirname(__file__), 'static'), os.path.join(public_dir, 'static'))
    
    # Render and save templates
    print("Rendering templates...")
    with app.test_request_context():
        # Render index.html
        index_html = render_template('index.html', company=COMPANY_INFO, products=PRODUCTS_DATABASE, destinations=TRADE_DESTINATIONS)
        with open(os.path.join(public_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
            
        # Render about.html
        about_dir = os.path.join(public_dir, 'about')
        os.makedirs(about_dir)
        about_html = render_template('about.html', company=COMPANY_INFO)
        with open(os.path.join(about_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(about_html)

    print("Static build complete. Output is in the 'public/' directory.")

if __name__ == '__main__':
    build()
