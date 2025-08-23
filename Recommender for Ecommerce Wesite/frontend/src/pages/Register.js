import React, { useState } from 'react';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Gọi API đăng ký
    alert(`Đăng ký với: ${username}, ${email}`);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: 300 }}>
        <div style={{ marginBottom: 12 }}>
          <label>Username</label>
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} required style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Email</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%' }} />
        </div>
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;