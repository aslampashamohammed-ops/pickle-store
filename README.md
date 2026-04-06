# 🥒 Pickle Store - Premium Homemade Indian Pickles

A complete, professional ecommerce website for an authentic homemade Indian pickle brand. Built with Flask, TailwindCSS, and vanilla JavaScript.

## 🎯 Features

### Frontend
- ✅ Professional, modern UI similar to Amazon, Flipkart, Blue Tokai
- ✅ Responsive mobile-first design
- ✅ Smooth animations and transitions
- ✅ Product filtering by taste, origin, price, and rating
- ✅ Advanced search functionality
- ✅ Product quick view modal
- ✅ Fully functional shopping cart
- ✅ Professional checkout page with order confirmation
- ✅ Customer testimonials section
- ✅ FAQ sections
- ✅ Newsletter signup
- ✅ Contact form

### Backend
- ✅ Flask REST API with CORS support
- ✅ SQLite database with 45+ authentic pickle products
- ✅ Cart management system
- ✅ Order processing
- ✅ Advanced product filtering and search
- ✅ Pagination support
- ✅ Session-based cart management

### Database
- ✅ Products table with 45+ varieties
- ✅ Cart tracking
- ✅ Order management
- ✅ Complete product information (price, rating, origin, taste, ingredients, etc.)

## 📁 Project Structure

```
pickle-store/
├── app.py                    # Flask application & API
├── database.db               # SQLite database (auto-generated)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── static/
│   ├── css/                 # Custom styles
│   ├── js/                  # JavaScript files
│   └── images/              # Product images
└── templates/
    ├── base.html            # Base template with navigation
    ├── index.html           # Homepage
    ├── products.html        # Products listing with filters
    ├── cart.html            # Shopping cart & checkout
    ├── about.html           # About us page
    └── contact.html         # Contact page
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
cd pickle-store
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 📦 Product Database

The app comes with **45+ authentic Indian pickles** including:

### Categories
- 🥭 Mango Pickles (Avakaya, Chhundo, Punjabi, Kerala varieties)
- 🌶️ Chilli Pickles (Green, Red, Garlic, Ginger)
- 🥕 Vegetable Pickles (Mixed, Carrot, Radish, Cauliflower, etc.)
- 🍋 Citrus Pickles (Lemon, Lime, Orange Peel)
- 🍎 Fruit Pickles (Amla, Papaya, Guava, Pomegranate)
- 🍤 Non-Vegetarian (Chicken, Fish, Prawn, Duck)
- 🎁 Gift Sets & Collections
- ✨ Specialty & Fusion Pickles

### Product Information
Each product includes:
- Name
- Price (₹100 - ₹1,300)
- Rating (4.3 - 5.0 stars)
- Review count
- Origin location
- Taste profile
- Spice level
- Ingredients
- Description
- Category

## 🔧 API Endpoints

### Products
- `GET /api/products` - Get all products with filtering & pagination
- `GET /api/products/<id>` - Get single product details
- `GET /api/filters` - Get available filter options
- `GET /api/search?q=<query>` - Search products

### Cart
- `GET /api/cart?session_id=<id>` - Get cart items
- `POST /api/cart` - Add product to cart
- `PUT /api/cart/<id>` - Update cart item quantity
- `DELETE /api/cart/<id>` - Remove item from cart

### Orders
- `POST /api/orders` - Create new order

## 🎨 UI/UX Features

### Design Elements
- Premium color scheme (Amber/Orange/Brown)
- Professional card-based layouts
- Smooth hover animations
- Responsive grid system
- Modern typography
- Soft shadows and rounded corners

### User Experience
- Sticky navigation bar
- Cart badge showing item count
- Quick product view modal
- Intuitive filtering system
- Pagination for products
- Form validation
- Order confirmation modal
- Success notifications

## 💾 Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    rating REAL,
    reviews_count INTEGER,
    origin TEXT,
    taste_profile TEXT,
    spice_level TEXT,
    ingredients TEXT,
    image_url TEXT,
    description TEXT,
    category TEXT,
    in_stock INTEGER,
    created_at TIMESTAMP
);
```

### Cart Table
```sql
CREATE TABLE cart (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    quantity INTEGER,
    session_id TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    customer_phone TEXT,
    customer_address TEXT,
    total_amount REAL,
    items TEXT (JSON),
    status TEXT,
    created_at TIMESTAMP
);
```

## 🌐 Deployment

### Deploying to Render

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Connect to Render**
- Go to https://render.com
- Click "New" → "Web Service"
- Connect your GitHub repository
- Set Build Command: `pip install -r requirements.txt`
- Set Start Command: `gunicorn app:app`
- Deploy

3. **Install gunicorn for production**
```bash
pip install gunicorn
pip freeze > requirements.txt
```

### Deploying to Heroku

1. **Install Heroku CLI**
2. **Create Procfile**
```
web: gunicorn app:app
```

3. **Deploy**
```bash
heroku create your-app-name
git push heroku main
```

## 🛠️ Technologies Used

### Frontend
- **HTML5** - Semantic markup
- **TailwindCSS** - Utility-first CSS framework
- **Vanilla JavaScript** - No dependencies, pure JS
- **Font Awesome** - Icons

### Backend
- **Python** - Backend language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin support
- **SQLite** - Database

### Tools
- **VS Code** - Development environment
- **Git** - Version control
- **GitHub** - Code repository

## 📱 Responsive Design

- **Mobile (< 640px)** - Single column, full width
- **Tablet (640px - 1024px)** - Two columns, optimized layout
- **Desktop (> 1024px)** - Three columns, full featured

## 🔐 Security Features

- Session-based cart management
- CSRF protection ready
- Form validation on both client and server
- CORS enabled for API access
- Input sanitization

## 📈 Performance

- Fast page load times
- Optimized database queries
- Pagination for large datasets
- Lazy loading animations
- Minimal CSS/JS

## 🎓 Learning Resources

This project demonstrates:
- ✅ Full-stack web development
- ✅ REST API design
- ✅ Database design & SQL
- ✅ Frontend state management
- ✅ Form handling & validation
- ✅ Session management
- ✅ Responsive design
- ✅ Modern CSS & animations

## 📝 License

This project is open source and available for educational and commercial use.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

For questions or issues:
- Email: support@picklestore.com
- GitHub Issues: Report problems here
- Contact form: Available on the website

## 🎉 Features to Enhance

Future improvements could include:
- User authentication & profiles
- Wishlist functionality
- Payment gateway integration
- Admin dashboard
- Inventory management
- Email notifications
- Reviews & ratings system
- Recommendation engine
- Multi-language support
- Analytics & reporting

## 📄 License

MIT License - feel free to use this for personal or commercial projects.

---

**Made with ❤️ for pickle lovers everywhere!**

🥒 Welcome to Pickle Store - Premium Homemade Indian Pickles 🥒
