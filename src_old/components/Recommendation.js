// Recommendation.js
import React, { useMemo, useRef } from "react";
import { Link } from "react-router-dom";
import { BOOKS } from "./ProductList";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";
import PropTypes from "prop-types";

export default function Recommendation({ current = null, category = "all", title = "Có thể bạn sẽ thích", items = null }) {
  const carouselRef = useRef(null);

  const recItems = useMemo(() => {
    if (items) return items;
    let filtered = BOOKS.filter(b => b.id !== (current?.id || ""));
    if (current) {
      const sameCategory = filtered.filter(b => b.category === current.category);
      const others = filtered.filter(b => b.category !== current.category);
      filtered = [...sameCategory, ...others].slice(0, 8);
    } else if (category !== "all") {
      filtered = filtered.filter(b => b.category === category).slice(0, 8);
    } else {
      filtered = filtered.sort(() => Math.random() - 0.5).slice(0, 8);
    }
    return filtered;
  }, [current, category, items]);

  const scrollLeft = () => {
    if (carouselRef.current) {
      carouselRef.current.scrollBy({ left: -200, behavior: "smooth" });
    }
  };

  const scrollRight = () => {
    if (carouselRef.current) {
      carouselRef.current.scrollBy({ left: 200, behavior: "smooth" });
    }
  };

  return (
    <section className="recommendation">
      <h3 className="recommendation-title">{title}</h3>
      <div className="carousel-wrapper">
        <button className="carousel-btn carousel-prev" onClick={scrollLeft} aria-label="Previous">
          <FaChevronLeft />
        </button>
        <div className="carousel" ref={carouselRef}>
          <div className="carousel-inner">
            {recItems.map(b => (
              <Link to={`/product/${b.id}`} key={b.id} className="card rec-card">
                <img src={b.coverImage} alt={b.title} className="rec-image" loading="lazy" />
                <div className="card-body">
                  <div className="rec-title">{b.title}</div>
                  <div className="muted rec-rating">★ {b.rating}</div>
                  <div className="muted rec-author">{b.author}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
        <button className="carousel-btn carousel-next" onClick={scrollRight} aria-label="Next">
          <FaChevronRight />
        </button>
      </div>
    </section>
  );
}

Recommendation.propTypes = {
  current: PropTypes.shape({
    id: PropTypes.string.isRequired,
    category: PropTypes.string.isRequired,
  }),
  category: PropTypes.string,
  title: PropTypes.string,
  items: PropTypes.array
};