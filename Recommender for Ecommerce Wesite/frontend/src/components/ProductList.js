import React from 'react';
import { Link } from 'react-router-dom';

const mockProducts = [
  { id: 1, name: 'Product 1', price: 100 },
  { id: 2, name: 'Product 2', price: 200 },
];

const ProductList = () => {
  return (
    <div style={{ padding: 24 }}>
      <h2>Product List</h2>
      <ul>
        {mockProducts.map(p => (
          <li key={p.id}>
            <Link to={`/products/${p.id}`}>{p.name}</Link> - ${p.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;