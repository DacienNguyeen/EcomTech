import React, { useState } from 'react';
import API from '../api';

const Payment = () => {
  const [paymentData, setPaymentData] = useState({
    amount: '100000',
    payment_method: 'credit_card',
    card_number: '4111111111111111',
    card_holder: 'John Doe',
    card_expiry: '12/2025',
    card_cvv: '123'
  });
  
  const [orderData, setOrderData] = useState({
    customer_name: 'Test Customer',
    items: [
      { book_id: 1, quantity: 1 },
      { book_id: 2, quantity: 1 }
    ]
  });
  
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [orderId, setOrderId] = useState(null);

  // Create order first
  const createOrder = async () => {
    try {
      const response = await API.post('/orders/', {
        customer_name: orderData.customer_name,
        items: orderData.items,
        total_amount: orderData.items.reduce((sum, item) => sum + (item.price * item.quantity), 0),
        status: 'pending'
      });
      return response.data.order_id;
    } catch (err) {
      console.error('Create order error:', err);
      throw err;
    }
  };

  // Process payment
  const handlePayment = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      // First create order if not exists
      let currentOrderId = orderId;
      if (!currentOrderId) {
        currentOrderId = await createOrder();
        setOrderId(currentOrderId);
      }

      // Then process payment
      const response = await API.post('/payments/charge/', {
        order_id: currentOrderId,
        ...paymentData
      });

      setResult({
        success: true,
        data: response.data,
        message: 'Payment processed successfully!'
      });

    } catch (err) {
      setError(err.response?.data?.error || err.message);
      setResult({
        success: false,
        error: err.response?.data || { error: err.message }
      });
    } finally {
      setLoading(false);
    }
  };

  // Get payment status
  const checkPaymentStatus = async (paymentId) => {
    try {
      const response = await API.get(`/payments/${paymentId}/status/`);
      alert(`Payment Status: ${response.data.status}\nMessage: ${response.data.message}`);
    } catch (err) {
      alert(`Error: ${err.response?.data?.error || err.message}`);
    }
  };

  // Test different card numbers
  const testCards = {
    success_visa: '4111111111111111',
    success_mastercard: '5555555555554444',
    decline_insufficient: '4000000000000002',
    decline_generic: '4000000000000069',
    decline_expired: '4000000000000069',
    decline_cvc: '4000000000000127'
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Payment Sandbox Test</h1>
      
      {/* Order Information */}
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h3>Order Information</h3>
        <div style={{ marginBottom: '10px' }}>
          <label>Customer Name: </label>
          <input 
            value={orderData.customer_name}
            onChange={(e) => setOrderData({...orderData, customer_name: e.target.value})}
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </div>
        
        <h4>Items:</h4>
        {orderData.items.map((item, idx) => (
          <div key={idx} style={{ marginLeft: '20px' }}>
            Book ID: {item.book_id} x {item.quantity}
          </div>
        ))}
        
        <div style={{ marginTop: '10px', fontWeight: 'bold' }}>
          Total: {orderData.items.length} item(s)
        </div>
        
        {orderId && <div style={{ color: 'green', marginTop: '10px' }}>Order ID: {orderId}</div>}
      </div>

      {/* Payment Form */}
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h3>Payment Details</h3>
        
        <div style={{ marginBottom: '10px' }}>
          <label>Payment Method: </label>
          <select 
            value={paymentData.payment_method}
            onChange={(e) => setPaymentData({...paymentData, payment_method: e.target.value})}
            style={{ marginLeft: '10px', padding: '5px' }}
          >
            <option value="credit_card">Credit Card</option>
            <option value="debit_card">Debit Card</option>
            <option value="paypal">PayPal</option>
            <option value="bank_transfer">Bank Transfer</option>
            <option value="e_wallet">E-Wallet</option>
          </select>
        </div>

        {(paymentData.payment_method === 'credit_card' || paymentData.payment_method === 'debit_card') && (
          <>
            <div style={{ marginBottom: '10px' }}>
              <label>Card Number: </label>
              <input 
                value={paymentData.card_number}
                onChange={(e) => setPaymentData({...paymentData, card_number: e.target.value})}
                style={{ marginLeft: '10px', padding: '5px', width: '200px' }}
                placeholder="4111111111111111"
              />
            </div>

            <div style={{ marginBottom: '10px' }}>
              <label>Card Holder: </label>
              <input 
                value={paymentData.card_holder}
                onChange={(e) => setPaymentData({...paymentData, card_holder: e.target.value})}
                style={{ marginLeft: '10px', padding: '5px', width: '200px' }}
              />
            </div>

            <div style={{ marginBottom: '10px' }}>
              <label>Expiry: </label>
              <input 
                value={paymentData.card_expiry}
                onChange={(e) => setPaymentData({...paymentData, card_expiry: e.target.value})}
                style={{ marginLeft: '10px', padding: '5px', width: '100px' }}
                placeholder="MM/YYYY"
              />
              
              <label style={{ marginLeft: '20px' }}>CVV: </label>
              <input 
                value={paymentData.card_cvv}
                onChange={(e) => setPaymentData({...paymentData, card_cvv: e.target.value})}
                style={{ marginLeft: '10px', padding: '5px', width: '60px' }}
                placeholder="123"
              />
            </div>
          </>
        )}
      </div>

      {/* Test Cards */}
      <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '8px' }}>
        <h4>Test Card Numbers (Sandbox)</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '10px' }}>
          {Object.entries(testCards).map(([name, cardNumber]) => (
            <button
              key={name}
              onClick={() => setPaymentData({...paymentData, card_number: cardNumber})}
              style={{ 
                padding: '8px', 
                border: '1px solid #ccc', 
                borderRadius: '4px',
                backgroundColor: paymentData.card_number === cardNumber ? '#007bff' : 'white',
                color: paymentData.card_number === cardNumber ? 'white' : 'black',
                cursor: 'pointer'
              }}
            >
              {name.replace(/_/g, ' ').toUpperCase()}<br/>
              <small>{cardNumber}</small>
            </button>
          ))}
        </div>
      </div>

      {/* Action Buttons */}
      <div style={{ marginBottom: '30px' }}>
        <button 
          onClick={handlePayment}
          disabled={loading}
          style={{ 
            padding: '12px 24px', 
            backgroundColor: '#28a745', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginRight: '10px'
          }}
        >
          {loading ? 'Processing...' : 'Process Payment'}
        </button>

        <button 
          onClick={() => {
            setOrderId(null);
            setResult(null);
            setError(null);
          }}
          style={{ 
            padding: '12px 24px', 
            backgroundColor: '#6c757d', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          Reset
        </button>
      </div>

      {/* Results */}
      {error && (
        <div style={{ 
          padding: '15px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          border: '1px solid #f5c6cb', 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          <h4>Error</h4>
          <pre style={{ whiteSpace: 'pre-wrap' }}>{error}</pre>
        </div>
      )}

      {result && (
        <div style={{ 
          padding: '15px', 
          backgroundColor: result.success ? '#d4edda' : '#f8d7da', 
          color: result.success ? '#155724' : '#721c24', 
          border: `1px solid ${result.success ? '#c3e6cb' : '#f5c6cb'}`, 
          borderRadius: '5px',
          marginBottom: '20px'
        }}>
          <h4>{result.success ? 'Success' : 'Error'}</h4>
          <p>{result.message || 'Payment processing completed'}</p>
          
          {result.data && (
            <div>
              <p><strong>Payment ID:</strong> {result.data.payment_id}</p>
              <p><strong>Status:</strong> {result.data.status}</p>
              <p><strong>Amount:</strong> {result.data.amount} VND</p>
              <p><strong>Sandbox Mode:</strong> {result.data.sandbox_mode ? 'Yes' : 'No'}</p>
              
              {result.data.payment_id && (
                <button 
                  onClick={() => checkPaymentStatus(result.data.payment_id)}
                  style={{ 
                    padding: '8px 16px', 
                    backgroundColor: '#17a2b8', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '3px',
                    cursor: 'pointer',
                    marginTop: '10px'
                  }}
                >
                  Check Status
                </button>
              )}
            </div>
          )}
          
          <details style={{ marginTop: '10px' }}>
            <summary style={{ cursor: 'pointer' }}>Raw Response</summary>
            <pre style={{ 
              backgroundColor: '#f8f9fa', 
              padding: '10px', 
              borderRadius: '3px',
              fontSize: '12px',
              overflow: 'auto'
            }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>
        </div>
      )}
    </div>
  );
};

export default Payment;
