import React, { useState } from 'react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Gọi API đăng nhập
    alert(`Đăng nhập với: ${username}`);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={{ maxWidth: 300 }}>
        <div style={{ marginBottom: 12 }}>
          <label>Username</label>
          <input type="text" value={username} onChange={e => setUsername(e.target.value)} required style={{ width: '100%' }} />
        </div>
        <div style={{ marginBottom: 12 }}>
          <label>Password</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%' }} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;