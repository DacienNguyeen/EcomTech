import React, { useState } from 'react';
import API from '../api';

const ApiTester = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const addResult = (test, result) => {
    setResults(prev => [...prev, { test, result, timestamp: new Date().toLocaleTimeString() }]);
  };

  const testApis = async () => {
    setLoading(true);
    setResults([]);

    try {
      // Test 1: Sandbox Info
      try {
        const sandboxResponse = await API.get('/payments/sandbox/info/');
        addResult('Sandbox Info API', { 
          success: true, 
          data: sandboxResponse.data,
          status: sandboxResponse.status 
        });
      } catch (err) {
        addResult('Sandbox Info API', { 
          success: false, 
          error: err.message,
          status: err.response?.status 
        });
      }

      // Test 2: Create Mock Order (updated payload format)
      try {
        const orderResponse = await API.post('/orders/', {
          from_cart: false,  // Use explicit items instead of session cart
          items: [{ book_id: 1, quantity: 1 }]  // Backend expects book_id format
        });
        addResult('Create Order API', { 
          success: true, 
          data: orderResponse.data,
          status: orderResponse.status 
        });

        // Test 3: Process Payment with created order
        const orderId = orderResponse.data.order_id;
        try {
          const paymentResponse = await API.post('/payments/charge/', {
            order_id: orderId,
            payment_method: 'credit_card',
            card_number: '4111111111111111',
            card_holder: 'Test User',
            card_expiry: '12/2025',
            card_cvv: '123'
          });
          addResult('Payment Processing API', { 
            success: true, 
            data: paymentResponse.data,
            status: paymentResponse.status 
          });

          // Test 4: Check Payment Status
          const paymentId = paymentResponse.data.payment_id;
          try {
            const statusResponse = await API.get(`/payments/${paymentId}/status/`);
            addResult('Payment Status API', { 
              success: true, 
              data: statusResponse.data,
              status: statusResponse.status 
            });
          } catch (err) {
            addResult('Payment Status API', { 
              success: false, 
              error: err.message,
              status: err.response?.status 
            });
          }

        } catch (err) {
          addResult('Payment Processing API', { 
            success: false, 
            error: err.response?.data?.error || err.message,
            status: err.response?.status,
            details: err.response?.data 
          });
        }

      } catch (err) {
        addResult('Create Order API', { 
          success: false, 
          error: err.response?.data?.error || err.message,
          status: err.response?.status,
          details: err.response?.data 
        });
      }

      // Test 5: Test Decline Card
      try {
        // First create another order for decline test
        const declineOrderResponse = await API.post('/orders/', {
          from_cart: false,
          items: [{ book_id: 1, quantity: 1 }]
        });

        const declinePaymentResponse = await API.post('/payments/charge/', {
          order_id: declineOrderResponse.data.order_id,
          payment_method: 'credit_card',
          card_number: '4000000000000002', // Decline card
          card_holder: 'Decline User',
          card_expiry: '12/2025',
          card_cvv: '123'
        });
        
        // Check if payment was actually declined
        if (declinePaymentResponse.data.success === false || declinePaymentResponse.data.status === 'failed') {
          addResult('Decline Test API', { 
            success: true,
            data: declinePaymentResponse.data,
            status: declinePaymentResponse.status,
            note: 'Card properly declined as expected'
          });
        } else {
          addResult('Decline Test API', { 
            success: false,
            data: declinePaymentResponse.data,
            status: declinePaymentResponse.status,
            note: 'This should have been declined!'
          });
        }

      } catch (err) {
        addResult('Decline Test API', { 
          success: false, 
          error: err.response?.data?.error || err.message,
          status: err.response?.status,
          details: err.response?.data,
          note: 'Error during decline test'
        });
      }

    } catch (error) {
      addResult('General Error', { 
        success: false, 
        error: error.message 
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1>🧪 API Integration Test</h1>
      
      <div style={{ marginBottom: '30px' }}>
        <button
          onClick={testApis}
          disabled={loading}
          style={{
            padding: '15px 30px',
            backgroundColor: loading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold'
          }}
        >
          {loading ? '🔄 Testing APIs...' : '🚀 Run API Tests'}
        </button>
      </div>

      <div style={{ marginTop: '20px' }}>
        <h3>Test Results:</h3>
        {results.length === 0 && !loading && (
          <p style={{ color: '#666', fontStyle: 'italic' }}>
            Click "Run API Tests" to test backend integration
          </p>
        )}

        {results.map((result, idx) => (
          <div 
            key={idx}
            style={{ 
              marginBottom: '20px',
              padding: '20px',
              border: '1px solid #ddd',
              borderRadius: '8px',
              backgroundColor: result.result.success ? '#d4edda' : '#f8d7da'
            }}
          >
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '10px'
            }}>
              <h4 style={{ 
                margin: 0,
                color: result.result.success ? '#155724' : '#721c24'
              }}>
                {result.result.success ? '✅' : '❌'} {result.test}
              </h4>
              <small style={{ color: '#666' }}>{result.timestamp}</small>
            </div>

            {result.result.status && (
              <p><strong>Status:</strong> {result.result.status}</p>
            )}

            {result.result.note && (
              <p style={{ 
                fontStyle: 'italic',
                color: '#0056b3',
                marginBottom: '10px'
              }}>
                ℹ️ {result.result.note}
              </p>
            )}

            {result.result.error && (
              <div>
                <strong>Error:</strong>
                <pre style={{ 
                  backgroundColor: '#f8f9fa',
                  padding: '10px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  whiteSpace: 'pre-wrap'
                }}>
                  {result.result.error}
                </pre>
              </div>
            )}

            {result.result.data && (
              <details style={{ marginTop: '10px' }}>
                <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
                  📄 Response Data
                </summary>
                <pre style={{ 
                  backgroundColor: '#f8f9fa',
                  padding: '15px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  overflow: 'auto',
                  maxHeight: '300px'
                }}>
                  {JSON.stringify(result.result.data, null, 2)}
                </pre>
              </details>
            )}

            {result.result.details && (
              <details style={{ marginTop: '10px' }}>
                <summary style={{ cursor: 'pointer', fontWeight: 'bold' }}>
                  🔍 Error Details
                </summary>
                <pre style={{ 
                  backgroundColor: '#f8f9fa',
                  padding: '15px',
                  borderRadius: '4px',
                  fontSize: '12px',
                  overflow: 'auto',
                  maxHeight: '200px'
                }}>
                  {JSON.stringify(result.result.details, null, 2)}
                </pre>
              </details>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default ApiTester;
