/* ==========================================================================
   KayBee Global RFQ & Container Load Calculator Module
   ========================================================================== */

let currentQuoteData = null;

document.addEventListener('DOMContentLoaded', () => {
    recalculateQuote();
});

async function recalculateQuote() {
    const product_id = document.getElementById('rfq-product-select').value;
    const quantity_tons = parseFloat(document.getElementById('rfq-quantity').value);
    const destination = document.getElementById('rfq-destination').value;
    const incoterm = document.getElementById('rfq-incoterm').value;
    const packaging = document.getElementById('rfq-packaging').value;

    try {
        const response = await fetch('/api/rfq/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                product_id,
                quantity_tons,
                destination,
                incoterm,
                packaging
            })
        });

        currentQuoteData = await response.json();
        updateQuoteUI(currentQuoteData);

    } catch (err) {
        console.error('Failed to calculate RFQ:', err);
    }
}

function updateQuoteUI(quote) {
    document.getElementById('summary-product').innerText = quote.product_name;
    document.getElementById('summary-containers').innerText = `${quote.containers_count} x ${quote.container_type} (${quote.quantity_tons} MT)`;
    document.getElementById('summary-transit').innerText = quote.transit_days;

    document.getElementById('summary-goods').innerText = `$${quote.subtotal_goods_usd.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById('summary-freight').innerText = `$${quote.freight_cost_usd.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    document.getElementById('summary-insurance').innerText = `$${quote.insurance_usd.toLocaleString('en-US', {minimumFractionDigits: 2})}`;

    document.getElementById('summary-total').innerText = `$${quote.total_quote_usd.toLocaleString('en-US', {minimumFractionDigits: 2})} USD`;
}

function openRfqModal() {
    window.location.href = '#rfq-calculator';
}

function downloadProformaInvoice() {
    if (!currentQuoteData) return;

    const invoiceWindow = window.open('', '_blank');
    invoiceWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Proforma Invoice - ${currentQuoteData.quote_id}</title>
            <style>
                body { font-family: 'Helvetica Neue', Arial, sans-serif; padding: 40px; color: #111; line-height: 1.5; }
                .header { display: flex; justify-content: space-between; border-bottom: 2px solid #E5CB9E; padding-bottom: 20px; }
                .logo { font-size: 24px; font-weight: bold; color: #1D1838; }
                .slogan { color: #888; font-size: 13px; }
                .inv-title { font-size: 22px; color: #C5A367; font-weight: bold; }
                .details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0; }
                .box { background: #f9f9f9; padding: 15px; border-radius: 8px; border: 1px solid #ddd; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
                th { background: #1D1838; color: #FFF; }
                .total-row td { font-weight: bold; font-size: 18px; color: #1D1838; border-top: 2px solid #1D1838; }
                .footer { margin-top: 50px; font-size: 12px; color: #777; text-align: center; }
            </style>
        </head>
        <body>
            <div class="header">
                <div>
                    <div class="logo">KAYBEE GLOBAL</div>
                    <div class="slogan">Connecting Culture, Creating Value</div>
                    <p>Sr. 50, Office no.1 15/1, Samarth Sankul, Near Bank of Maharashtra,<br>Narhe Road, Pune, Maharashtra 411041<br>Phone: +91 7499417458 | Email: info@kaybeeglobal.com</p>
                </div>
                <div style="text-align: right;">
                    <div class="inv-title">OFFICIAL PROFORMA INVOICE</div>
                    <p><strong>Quote Ref:</strong> ${currentQuoteData.quote_id}</p>
                    <p><strong>Date:</strong> ${new Date().toLocaleDateString()}</p>
                    <p><strong>Incoterm:</strong> ${currentQuoteData.incoterm}</p>
                </div>
            </div>

            <div class="details-grid">
                <div class="box">
                    <strong>Exporter / Seller:</strong><br>
                    KayBee Global Exports<br>
                    APEDA & Phytosanitary Registered<br>
                    Pune, Maharashtra, India
                </div>
                <div class="box">
                    <strong>Shipment Destination:</strong><br>
                    Port: ${currentQuoteData.destination}<br>
                    Estimated Transit: ${currentQuoteData.transit_days}<br>
                    Container Allocation: ${currentQuoteData.containers_count} x ${currentQuoteData.container_type}
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Item Description</th>
                        <th>Quantity</th>
                        <th>Incoterm</th>
                        <th>Amount (USD)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>${currentQuoteData.product_name}</strong><br>Export-grade sorting, machine-cleaned & inspected</td>
                        <td>${currentQuoteData.quantity_tons} MT</td>
                        <td>${currentQuoteData.incoterm}</td>
                        <td>$${currentQuoteData.subtotal_goods_usd.toFixed(2)}</td>
                    </tr>
                    <tr>
                        <td>International Shipping & Container Freight</td>
                        <td>${currentQuoteData.containers_count} Unit(s)</td>
                        <td>Freight</td>
                        <td>$${currentQuoteData.freight_cost_usd.toFixed(2)}</td>
                    </tr>
                    <tr>
                        <td>Comprehensive Marine Cargo Insurance</td>
                        <td>Full Coverage</td>
                        <td>Insurance</td>
                        <td>$${currentQuoteData.insurance_usd.toFixed(2)}</td>
                    </tr>
                    <tr class="total-row">
                        <td colspan="3" style="text-align: right;">Total Estimated Payable:</td>
                        <td>$${currentQuoteData.total_quote_usd.toFixed(2)} USD</td>
                    </tr>
                </tbody>
            </table>

            <div class="footer">
                <p>This is a computer-generated Proforma Invoice by KayBee Global Automated Trade System.</p>
            </div>
            <script>window.print();</script>
        </body>
        </html>
    `);
    invoiceWindow.document.close();
}
