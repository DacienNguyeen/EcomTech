import React from 'react';
import { useParams } from 'react-router-dom';

const ProductDetail = () => {
  const { id } = useParams();
  // Mock data
  const product = { id, name: `Product ${id}`, price: 100 * id, description: 'Mô tả sản phẩm...' };
  return (
    <div style={{ padding: 24 }}>
      <h2>{product.name}</h2>
      <p>Giá: ${product.price}</p>
      <p>{product.description}</p>
      <button>Thêm vào giỏ hàng</button>
    </div>
  );
};

export default ProductDetail;