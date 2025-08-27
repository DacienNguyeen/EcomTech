# E-commerce Website with Product Recommendation

A Django-based e-commerce platform with integrated recommendation system using collaborative filtering and content-based approaches.

## Database Setup

### MonsterASP MySQL Configuration

1. **Enable Remote Access** on MonsterASP control panel
2. **Update .env file** with your actual hostname:
   ```
   MYSQL_HOST=your-monsterasp-hostname
   ```

### Database Initialization

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Test database connection
python manage.py test_db

# Create and setup database tables
mysql -h your-host -u db26061 -p BookStore < ../database/schema.sql
mysql -h your-host -u db26061 -p BookStore < ../database/sample_data.sql

# Or use Django migrations (recommended)
python manage.py makemigrations
python manage.py migrate
```

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# MonsterASP MySQL Database
MYSQL_HOST=your-monsterasp-hostname
MYSQL_PORT=3306
MYSQL_DATABASE=BookStore
MYSQL_USER=db26061
MYSQL_PASSWORD=5Rt%_q7Jb6T+

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# CORS for frontend
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

## Running the Application

```bash
# Backend (Django)
cd backend
python manage.py runserver

# Frontend (React)
cd frontend
npm install
npm start
```

## Database Schema

The application uses the following main tables:
- `author` - Book authors
- `publisher` - Publishers
- `category` - Book categories  
- `book` - Product catalog
- `customer` - User accounts
- `orders` - Order management
- `orderdetail` - Order line items
- `payment` - Payment tracking
- `useractivity` - User behavior for recommendations

## API Endpoints

- `/api/v1/catalog/` - Product catalog
- `/api/v1/cart/` - Shopping cart
- `/api/v1/users/` - User management
- `/api/v1/recommendations/` - Recommendation engine
