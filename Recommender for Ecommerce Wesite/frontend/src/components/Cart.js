import React from 'react';

const Cart = () => {
  // Mock cart data
  const cartItems = [
    { id: 1, name: 'Product 1', price: 100, quantity: 2 },
    { id: 2, name: 'Product 2', price: 200, quantity: 1 },
  ];
  const total = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  return (
    <div style={{ padding: 24 }}>
      <h2>Cart</h2>
      <ul>
        {cartItems.map(item => (
          <li key={item.id}>
            {item.name} - ${item.price} x {item.quantity}
          </li>
        ))}
      </ul>
      <p><b>Total: ${total}</b></p>
      <button>Thanh toán</button>
    </div>
  );
};

export default Cart;