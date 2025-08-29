import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ padding: 24, maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', marginBottom: '40px', color: '#343a40' }}>
        🛍️ E-commerce Payment Demo
      </h1>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '30px',
        marginBottom: '40px' 
      }}>
        {/* Payment Demo Card */}
        <div style={{ 
          padding: '30px', 
          border: '2px solid #28a745', 
          borderRadius: '12px',
          backgroundColor: '#f8fff8',
          textAlign: 'center'
        }}>
          <h2 style={{ color: '#28a745', marginBottom: '20px' }}>💳 Payment System</h2>
          <p style={{ marginBottom: '20px', color: '#666' }}>
            Test our complete payment sandbox with multiple card types, 
            success/decline scenarios, and webhook simulation.
          </p>
          <Link 
            to="/payment" 
            style={{ 
              display: 'inline-block',
              padding: '12px 24px',
              backgroundColor: '#28a745',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Test Payment →
          </Link>
        </div>

        {/* Sandbox Info Card */}
        <div style={{ 
          padding: '30px', 
          border: '2px solid #17a2b8', 
          borderRadius: '12px',
          backgroundColor: '#f0fbff',
          textAlign: 'center'
        }}>
          <h2 style={{ color: '#17a2b8', marginBottom: '20px' }}>🔧 Sandbox Tools</h2>
          <p style={{ marginBottom: '20px', color: '#666' }}>
            View test card numbers, payment methods, API endpoints,
            and simulate webhook events for testing.
          </p>
          <Link 
            to="/sandbox" 
            style={{ 
              display: 'inline-block',
              padding: '12px 24px',
              backgroundColor: '#17a2b8',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Sandbox Info →
          </Link>
        </div>

        {/* Products Card */}
        <div style={{ 
          padding: '30px', 
          border: '2px solid #6f42c1', 
          borderRadius: '12px',
          backgroundColor: '#faf9ff',
          textAlign: 'center'
        }}>
          <h2 style={{ color: '#6f42c1', marginBottom: '20px' }}>🛍️ Product Catalog</h2>
          <p style={{ marginBottom: '20px', color: '#666' }}>
            Browse our demo product catalog, add items to cart,
            and proceed to checkout with payment processing.
          </p>
          <Link 
            to="/products" 
            style={{ 
              display: 'inline-block',
              padding: '12px 24px',
              backgroundColor: '#6f42c1',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            View Products →
          </Link>
        </div>
      </div>

      {/* Features */}
      <div style={{ 
        padding: '30px', 
        backgroundColor: '#f8f9fa', 
        borderRadius: '12px',
        marginBottom: '30px'
      }}>
        <h3 style={{ textAlign: 'center', marginBottom: '30px', color: '#343a40' }}>
          🚀 Payment Features Demo
        </h3>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '20px' 
        }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: '10px' }}>✅</div>
            <h4>Success Scenarios</h4>
            <p>Test successful payments with Visa, Mastercard</p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: '10px' }}>❌</div>
            <h4>Decline Testing</h4>
            <p>Insufficient funds, expired cards, CVC errors</p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: '10px' }}>🔄</div>
            <h4>Webhook Events</h4>
            <p>Simulate payment webhooks and status updates</p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '32px', marginBottom: '10px' }}>💰</div>
            <h4>Refund Processing</h4>
            <p>Full and partial refund capabilities</p>
          </div>
        </div>
      </div>

      {/* Quick Start */}
      <div style={{ 
        textAlign: 'center',
        padding: '30px',
        border: '1px solid #dee2e6',
        borderRadius: '8px'
      }}>
        <h3 style={{ marginBottom: '20px' }}>🚀 Quick Start</h3>
        <div style={{ fontSize: '16px', color: '#666', lineHeight: '1.6' }}>
          <p>1. Click <strong>Payment</strong> to test payment processing</p>
          <p>2. Use test card numbers provided in <strong>Sandbox</strong></p>
          <p>3. Try different scenarios: success, decline, webhooks</p>
          <p>4. Check payment status and simulate refunds</p>
        </div>
      </div>
    </div>
  );
};

export default Home;