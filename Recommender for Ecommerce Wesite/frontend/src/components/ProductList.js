import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../api';

const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addingToCart, setAddingToCart] = useState({});

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await API.get('/catalog/books/');
        console.log('API response:', res.data);
        // Handle both array and paginated response formats
        const productsData = Array.isArray(res.data) ? res.data : res.data.results || [];
        setProducts(productsData);
      } catch (err) {
        console.error('Fetch products error:', err.response?.data || err.message);
        setError('Failed to fetch products: ' + (err.response?.data?.detail || err.message));
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const handleAddToCart = async (bookId) => {
    setAddingToCart(prev => ({ ...prev, [bookId]: true }));
    try {
      await API.post('/cart/add/', { book_id: bookId, quantity: 1 });
      alert('Product added to cart!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to add to cart');
    } finally {
      setAddingToCart(prev => ({ ...prev, [bookId]: false }));
    }
  };

  if (loading) return <div>Loading products...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!Array.isArray(products)) {
    console.error('Products is not an array:', products);
    return <div style={{ color: 'red' }}>Invalid products data format</div>;
  }

  return (
    <div style={{ padding: 24 }}>
      <h2>Product List</h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '16px' }}>
        {products.map(product => (
          <div key={product.BookID} style={{ 
            border: '1px solid #ddd', 
            borderRadius: '8px', 
            padding: '16px',
            backgroundColor: '#f9f9f9'
          }}>
            <h3>
              <Link to={`/products/${product.BookID}`} style={{ textDecoration: 'none', color: '#333' }}>
                {product.Title}
              </Link>
            </h3>
            <p><strong>Price:</strong> ${product.Price}</p>
            <p><strong>Stock:</strong> {product.Stock}</p>
            {product.Description && <p><em>{product.Description.substring(0, 100)}...</em></p>}
            <button 
              onClick={() => handleAddToCart(product.BookID)}
              disabled={addingToCart[product.BookID] || product.Stock < 1}
              style={{
                backgroundColor: product.Stock < 1 ? '#ccc' : '#28a745',
                color: 'white',
                border: 'none',
                padding: '8px 16px',
                borderRadius: '4px',
                cursor: product.Stock < 1 ? 'not-allowed' : 'pointer'
              }}
            >
              {addingToCart[product.BookID] ? 'Adding...' : 
               product.Stock < 1 ? 'Out of Stock' : 'Add to Cart'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;