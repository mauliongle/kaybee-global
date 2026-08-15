/* ==========================================================================
   KayBee Global Product Catalog Module
   ========================================================================== */

let allProducts = [];
let activeCategory = 'all';

document.addEventListener('DOMContentLoaded', () => {
    fetchProducts();
});

async function fetchProducts() {
    try {
        allProducts = window.PRODUCTS_DATABASE;
        renderProducts(allProducts);
    } catch (err) {
        console.error('Failed to load products:', err);
    }
}

function renderProducts(products) {
    const grid = document.getElementById('product-grid');
    if (!grid) return;

    if (products.length === 0) {
        grid.innerHTML = '<div class="no-products"><p>No products match your filter.</p></div>';
        return;
    }

    grid.innerHTML = products.map(p => `
        <div class="product-card">
            <div class="card-img-wrapper">
                <img src="${p.image}" alt="${p.name}" class="card-img" onerror="this.src='/static/images/kaybee_onions_img.jpg'">
                <span class="card-badge">${p.category_label}</span>
            </div>

            <div class="card-body">
                <h3 class="product-title">${p.name}</h3>
                <p class="product-tagline">${p.tagline}</p>
                <p class="product-desc">${p.description.substring(0, 110)}...</p>

                <div class="card-meta-list">
                    <div class="meta-item">
                        <span><i class="fa-solid fa-earth-americas"></i> Origin:</span>
                        <strong>${p.origin}</strong>
                    </div>
                    <div class="meta-item">
                        <span><i class="fa-solid fa-truck-ramp-box"></i> MOQ:</span>
                        <strong>${p.moq}</strong>
                    </div>
                    <div class="meta-item">
                        <span><i class="fa-solid fa-barcode"></i> HS Code:</span>
                        <strong>${p.hs_code}</strong>
                    </div>
                </div>

                <div class="card-actions">
                    <button class="btn btn-gold btn-block" onclick="quickQuoteForProduct('${p.id}')">
                        <i class="fa-solid fa-calculator"></i> Get Instant Quote
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function setCategoryFilter(category, btnElement) {
    activeCategory = category;

    // Update active tab styling
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');

    filterProducts();
}

function filterProducts() {
    const searchInput = document.getElementById('catalog-search-input');
    const query = searchInput ? searchInput.value.toLowerCase().trim() : '';

    let filtered = allProducts;

    if (activeCategory !== 'all') {
        filtered = filtered.filter(p => p.category === activeCategory);
    }

    if (query) {
        filtered = filtered.filter(p => 
            p.name.toLowerCase().includes(query) ||
            p.tagline.toLowerCase().includes(query) ||
            p.description.toLowerCase().includes(query)
        );
    }

    renderProducts(filtered);
}

function openProduct3DModal(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;

    document.getElementById('modal-product-name').innerText = product.name;
    document.getElementById('modal-category-label').innerText = product.category_label;
    document.getElementById('modal-tagline').innerText = product.tagline;
    document.getElementById('modal-description').innerText = product.description;

    // Spec table rendering
    const specTable = document.getElementById('modal-spec-table');
    let specRows = `
        <tr><td><strong>Origin</strong></td><td>${product.origin}</td></tr>
        <tr><td><strong>MOQ</strong></td><td>${product.moq}</td></tr>
        <tr><td><strong>Shelf Life</strong></td><td>${product.shelf_life}</td></tr>
        <tr><td><strong>HS Code</strong></td><td>${product.hs_code}</td></tr>
    `;

    if (product.specifications) {
        Object.entries(product.specifications).forEach(([k, v]) => {
            specRows += `<tr><td><strong>${k}</strong></td><td>${v}</td></tr>`;
        });
    }

    if (product.packaging) {
        specRows += `<tr><td><strong>Packaging</strong></td><td>${product.packaging.join(', ')}</td></tr>`;
    }

    specTable.innerHTML = specRows;

    // Open Modal
    const modal = document.getElementById('product-3d-modal');
    modal.classList.add('active');

    // Init 3D Canvas
    setTimeout(() => {
        initProduct3DViewer(product);
    }, 100);
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function quickQuoteForProduct(productId) {
    const select = document.getElementById('rfq-product-select');
    if (select) {
        select.value = productId;
        recalculateQuote();
    }
    window.location.href = '#rfq-calculator';
}

function selectProductForRfq() {
    closeModal('product-3d-modal');
    window.location.href = '#rfq-calculator';
}
