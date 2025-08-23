import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ padding: 24 }}>
      <h1>Welcome to E-commerce Website</h1>
      <nav style={{ marginBottom: 16 }}>
        <Link to="/login" style={{ marginRight: 12 }}>Login</Link>
        <Link to="/register" style={{ marginRight: 12 }}>Register</Link>
        <Link to="/products">Products</Link>
      </nav>
      <p>Trang chủ demo cho hệ thống thương mại điện tử.</p>
    </div>
  );
};

export default Home;