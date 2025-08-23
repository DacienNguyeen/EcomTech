import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import Cart from './components/Cart';

const App = () => (
	<Router>
		<nav style={{ padding: 12, background: '#eee', marginBottom: 24 }}>
			<Link to="/" style={{ marginRight: 12 }}>Home</Link>
			<Link to="/products" style={{ marginRight: 12 }}>Products</Link>
			<Link to="/cart">Cart</Link>
		</nav>
		<Routes>
			<Route path="/" element={<Home />} />
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/products" element={<ProductList />} />
			<Route path="/products/:id" element={<ProductDetail />} />
			<Route path="/cart" element={<Cart />} />
		</Routes>
	</Router>
);

export default App;
