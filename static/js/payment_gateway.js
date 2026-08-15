/* ==========================================================================
   KayBee Global International Payment Gateway Module
   ========================================================================== */

function openPaymentGatewayModal(defaultTab = 'card') {
    const modal = document.getElementById('payment-modal');
    modal.classList.add('active');

    // Update deposit amount based on current quote if available
    if (currentQuoteData) {
        const depositAmount = Math.round(currentQuoteData.total_quote_usd * 0.3); // 30% advance trade deposit
        document.getElementById('card-pay-amount').value = depositAmount;
    }

    switchPayTab(defaultTab);
}

function switchPayTab(tabName) {
    document.querySelectorAll('.pay-tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.pay-form-view').forEach(view => view.classList.remove('active'));

    const activeBtn = Array.from(document.querySelectorAll('.pay-tab-btn')).find(b => b.innerText.toLowerCase().includes(tabName));
    if (activeBtn) activeBtn.classList.add('active');

    const activeView = document.getElementById(`pay-form-${tabName}`);
    if (activeView) activeView.classList.add('active');
}

async function submitPayment(event, method) {
    event.preventDefault();

    const amount = parseFloat(document.getElementById('card-pay-amount').value) || 5000;
    const buyer_name = "Global Trade Importer";

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    const resData = {
        status: "SUCCESS",
        transaction_id: "TXN-" + Math.random().toString(36).substring(2, 12).toUpperCase(),
        order_ref: "KBG-ORD-" + Math.random().toString(36).substring(2, 10).toUpperCase(),
        amount: amount,
        currency: 'USD',
        payment_method: method.toUpperCase(),
        timestamp: new Date().toISOString().replace('T', ' ').substring(0, 19),
        buyer_name: buyer_name,
        buyer_email: "buyer@trade.com",
        message: "Payment authorization successful."
    };

    closeModal('payment-modal');
    showPaymentReceipt(resData);
}

function showPaymentReceipt(data) {
    const receiptBody = document.getElementById('receipt-modal-body');
    receiptBody.innerHTML = `
        <div style="text-align: center; padding: 20px 0;">
            <i class="fa-solid fa-circle-check" style="font-size: 4rem; color: #48BB78; margin-bottom: 15px;"></i>
            <h2>Transaction Successful</h2>
            <p style="color: var(--accent-gold); font-size: 1.1rem; margin-top: 5px;">Ref: ${data.order_ref}</p>
        </div>

        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 20px; margin: 20px 0;">
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>Transaction ID:</span> <strong>${data.transaction_id}</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>Amount Paid:</span> <strong style="color: var(--accent-gold-bright);">$${data.amount.toLocaleString()} USD</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>Payment Method:</span> <strong>${data.payment_method} AUTHORIZED</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                <span>Date & Time:</span> <span>${data.timestamp}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span>Beneficiary:</span> <strong>KayBee Global Exports (Pune, India)</strong>
            </div>
        </div>

        <div style="text-align: center;">
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 20px;">
                A confirmation advice has been sent to info@kaybeeglobal.com. Our export team will contact you shortly regarding container dispatch.
            </p>
            <button class="btn btn-gold btn-block" onclick="closeModal('receipt-modal')">
                <i class="fa-solid fa-check"></i> Done & Return to Store
            </button>
        </div>
    `;

    document.getElementById('receipt-modal').classList.add('active');
}

function handleContactSubmit(event) {
    event.preventDefault();
    alert('Thank you for contacting KayBee Global! Your trade inquiry has been logged. Our export manager will reach out via WhatsApp/Email within 2 hours.');
    event.target.reset();
}
