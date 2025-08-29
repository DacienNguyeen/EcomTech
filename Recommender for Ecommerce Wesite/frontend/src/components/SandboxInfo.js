import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SandboxInfo = () => {
  const [sandboxInfo, setSandboxInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_BASE = 'http://127.0.0.1:8000/api/v1';

  useEffect(() => {
    fetchSandboxInfo();
  }, []);

  const fetchSandboxInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE}/payments/sandbox/info/`, { withCredentials: true });
      setSandboxInfo(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.message);
    } finally {
      setLoading(false);
    }
  };

  const simulateWebhook = async (paymentId, eventType) => {
    try {
      const response = await axios.post(`${API_BASE}/payments/sandbox/webhook/${paymentId}/`, {
        event_type: eventType
      }, { withCredentials: true });
      alert(`Webhook simulated: ${JSON.stringify(response.data, null, 2)}`);
    } catch (err) {
      alert(`Webhook error: ${err.response?.data?.error || err.message}`);
    }
  };

  if (loading) return <div>Loading sandbox info...</div>;
  if (error) return <div style={{ color: 'red' }}>Error: {error}</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Payment Sandbox Information</h1>
      
      {sandboxInfo && (
        <div>
          {/* Environment Info */}
          <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>Environment</h3>
            <p><strong>Mode:</strong> {sandboxInfo.sandbox_mode ? 'Sandbox' : 'Production'}</p>
            <p><strong>Version:</strong> {sandboxInfo.version}</p>
            <p><strong>Environment:</strong> {sandboxInfo.environment}</p>
          </div>

          {/* Test Cards */}
          <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>Test Card Numbers</h3>
            
            <h4 style={{ color: 'green' }}>Success Cards</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginBottom: '20px' }}>
              {Object.entries(sandboxInfo.test_cards?.success || {}).map(([type, number]) => (
                <div key={type} style={{ padding: '10px', backgroundColor: '#d4edda', borderRadius: '5px' }}>
                  <strong>{type.toUpperCase()}</strong><br/>
                  <code>{number}</code>
                </div>
              ))}
            </div>

            <h4 style={{ color: 'red' }}>Decline Cards</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '10px' }}>
              {Object.entries(sandboxInfo.test_cards?.decline || {}).map(([type, number]) => (
                <div key={type} style={{ padding: '10px', backgroundColor: '#f8d7da', borderRadius: '5px' }}>
                  <strong>{type.replace(/_/g, ' ').toUpperCase()}</strong><br/>
                  <code>{number}</code>
                </div>
              ))}
            </div>
          </div>

          {/* Payment Methods */}
          <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>Supported Payment Methods</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {sandboxInfo.payment_methods?.map(method => (
                <span key={method} style={{ 
                  padding: '5px 10px', 
                  backgroundColor: '#e9ecef', 
                  borderRadius: '3px',
                  fontSize: '14px'
                }}>
                  {method.replace(/_/g, ' ').toUpperCase()}
                </span>
              ))}
            </div>
          </div>

          {/* API Endpoints */}
          <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>API Endpoints</h3>
            <div style={{ fontFamily: 'monospace', fontSize: '14px' }}>
              <div style={{ marginBottom: '10px' }}>
                <strong>POST</strong> <code>/api/v1/payments/charge/</code> - Process Payment
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>GET</strong> <code>/api/v1/payments/[id]/status/</code> - Check Payment Status
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>POST</strong> <code>/api/v1/payments/[id]/refund/</code> - Process Refund
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>POST</strong> <code>/api/v1/payments/sandbox/webhook/[id]/</code> - Simulate Webhook
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>GET</strong> <code>/api/v1/payments/sandbox/info/</code> - Sandbox Information
              </div>
            </div>
          </div>

          {/* Webhook Simulator */}
          <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h3>Webhook Simulator</h3>
            <p>Test webhook events for payment processing:</p>
            
            <div style={{ marginBottom: '10px' }}>
              <input 
                type="text" 
                placeholder="Payment ID" 
                id="webhook-payment-id"
                style={{ padding: '8px', marginRight: '10px', width: '200px' }}
              />
            </div>
            
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
              {['payment_intent.succeeded', 'payment_intent.payment_failed', 'charge.dispute.funds_withdrawn'].map(eventType => (
                <button
                  key={eventType}
                  onClick={() => {
                    const paymentId = document.getElementById('webhook-payment-id').value;
                    if (paymentId) {
                      simulateWebhook(paymentId, eventType);
                    } else {
                      alert('Please enter a Payment ID');
                    }
                  }}
                  style={{
                    padding: '8px 12px',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '12px'
                  }}
                >
                  {eventType}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SandboxInfo;
