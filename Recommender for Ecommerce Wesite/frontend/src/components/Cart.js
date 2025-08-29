import React, { useEffect, useState } from 'react';
import API from '../api';

const Cart = () => {
  const [cart, setCart] = useState({ items: [], total_items: 0, total_amount: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addBookId, setAddBookId] = useState('');
  const [addQuantity, setAddQuantity] = useState(1);
  const [actionLoading, setActionLoading] = useState(false);

  // Fetch cart from backend
  const fetchCart = async () => {
    setLoading(true);
    try {
      const res = await API.get('/cart/');
      setCart(res.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch cart');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  // Add item to cart
  const handleAddToCart = async () => {
    if (!addBookId) return;
    setActionLoading(true);
    try {
      await API.post('/cart/add/', { book_id: Number(addBookId), quantity: Number(addQuantity) });
      setAddBookId('');
      setAddQuantity(1);
      fetchCart();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add item');
    } finally {
      setActionLoading(false);
    }
  };

  // Update item quantity
  const handleUpdateQuantity = async (book_id, quantity) => {
    setActionLoading(true);
    try {
      await API.patch(`/cart/items/${book_id}/`, { quantity });
      fetchCart();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update item');
    } finally {
      setActionLoading(false);
    }
  };

  // Remove item
  const handleRemove = async (book_id) => {
    setActionLoading(true);
    try {
      await API.delete(`/cart/items/${book_id}/remove/`);
      fetchCart();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to remove item');
    } finally {
      setActionLoading(false);
    }
  };

  // Clear cart
  const handleClearCart = async () => {
    setActionLoading(true);
    try {
      await API.delete('/cart/clear/');
      fetchCart();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to clear cart');
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) return <div>Loading cart...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: 24 }}>
      <h2>Your Cart</h2>
      {cart.items.length === 0 ? (
        <div>Your cart is empty.</div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: 16 }}>
          <thead>
            <tr>
              <th style={{ border: '1px solid #ccc', padding: 8 }}>Book</th>
              <th style={{ border: '1px solid #ccc', padding: 8 }}>Price</th>
              <th style={{ border: '1px solid #ccc', padding: 8 }}>Quantity</th>
              <th style={{ border: '1px solid #ccc', padding: 8 }}>Subtotal</th>
              <th style={{ border: '1px solid #ccc', padding: 8 }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {cart.items.map(item => (
              <tr key={item.book_id}>
                <td style={{ border: '1px solid #ccc', padding: 8 }}>{item.title}</td>
                <td style={{ border: '1px solid #ccc', padding: 8 }}>${item.price}</td>
                <td style={{ border: '1px solid #ccc', padding: 8 }}>
                  <input
                    type="number"
                    min="1"
                    value={item.quantity}
                    onChange={e => handleUpdateQuantity(item.book_id, Number(e.target.value))}
                    style={{ width: 60 }}
                    disabled={actionLoading}
                  />
                </td>
                <td style={{ border: '1px solid #ccc', padding: 8 }}>${item.subtotal}</td>
                <td style={{ border: '1px solid #ccc', padding: 8 }}>
                  <button onClick={() => handleRemove(item.book_id)} disabled={actionLoading}>Remove</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div style={{ marginBottom: 16 }}>
        <b>Total Items:</b> {cart.total_items} <br />
        <b>Total Amount:</b> ${cart.total_amount}
      </div>

      <button onClick={handleClearCart} disabled={actionLoading || cart.items.length === 0} style={{ marginRight: 16 }}>
        Clear Cart
      </button>

      <h3>Add Product to Cart</h3>
      <div style={{ marginBottom: 16 }}>
        <input
          type="number"
          placeholder="Book ID"
          value={addBookId}
          onChange={e => setAddBookId(e.target.value)}
          style={{ width: 100, marginRight: 8 }}
          disabled={actionLoading}
        />
        <input
          type="number"
          min="1"
          value={addQuantity}
          onChange={e => setAddQuantity(e.target.value)}
          style={{ width: 60, marginRight: 8 }}
          disabled={actionLoading}
        />
        <button onClick={handleAddToCart} disabled={actionLoading || !addBookId}>Add to Cart</button>
      </div>
    </div>
  );
};

export default Cart;