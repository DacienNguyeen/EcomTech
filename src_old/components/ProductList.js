import React, { useMemo, useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";

export const BOOKS = [
  { id: "clean-code", title: "Clean Code", author: "Robert C. Martin", price: 320000, category: "tech", rating: 4.8, coverImage: "https://toidicodedao.com/wp-content/uploads/2015/03/71ambnhelil-e1552820007165.jpg", tags: ["code", "software"], description: "Nguyên tắc viết mã sạch, dễ bảo trì." },
  { id: "atomic-habits", title: "Atomic Habits", author: "James Clear", price: 180000, category: "selfhelp", rating: 4.9, coverImage: "https://m.media-amazon.com/images/I/81ANaVZk5LL.jpg", tags: ["habit", "productivity"], description: "Xây dựng thói quen nhỏ tạo thay đổi lớn." },
  { id: "the-alchemist", title: "The Alchemist", author: "Paulo Coelho", price: 150000, category: "novel", rating: 4.6, coverImage: "https://static.wixstatic.com/media/8cc233_da3154cf2cdd4e979a841903fb3cf770~mv2.jpg/v1/fill/w_1585,h_2400,al_c,q_90/The%20Alchemist%20cover.jpg", tags: ["novel", "journey"], description: "Hành trình tìm giấc mơ." },
  { id: "zero-to-one", title: "Zero to One", author: "Peter Thiel", price: 190000, category: "business", rating: 4.5, coverImage: "https://www.nxbtre.com.vn/Images/Book/nxbtre_full_09242020_032405.jpg", tags: ["startup", "innovation"], description: "Tư duy tạo giá trị mới." },
  { id: "you-dont-know-js", title: "You Don't Know JS Yet", author: "Kyle Simpson", price: 240000, category: "tech", rating: 4.7, coverImage: "https://m.media-amazon.com/images/I/71GsZGf3opL._UF1000,1000_QL80_.jpg", tags: ["js", "programming"], description: "Sâu về bản chất JavaScript." },
  { id: "design-patterns", title: "Design Patterns", author: "Erich Gamma", price: 350000, category: "tech", rating: 4.9, coverImage: "https://m.media-amazon.com/images/I/818eEdFC48L._UF1000,1000_QL80_.jpg", tags: ["design", "software"], description: "Các mẫu thiết kế phần mềm cổ điển." },
  { id: "deep-work", title: "Deep Work", author: "Cal Newport", price: 200000, category: "selfhelp", rating: 4.7, coverImage: "https://m.media-amazon.com/images/I/71din4TLubL._UF1000,1000_QL80_.jpg", tags: ["productivity", "focus"], description: "Làm việc tập trung để đạt hiệu quả tối đa." },
  { id: "1984", title: "1984", author: "George Orwell", price: 160000, category: "novel", rating: 4.8, coverImage: "https://m.media-amazon.com/images/I/71wANojhEKL._UF1000,1000_QL80_.jpg", tags: ["dystopian", "classic"], description: "Tiểu thuyết dystopian kinh điển." },
  { id: "lean-startup", title: "The Lean Startup", author: "Eric Ries", price: 220000, category: "business", rating: 4.6, coverImage: "https://m.media-amazon.com/images/I/81-QB7nDh4L.jpg", tags: ["startup", "business"], description: "Phương pháp khởi nghiệp tinh gọn." },
  { id: "sapiens", title: "Sapiens", author: "Yuval Noah Harari", price: 250000, category: "history", rating: 4.9, coverImage: "https://cdn1.fahasa.com/media/catalog/product/7/1/713jiomo3ul.jpg", tags: ["history", "anthropology"], description: "Lịch sử loài người từ thời kỳ đồ đá." },
  { id: "thinking-fast-and-slow", title: "Thinking, Fast and Slow", author: "Daniel Kahneman", price: 210000, category: "psychology", rating: 4.7, coverImage: "https://nhasachphuongnam.com/images/detailed/173/51oXKWrcYYL.jpg", tags: ["psychology", "decision-making"], description: "Cách chúng ta tư duy và ra quyết định." },
  { id: "pride-and-prejudice", title: "Pride and Prejudice", author: "Jane Austen", price: 140000, category: "novel", rating: 4.6, coverImage: "https://m.media-amazon.com/images/I/71Q1tPupKjL.jpg", tags: ["romance", "classic"], description: "Tiểu thuyết lãng mạn kinh điển." },
  { id: "the-power-of-habit", title: "The Power of Habit", author: "Charles Duhigg", price: 190000, category: "selfhelp", rating: 4.5, coverImage: "https://m.media-amazon.com/images/I/71wm29Etl4L._UF1000,1000_QL80_.jpg", tags: ["habit", "psychology"], description: "Sức mạnh của thói quen trong đời sống." },
  { id: "javascript-the-good-parts", title: "JavaScript: The Good Parts", author: "Douglas Crockford", price: 230000, category: "tech", rating: 4.6, coverImage: "https://m.media-amazon.com/images/I/7185IMvz88L._UF1000,1000_QL80_.jpg", tags: ["js", "programming"], description: "Những phần tinh túy của JavaScript." },
  { id: "the-great-gatsby", title: "The Great Gatsby", author: "F. Scott Fitzgerald", price: 130000, category: "novel", rating: 4.5, coverImage: "https://m.media-amazon.com/images/I/71FTb9X6wsL.jpg", tags: ["classic", "novel"], description: "Tiểu thuyết về giấc mơ Mỹ." },
  { id: "homo-deus", title: "Homo Deus", author: "Yuval Noah Harari", price: 260000, category: "history", rating: 4.8, coverImage: "https://m.media-amazon.com/images/I/71KBDP3mDfL._UF1000,1000_QL80_.jpg", tags: ["history", "future"], description: "Tương lai của loài người." },
  { id: "start-with-why", title: "Start with Why", author: "Simon Sinek", price: 200000, category: "business", rating: 4.7, coverImage: "https://m.media-amazon.com/images/I/71M1P287BjL.jpg", tags: ["leadership", "business"], description: "Tầm quan trọng của mục đích trong kinh doanh." },
  { id: "the-subtle-art", title: "The Subtle Art of Not Giving a F*ck", author: "Mark Manson", price: 170000, category: "selfhelp", rating: 4.6, coverImage: "https://cdn1.fahasa.com/media/catalog/product/1/_/1_67_1.jpg", tags: ["selfhelp", "mindset"], description: "Nghệ thuật sống tỉnh thức." },
  { id: "to-kill-a-mockingbird", title: "To Kill a Mockingbird", author: "Harper Lee", price: 150000, category: "novel", rating: 4.8, coverImage: "https://upload.wikimedia.org/wikipedia/commons/4/4f/To_Kill_a_Mockingbird_%28first_edition_cover%29.jpg", tags: ["classic", "social"], description: "Tiểu thuyết về công lý và phân biệt chủng tộc." },
  { id: "refactoring", title: "Refactoring", author: "Martin Fowler", price: 340000, category: "tech", rating: 4.8, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWIGUNKdGV4TdG7nsTqCBRt2vYYjwrmz_qSw&s", tags: ["code", "software"], description: "Cải thiện mã nguồn hiện có." },
  { id: "van-hoc-vn", title: "Sông Đông Êm Đềm", author: "Mikhail Sholokhov", price: 250000, category: "literature", rating: 4.7, coverImage: "https://upload.wikimedia.org/wikipedia/vi/a/af/MikhailSholokhov_AndQuietFlowsTheDon.gif", tags: ["van-hoc", "kinh-dien"], description: "Tiểu thuyết kinh điển về chiến tranh." },
  { id: "thieu-nhi-1", title: "Dế Mèn Phiêu Lưu Ký", author: "Tô Hoài", price: 120000, category: "children", rating: 4.6, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQnokNsUDPopTx9K3ZDgFtU74O-wk5OtAL9vA&s", tags: ["thieu-nhi", "viet-nam"], description: "Cuộc phiêu lưu của chú dế mèn." },
  { id: "lich-su-1", title: "Lịch Sử Việt Nam", author: "Nguyễn Khắc Viện", price: 200000, category: "history", rating: 4.8, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRAIBXw2bkClc5JKRbPI3_ZqBqVUVL3k_sGVw&s", tags: ["lich-su", "viet-nam"], description: "Tổng quan lịch sử dân tộc." },
  { id: "ngoai-ngu-1", title: "English Grammar in Use", author: "Raymond Murphy", price: 180000, category: "language", rating: 4.9, coverImage: "https://m.media-amazon.com/images/I/51a+XisfDsL._UF1000,1000_QL80_.jpg", tags: ["tieng-anh", "ngu-phap"], description: "Sách học ngữ pháp tiếng Anh." },
  { id: "khoa-hoc-1", title: "Vũ Trụ Trong Lòng Bàn Tay", author: "Christophe Galfard", price: 220000, category: "science", rating: 4.7, coverImage: "https://thebookland.vn/thumbnail_1200/TheUniverseinYourHand.jpg", tags: ["khoa-hoc", "vu-tru"], description: "Khám phá vũ trụ dễ hiểu." },
  { id: "tam-ly-1", title: "Nghệ Thuật Sống", author: "Dale Carnegie", price: 150000, category: "psychology", rating: 4.5, coverImage: "https://nhasachphuongnam.com/images/detailed/227/nghe-thuat-xu-the-tb-2022.jpg", tags: ["tam-ly", "phat-trien"], description: "Kỹ năng sống và giao tiếp." },
  { id: "kinh-te-1", title: "Kinh Tế Học Vui", author: "Steven Levitt", price: 190000, category: "economy", rating: 4.6, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQY2XfxIrvGcbuIVPfuJlmuFRqda5CsQNL4Ew&s", tags: ["kinh-te", "thuc-te"], description: "Kinh tế học qua ví dụ đời thường." },
  { id: "truyen-tranh-1", title: "Doraemon Tập 1", author: "Fujiko F. Fujio", price: 50000, category: "children", rating: 4.9, coverImage: "https://product.hstatic.net/1000376556/product/xhljijuw_9de22abba6a2407d87e202d773acda07_1024x1024.png", tags: ["truyen-tranh", "thieu-nhi"], description: "Cuộc phiêu lưu của Doraemon." },
  { id: "y-hoc-1", title: "Cơ Thể Con Người", author: "DK Publishing", price: 300000, category: "science", rating: 4.8, coverImage: "https://cdn1.fahasa.com/media/catalog/product/9/7/9780241617175.jpg", tags: ["y-hoc", "khoa-hoc"], description: "Hướng dẫn về cơ thể học." },
  { id: "du-lich-1", title: "Du Lịch Việt Nam", author: "Lonely Planet", price: 210000, category: "travel", rating: 4.7, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxLeRRxHMrKgbgji6MlX80UaA5wsj4UbSxQg&s", tags: ["du-lich", "huong-dan"], description: "Hướng dẫn du lịch các tỉnh." },
  { id: "python-crash-course", title: "Python Crash Course", author: "Eric Matthes", price: 280000, category: "tech", rating: 4.7, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSag-kXgJHszTxz-VShbPB1fqFdZalhm2gQg&s", tags: ["python", "programming"], description: "Khóa học Python cơ bản đến nâng cao." },
  { id: "mindset", title: "Mindset", author: "Carol S. Dweck", price: 190000, category: "selfhelp", rating: 4.6, coverImage: "https://nhasachphuongnam.com/images/detailed/143/81o--FP-hPL.jpg", tags: ["mindset", "growth"], description: "Tư duy phát triển thay đổi cuộc đời." },
  { id: "lord-of-the-rings", title: "The Lord of the Rings", author: "J.R.R. Tolkien", price: 300000, category: "novel", rating: 4.9, coverImage: "https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1566425108i/33.jpg", tags: ["fantasy", "classic"], description: "Hành trình huyền thoại của vành đai." },
  { id: "good-to-great", title: "Good to Great", author: "Jim Collins", price: 230000, category: "business", rating: 4.7, coverImage: "https://m.media-amazon.com/images/I/71LhjimPd8L._UF1000,1000_QL80_.jpg", tags: ["leadership", "business"], description: "Từ tốt đến vĩ đại trong kinh doanh." },
  { id: "guns-germs-steel", title: "Guns, Germs, and Steel", author: "Jared Diamond", price: 270000, category: "history", rating: 4.8, coverImage: "https://bizweb.dktcdn.net/100/326/228/products/gunsgermssteeljareddiamond.jpg?v=1540291210800", tags: ["history", "civilization"], description: "Nguyên nhân sự phát triển của các nền văn minh." },
  { id: "emotional-intelligence", title: "Emotional Intelligence", author: "Daniel Goleman", price: 200000, category: "psychology", rating: 4.6, coverImage: "https://m.media-amazon.com/images/I/71z-XQzRclL._UF1000,1000_QL80_.jpg", tags: ["eq", "psychology"], description: "Trí tuệ cảm xúc trong cuộc sống." },
  { id: "brief-history-time", title: "A Brief History of Time", author: "Stephen Hawking", price: 220000, category: "science", rating: 4.9, coverImage: "https://m.media-amazon.com/images/I/91ebghaV-eL._UF1000,1000_QL80_.jpg", tags: ["physics", "universe"], description: "Lịch sử ngắn gọn về thời gian và vũ trụ." },
  { id: "charlie-and-chocolate", title: "Charlie and the Chocolate Factory", author: "Roald Dahl", price: 110000, category: "children", rating: 4.7, coverImage: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwBPrEP9K087q1BAbrfrhTPO9ORtx0UTZ9JA&s", tags: ["children", "fantasy"], description: "Cuộc phiêu lưu trong nhà máy sô-cô-la." },
  { id: "spanish-for-dummies", title: "Spanish for Dummies", author: "Susana Wald", price: 160000, category: "language", rating: 4.5, coverImage: "https://m.media-amazon.com/images/I/61sUWEl2QIL._UF1000,1000_QL80_.jpg", tags: ["spanish", "language"], description: "Học tiếng Tây Ban Nha cơ bản." },
  { id: "freakonomics", title: "Freakonomics", author: "Steven D. Levitt", price: 180000, category: "economy", rating: 4.6, coverImage: "https://m.media-amazon.com/images/I/71uGp5GrqkL._UF1000,1000_QL80_.jpg", tags: ["economy", "data"], description: "Kinh tế học qua các câu chuyện độc đáo." },
  { id: "lonely-planet-thailand", title: "Lonely Planet Thailand", author: "Lonely Planet", price: 250000, category: "travel", rating: 4.8, coverImage: "https://m.media-amazon.com/images/I/71vzV6XZRRL._UF1000,1000_QL80_.jpg", tags: ["travel", "guide"], description: "Hướng dẫn du lịch Thái Lan." },
  { id: "crime-and-punishment", title: "Crime and Punishment", author: "Fyodor Dostoevsky", price: 200000, category: "literature", rating: 4.9, coverImage: "https://m.media-amazon.com/images/I/71O2XIytdqL._UF1000,1000_QL80_.jpg", tags: ["classic", "literature"], description: "Tác phẩm kinh điển về tội lỗi và trừng phạt." },
];

export function formatVND(n) { return n.toLocaleString("vi-VN") + "₫"; }

export default function ProductList({ query = "", category = "all", onAddToCart }) {
  const navigate = useNavigate();
  const [sort, setSort] = useState("popular");
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const itemsPerPage = 8;

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 500);
    return () => clearTimeout(timer);
  }, [query, category, sort, page]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    let arr = BOOKS.filter(b => 
      (category === "all" || b.category === category) && 
      (q === "" || b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q) || b.tags.some(t => t.includes(q)))
    );
    if (sort === "price-asc") arr.sort((a, b) => a.price - b.price);
    if (sort === "price-desc") arr.sort((a, b) => b.price - a.price);
    if (sort === "rating") arr.sort((a, b) => b.rating - a.rating);
    return arr;
  }, [query, category, sort]);

  const paginated = useMemo(() => {
    const start = (page - 1) * itemsPerPage;
    return filtered.slice(start, start + itemsPerPage);
  }, [filtered, page]);

  const totalPages = Math.ceil(filtered.length / itemsPerPage);

  if (loading) {
    return <div className="loading">Đang tải...</div>;
  }

  return (
    <section>
      <div className="product-header">
        <h2>Sách nổi bật</h2>
        <div className="spacer" />
        <select value={sort} onChange={e => setSort(e.target.value)} className="input sort-select">
          <option value="popular">Phổ biến</option>
          <option value="rating">Đánh giá cao</option>
          <option value="price-asc">Giá tăng dần</option>
          <option value="price-desc">Giá giảm dần</option>
        </select>
      </div>

      <div className="grid cols-4">
        {paginated.length > 0 ? (
          paginated.map(b => (
            <article key={b.id} className="card product-card" aria-label={b.title}>
              <img src={b.coverImage} alt={b.title} className="product-image" loading="lazy" />
              <div className="card-body">
                <Link to={`/product/${b.id}`} className="product-title">{b.title}</Link>
                <div className="muted product-author">{b.author}</div>
                <div className="product-footer">
                  <div className="price">{formatVND(b.price)}</div>
                  <div className="product-actions">
                    <button className="btn" onClick={() => navigate(`/product/${b.id}`)}>Chi tiết</button>
                    <button className="btn btn-primary" onClick={() => onAddToCart(b, 1)}>Thêm</button>
                  </div>
                </div>
              </div>
            </article>
          ))
        ) : (
          <div className="muted no-results">Không có kết quả phù hợp.</div>
        )}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button 
            className="btn" 
            onClick={() => setPage(p => Math.max(1, p - 1))} 
            disabled={page === 1}
          >
            Trước
          </button>
          <span>Trang {page} / {totalPages}</span>
          <button 
            className="btn" 
            onClick={() => setPage(p => Math.min(totalPages, p + 1))} 
            disabled={page === totalPages}
          >
            Tiếp
          </button>
        </div>
      )}
    </section>
  );
}