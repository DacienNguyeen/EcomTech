import React, { useState } from 'react';
import API from '../api';

const Register = () => {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const API_BASE = 'http://127.0.0.1:8000/api/v1';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await API.post(`/users/register/`, {
        full_name: fullName,
        email: email,
        password: password,
        phone: phone,
        address: address
      });

      setMessage('Registration successful! Logging you in...');
      console.log('Registration response:', response.data);

      // Auto-login to create session and JWT
      try {
        const loginResp = await API.post('/users/login/', {
          email: email,
          password: password
        });
        console.log('Auto-login response:', loginResp.data);
        
        // Store both user info and JWT token
        localStorage.setItem('user', JSON.stringify(loginResp.data.user));
        localStorage.setItem('token', loginResp.data.token);
        
        setMessage('Registration and login successful! Redirecting...');
        setTimeout(() => { window.location.href = '/payment'; }, 1000);
      } catch (loginErr) {
        console.error('Auto-login failed:', loginErr.response?.data || loginErr.message);
        setMessage('Registration succeeded but automatic login failed. Please login manually.');
      }

      // Clear form
      setFullName('');
      setEmail('');
      setPassword('');
      setPhone('');
      setAddress('');
    } catch (error) {
      // Detailed error logging
      console.error('Registration error full:', error);
      const errorMessage = error.response?.data?.detail ||
                          error.response?.data?.error ||
                          JSON.stringify(error.response?.data) ||
                          error.message;
      setMessage(`Registration failed: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 500, margin: '0 auto' }}>
      <h2>Register New Account</h2>
      
      {message && (
        <div style={{ 
          padding: 12, 
          marginBottom: 16,
          backgroundColor: message.includes('successful') ? '#d4edda' : '#f8d7da',
          color: message.includes('successful') ? '#155724' : '#721c24',
          border: `1px solid ${message.includes('successful') ? '#c3e6cb' : '#f5c6cb'}`,
          borderRadius: 4
        }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Full Name *</label>
          <input 
            type="text" 
            value={fullName} 
            onChange={e => setFullName(e.target.value)} 
            required 
            style={{ 
              width: '100%', 
              padding: 8, 
              border: '1px solid #ccc', 
              borderRadius: 4,
              fontSize: 14
            }} 
          />
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Email *</label>
          <input 
            type="email" 
            value={email} 
            onChange={e => setEmail(e.target.value)} 
            required 
            style={{ 
              width: '100%', 
              padding: 8, 
              border: '1px solid #ccc', 
              borderRadius: 4,
              fontSize: 14
            }} 
          />
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Password *</label>
          <input 
            type="password" 
            value={password} 
            onChange={e => setPassword(e.target.value)} 
            required 
            style={{ 
              width: '100%', 
              padding: 8, 
              border: '1px solid #ccc', 
              borderRadius: 4,
              fontSize: 14
            }} 
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Phone</label>
          <input 
            type="text" 
            value={phone} 
            onChange={e => setPhone(e.target.value)} 
            style={{ 
              width: '100%', 
              padding: 8, 
              border: '1px solid #ccc', 
              borderRadius: 4,
              fontSize: 14
            }} 
          />
        </div>

        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Address</label>
          <textarea 
            value={address} 
            onChange={e => setAddress(e.target.value)} 
            rows={3}
            style={{ 
              width: '100%', 
              padding: 8, 
              border: '1px solid #ccc', 
              borderRadius: 4,
              fontSize: 14,
              resize: 'vertical'
            }} 
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          style={{
            width: '100%',
            padding: 12,
            backgroundColor: loading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            fontSize: 16,
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Registering...' : 'Register Account'}
        </button>
      </form>
    </div>
  );
};

export default Register;