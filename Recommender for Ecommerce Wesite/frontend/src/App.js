import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import ProductList from './components/ProductList';
import ProductDetail from './components/ProductDetail';
import Cart from './components/Cart';
import Payment from './components/Payment';
import SandboxInfo from './components/SandboxInfo';
import ApiTester from './components/ApiTester';

const App = () => (
	<Router>
		<nav style={{ 
			padding: 16, 
			background: '#343a40', 
			marginBottom: 24,
			display: 'flex',
			alignItems: 'center',
			justifyContent: 'space-between'
		}}>
			<div>
				<Link to="/" style={{ 
					marginRight: 20, 
					color: 'white', 
					textDecoration: 'none',
					fontWeight: 'bold'
				}}>🏠 Home</Link>
				<Link to="/products" style={{ 
					marginRight: 20, 
					color: 'white', 
					textDecoration: 'none' 
				}}>🛍️ Products</Link>
				<Link to="/cart" style={{ 
					marginRight: 20, 
					color: 'white', 
					textDecoration: 'none' 
				}}>🛒 Cart</Link>
				<Link to="/payment" style={{ 
					marginRight: 20, 
					color: 'white', 
					textDecoration: 'none',
					backgroundColor: '#28a745',
					padding: '8px 16px',
					borderRadius: '4px'
				}}>💳 Payment</Link>
				<Link to="/sandbox" style={{ 
					marginRight: 20, 
					color: 'white', 
					textDecoration: 'none',
					backgroundColor: '#17a2b8',
					padding: '8px 16px',
					borderRadius: '4px'
				}}>🔧 Sandbox</Link>
				<Link to="/test" style={{ 
					color: 'white', 
					textDecoration: 'none',
					backgroundColor: '#6f42c1',
					padding: '8px 16px',
					borderRadius: '4px'
				}}>🧪 API Test</Link>
			</div>
			<div>
				<Link to="/login" style={{ 
					marginRight: 12, 
					color: 'white', 
					textDecoration: 'none' 
				}}>Login</Link>
				<Link to="/register" style={{ 
					color: 'white', 
					textDecoration: 'none' 
				}}>Register</Link>
			</div>
		</nav>
		<Routes>
			<Route path="/" element={<Home />} />
			<Route path="/login" element={<Login />} />
			<Route path="/register" element={<Register />} />
			<Route path="/products" element={<ProductList />} />
			<Route path="/products/:id" element={<ProductDetail />} />
			<Route path="/cart" element={<Cart />} />
			<Route path="/payment" element={<Payment />} />
			<Route path="/sandbox" element={<SandboxInfo />} />
			<Route path="/test" element={<ApiTester />} />
		</Routes>
	</Router>
);

export default App;
