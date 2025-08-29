import React, { useState } from 'react';
import API from '../api';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await API.post('/users/login/', {
        email: email,
        password: password
      });

      console.log('Login response:', response.data);
      
      // Store both user info and JWT token
      localStorage.setItem('user', JSON.stringify(response.data.user));
      localStorage.setItem('token', response.data.token);
      
      setMessage('Login successful! Both session and JWT token created.');
      
      // Redirect or update UI as needed
      setTimeout(() => {
        window.location.href = '/payment'; // Redirect to payment page
      }, 1500);

    } catch (error) {
      const errorMessage = error.response?.data?.detail || 
                          error.response?.data?.error || 
                          error.message;
      setMessage(`Login failed: ${errorMessage}`);
      console.error('Login error:', error.response?.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 24, maxWidth: 400, margin: '0 auto' }}>
      <h2>Login to Your Account</h2>
      
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
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Email</label>
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
        
        <div style={{ marginBottom: 20 }}>
          <label style={{ display: 'block', marginBottom: 4, fontWeight: 'bold' }}>Password</label>
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

        <button 
          type="submit" 
          disabled={loading}
          style={{
            width: '100%',
            padding: 12,
            backgroundColor: loading ? '#6c757d' : '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: 4,
            fontSize: 16,
            fontWeight: 'bold',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;