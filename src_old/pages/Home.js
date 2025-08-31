import React from "react";
import PropTypes from "prop-types";
import ProductList from "../components/ProductList";
import Recommendation from "../components/Recommendation";


export default function Home({ query, category, onAddToCart }) {

  return (
    <>
      <section className="hero hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Chào mừng đến BookVerse</h1>
          <p className="hero-subtitle">Khám phá kho sách chọn lọc, giao diện thân thiện, mua sắm dễ dàng.</p>
          <button className="btn btn-primary hero-cta" onClick={() => window.scrollTo({ top: 400, behavior: "smooth" })}>
            Tìm sách ngay
          </button>
        </div>
      </section>

      <ProductList query={query} category={category} onAddToCart={onAddToCart} />
      <Recommendation category={category} />
    </>
  );
}

Home.propTypes = {
  query: PropTypes.string,
  category: PropTypes.string,
  onAddToCart: PropTypes.func.isRequired,
};

Home.defaultProps = {
  query: "",
  category: "all",
};