import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import API from '../api';

const ProductDetail = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addingToCart, setAddingToCart] = useState(false);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await API.get(`/catalog/books/${id}/`);
        setProduct(res.data);
      } catch (err) {
        setError('Failed to fetch product');
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  const handleAddToCart = async () => {
    setAddingToCart(true);
    try {
      await API.post('/cart/add/', { book_id: Number(id), quantity });
      alert(`Added ${quantity} item(s) to cart!`);
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to add to cart');
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) return <div>Loading product...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!product) return <div>Product not found</div>;

  return (
    <div style={{ padding: 24 }}>
      <h2>{product.Title}</h2>
      <p><strong>Price:</strong> ${product.Price}</p>
      <p><strong>Stock:</strong> {product.Stock}</p>
      <p><strong>Author ID:</strong> {product.AuthorID}</p>
      <p><strong>Category ID:</strong> {product.CategoryID}</p>
      <p><strong>Publisher ID:</strong> {product.PublisherID}</p>
      {product.Description && <p><strong>Description:</strong> {product.Description}</p>}
      {product.PublicationDate && <p><strong>Publication Date:</strong> {product.PublicationDate}</p>}
      
      <div style={{ marginTop: '20px' }}>
        <label>Quantity: </label>
        <input
          type="number"
          min="1"
          max={product.Stock}
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
          style={{ width: '60px', marginRight: '10px' }}
          disabled={addingToCart || product.Stock < 1}
        />
        <button 
          onClick={handleAddToCart}
          disabled={addingToCart || product.Stock < 1}
          style={{
            backgroundColor: product.Stock < 1 ? '#ccc' : '#28a745',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
            cursor: product.Stock < 1 ? 'not-allowed' : 'pointer'
          }}
        >
          {addingToCart ? 'Adding...' : 
           product.Stock < 1 ? 'Out of Stock' : 'Add to Cart'}
        </button>
      </div>
    </div>
  );
};

export default ProductDetail;