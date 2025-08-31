import React from 'react';

const ProductModal = ({ product, onClose, onAddToCart }) => {
  if (!product) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        
        <div className="modal-body">
          <div className="modal-image">
            <img src={product.coverImage || product.image_url} alt={product.title} />
          </div>
          
          <div className="modal-info">
            <h2>{product.title}</h2>
            <p className="author">Tác giả: {product.author}</p>
            <p className="price">{(product.price || 0).toLocaleString('vi-VN')}đ</p>
            <p className="description">{product.description}</p>
            
            <div className="modal-actions">
              <button 
                className="btn btn-primary" 
                onClick={() => {
                  onAddToCart(product);
                  onClose();
                }}
              >
                Thêm vào giỏ hàng
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductModal;
