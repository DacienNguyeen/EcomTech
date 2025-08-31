// Cart.js
import React, { useMemo } from "react";
import { Link } from "react-router-dom";
import { FaTrash, FaPlus, FaMinus } from "react-icons/fa";
import Recommendation from "./Recommendation";
import { BOOKS } from "./ProductList";

function formatVND(n) {
  return n.toLocaleString("vi-VN") + "₫";
}

export default function Cart({ items, total, onInc, onDec, onRemove, onClear }) {
  const bestSellers = useMemo(() => {
    return BOOKS.sort((a, b) => b.rating - a.rating).slice(0, 8);
  }, []);

  return (
    <section className="container">
      <h1>Giỏ hàng</h1>

      {items.length === 0 && (
        <div className="muted" style={{ padding: "var(--spacing-md)" }}>
          Giỏ hàng trống. Hãy thêm sách bạn thích.
        </div>
      )}

      <div className="cart-layout">
        <div className="cart-items">
          {items.map((it) => (
            <div key={it.BookID || it.id} className="card cart-item">
              <img src={it.coverImage || it.ImageURL} alt={it.title || it.Title} className="cart-image" />
              <div className="cart-details">
                <div style={{ fontWeight: 700 }}>{it.title || it.Title}</div>
                <div className="muted" style={{ fontSize: 13 }}>
                  {formatVND(it.price || it.Price)}
                </div>
                <div className="quantity-controls">
                  <button className="btn" onClick={() => onDec(it.BookID || it.id)}>
                    <FaMinus />
                  </button>
                  <div aria-live="polite">{it.quantity}</div>
                  <button className="btn" onClick={() => onInc(it.id)}>
                    <FaPlus />
                  </button>
                </div>
              </div>
              <div className="cart-actions">
                <div className="price">{formatVND(it.price * it.quantity)}</div>
                <button
                  className="btn btn-danger"
                  onClick={() => onRemove(it.id)}
                >
                  <FaTrash /> Xóa
                </button>
              </div>
            </div>
          ))}
        </div>

        <aside className="cart-summary">
          <div className="card-body">
            <div className="summary-row">
              <span>Tạm tính</span>
              <strong>{formatVND(total)}</strong>
            </div>
            <div className="summary-row">
              <span>Phí vận chuyển</span>
              <span className="muted">Miễn phí</span>
            </div>
            <div className="summary-total">
              <span>Tổng</span>
              <span className="price">{formatVND(total)}</span>
            </div>
            <div className="summary-actions" style={{ textAlign: "center" }}>
              <Link
                to="/checkout"
                className="btn btn-primary"
                style={{ textDecoration: "none" }}
                disabled={items.length === 0}
              >
                Thanh toán
              </Link>
              <button
                className="btn"
                onClick={onClear}
                disabled={items.length === 0}
              >
                Xóa giỏ
              </button>
            </div>
          </div>
        </aside>
      </div>

      <div className="cart-info">
        <Recommendation title="Sách được mua nhiều" items={bestSellers} />
      </div>
    </section>
  );
}