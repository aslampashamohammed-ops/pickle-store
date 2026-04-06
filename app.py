"""
Pickle Store - Professional E-Commerce Application
A complete Flask-based ecommerce platform for premium homemade Indian pickles
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)
CORS(app)

# Database configuration
DATABASE = 'database.db'

def get_db():
    """Get database connection"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@contextmanager
def get_db_context():
    """Context manager for database connections"""
    db = get_db()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def init_db():
    """Initialize database with schema"""
    with get_db_context() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                rating REAL NOT NULL DEFAULT 4.5,
                reviews_count INTEGER NOT NULL DEFAULT 0,
                origin TEXT NOT NULL,
                taste_profile TEXT NOT NULL,
                spice_level TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                image_url TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                in_stock INTEGER NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 1,
                session_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products(id),
                UNIQUE(product_id, session_id)
            );
            
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                customer_address TEXT NOT NULL,
                total_amount REAL NOT NULL,
                items TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')

def seed_products():
    """Seed database with 45 authentic Indian pickle products"""
    products = [
        # Mango Pickles
        ('Andhra Avakaya Mango Pickle', 299, 4.8, 124, 'Andhra Pradesh', 'Complex & Spicy', 'Extra Hot', 'Raw Mango, Chilli, Turmeric, Salt, Mustard Oil', 'mango', 'Classic Andhra Pradesh preparation with raw mangoes, red chillies, and traditional spices. Tangy and fiercely spicy with authentic flavor.', 'Mango'),
        ('Punjabi Mango Pickle', 279, 4.6, 98, 'Punjab', 'Sweet & Tangy', 'Medium', 'Mango, Sugar, Chilli, Salt, Fenugreek', 'mango', 'Traditional Punjabi sweet mango pickle with balance of sweetness and tanginess. Perfect with Indian breads and rice.', 'Mango'),
        ('Gujarati Chhundo Sweet Mango Pickle', 319, 4.9, 156, 'Gujarat', 'Sweet', 'Mild', 'Mango, Jaggery, Turmeric, Salt, Oil', 'mango', 'Legendary sweet mango pickle from Gujarat. Made with jaggery and slow-cooked for authentic taste.', 'Mango'),
        ('Kerala Kadumanga Mango Pickle', 349, 4.7, 89, 'Kerala', 'Tangy & Spicy', 'Hot', 'Raw Mango, Turmeric, Chilli, Coconut Oil', 'mango', 'South Indian specialty with coconut oil and traditional Kerala spices. Distinctly tangy and aromatic.', 'Mango'),
        ('Lakhanpal National Mango Pickle', 269, 4.5, 112, 'Uttar Pradesh', 'Spicy & Tangy', 'Medium-Hot', 'Mango, Chilli, Fenugreek, Salt, Oil', 'mango', 'Traditional North Indian mango pickle with perfect balance of spices. Sets high standard for taste.', 'Mango'),
        ('Raw Mango Pickle with Garlic', 289, 4.6, 105, 'Rajasthan', 'Spicy', 'Extra Hot', 'Raw Mango, Garlic, Chilli, Turmeric, Salt', 'mango', 'Fiery mango pickle infused with fresh garlic. Strong, bold flavors for adventurous palates.', 'Mango'),
        
        # Chilli & Spice Pickles
        ('Green Chilli Pickle', 229, 4.7, 167, 'Andhra Pradesh', 'Spicy', 'Extra Hot', 'Green Chilli, Turmeric, Salt, Mustard Oil', 'chilli', 'Intense green chilli pickle with aromatic mustard oil. A staple in South Indian households.', 'Chilli'),
        ('Red Chilli Pickle', 239, 4.6, 142, 'Telangana', 'Very Spicy', 'Extra Hot', 'Red Chilli, Salt, Turmeric, Garlic, Oil', 'chilli', 'Fiery red chilli pickle with whole chillies. Perfect for those who love extreme heat.', 'Chilli'),
        ('Ginger Pickle', 259, 4.5, 98, 'Kerala', 'Spicy & Warm', 'Medium', 'Fresh Ginger, Chilli, Turmeric, Salt, Oil', 'ginger', 'Aromatic ginger pickle with warming spices. Great for digestion and adds zing to meals.', 'Spice'),
        ('Garlic Pickle', 249, 4.8, 134, 'Maharashtra', 'Pungent & Spicy', 'Medium-Hot', 'Fresh Garlic, Chilli, Turmeric, Salt, Oil', 'garlic', 'Bold garlic pickle with potent aroma and taste. A Chinese-inspired Indian twist on traditional recipes.', 'Spice'),
        ('Turmeric & Chilli Pickle', 219, 4.4, 87, 'West Bengal', 'Spicy', 'Medium-Hot', 'Turmeric Root, Chilli, Salt, Oil', 'turmeric', 'Golden turmeric pickle with health benefits. warming spices for immunity and wellness.', 'Spice'),
        ('Fenugreek (Methi) Pickle', 239, 4.5, 76, 'Rajasthan', 'Bitter & Spicy', 'Medium', 'Fenugreek Seeds, Chilli, Turmeric, Oil', 'plant', 'Unique bitter-spicy fenugreek pickle. Good for diabetes and metabolism.', 'Spice'),
        
        # Regional Specialties
        ('Gongura Pickle', 269, 4.7, 119, 'Telangana', 'Tangy', 'Medium', 'Gongura Leaves, Chilli, Salt, Oil', 'plant', 'Authentic Telangana specialty with tangy gongura leaves. A regional pride with unique flavor.', 'Regional'),
        ('Poondu Pickle (Garlic)', 279, 4.6, 95, 'Tamil Nadu', 'Pungent', 'Medium-Hot', 'Pearl Garlic, Chilli, Oil, Salt', 'garlic', 'South Indian garlic pickle in mustard oil. A powerhouse of flavor and nutrition.', 'Regional'),
        ('Lemon Pickle', 199, 4.9, 201, 'Karnataka', 'Tangy & Sour', 'Mild-Medium', 'Lemon, Chilli, Turmeric, Salt, Oil', 'lemon', 'Bright, zesty lemon pickle perfect as a condiment. Fresh citrus flavor enhances any meal.', 'Citrus'),
        ('Lime Pickle with Asafetida', 209, 4.5, 88, 'Telangana', 'Tangy', 'Medium', 'Lime, Chilli, Turmeric, Asafetida, Oil', 'lemon', 'Traditional lime pickle with digestive asafetida. Aids digestion and adds flavor.', 'Citrus'),
        ('Tamarind Pickle', 249, 4.6, 107, 'Andhra Pradesh', 'Sour & Sweet', 'Mild', 'Tamarind Pulp, Jaggery, Chilli, Salt, Oil', 'bottle', 'Sweet-sour tamarind pickle with tanginess. Versatile condiment for dal and rice.', 'Citrus'),
        ('Pomegranate Pickle', 329, 4.8, 76, 'Maharashtra', 'Tangy & Sweet', 'Medium', 'Pomegranate Seeds, Chilli, Jaggery, Oil', 'apple', 'Premium pomegranate pickle with sweet-tangy profile. Rich in antioxidants and taste.', 'Fruit'),
        
        # Vegetable Pickles
        ('Mixed Vegetable Pickle', 219, 4.5, 145, 'Himachal Pradesh', 'Spicy & Tangy', 'Medium', 'Carrot, Turnip, Cauliflower, Chilli, Oil', 'carrot', 'Colorful mix of seasonal vegetables. Perfect for balanced nutrition and varied flavors.', 'Vegetable'),
        ('Carrot Pickle', 189, 4.6, 156, 'Punjab', 'Sweet & Spicy', 'Mild-Medium', 'Carrot, Ginger, Chilli, Salt, Oil', 'carrot', 'Crunchy carrot pickle with mild spice. Rich in beta-carotene and naturally sweet.', 'Vegetable'),
        ('Radish Pickle', 199, 4.4, 98, 'Uttarakhand', 'Pungent', 'Medium', 'Radish, Chilli, Turmeric, Salt, Oil', 'plant', 'Peppery radish pickle with mustard oil. Excellent for digestion and detoxification.', 'Vegetable'),
        ('Cauliflower Pickle', 209, 4.5, 87, 'Haryana', 'Spicy', 'Medium-Hot', 'Cauliflower, Ginger, Chilli, Oil, Salt', 'leaf', 'Florets of cauliflower in aromatic oil. Nutritious and flavorful vegetable pickle.', 'Vegetable'),
        ('Beetroot Pickle', 229, 4.7, 112, 'Uttarakhand', 'Sweet & Tangy', 'Mild', 'Beetroot, Ginger, Chilli, Salt, Oil', 'apple', 'Earthy beetroot pickle with sweet undertone. Rich in iron and blood purifying.', 'Vegetable'),
        ('Cucumber Pickle', 189, 4.5, 134, 'Uttar Pradesh', 'Salty & Sour', 'Mild', 'Cucumber, Dill, Chilli, Salt, Oil', 'leaf', 'Refreshing cucumber pickle with herbs. Cooling and light with tangy flavor.', 'Vegetable'),
        ('Onion Pickle', 179, 4.3, 76, 'Andhra Pradesh', 'Spicy & Tangy', 'Medium', 'Pearl Onion, Chilli, Turmeric, Salt, Oil', 'circle-notch', 'Traditional onion pickle with bite. Simple yet flavorful vegetable preservation.', 'Vegetable'),
        ('Bitter Gourd Pickle', 219, 4.4, 92, 'Gujarat', 'Bitter & Spicy', 'Medium-Hot', 'Bitter Gourd, Chilli, Salt, Oil', 'leaf', 'Medicinal bitter gourd pickle. Excellent for blood sugar regulation.', 'Vegetable'),
        
        # Fruit Pickles
        ('Amla Pickle', 269, 4.8, 178, 'Uttar Pradesh', 'Tangy & Sweet', 'Mild-Medium', 'Indian Gooseberry, Chilli, Turmeric, Salt, Oil', 'apple', 'Vitamin C powerhouse. Tangy gooseberry pickle aids immunity and digestion.', 'Fruit'),
        ('Mango Murabba', 349, 4.7, 95, 'Uttar Pradesh', 'Sweet', 'Mild', 'Ripe Mango, Sugar, Cardamom, Dry Fruit', 'mango', 'Sweet preserve jam with whole mango pieces. Delicacy for special occasions.', 'Fruit'),
        ('Orange Peel Pickle', 289, 4.6, 78, 'Tamil Nadu', 'Tangy & Bitter', 'Mild-Medium', 'Orange Peel, Sugar, Chilli, Oil', 'lemon', 'Aromatic orange peel pickle with citrus notes. Unique and refreshing.', 'Citrus'),
        ('Papaya Pickle', 239, 4.5, 88, 'Karnataka', 'Spicy & Tangy', 'Medium', 'Raw Papaya, Chilli, Turmeric, Salt, Oil', 'apple', 'Green papaya pickle with spices. Enzyme-rich and aids digestion.', 'Fruit'),
        ('Guava Pickle', 259, 4.6, 76, 'Madhya Pradesh', 'Tangy & Spicy', 'Medium', 'Raw Guava, Chilli, Dry Mango Powder, Oil', 'apple', 'Tangy guava pickle with mango powder. Vitamin C rich and refreshing.', 'Fruit'),
        
        # Specialty & Fusion
        ('Dry Mango Powder Pickle (Amchur)', 279, 4.5, 87, 'Rajasthan', 'Tangy', 'Mild-Medium', 'Dry Mango Powder, Chilli, Salt, Oil, Spices', 'mango', 'Concentrated tangy powder from sun-dried mangoes. Essential spice for cooking.', 'Specialty'),
        ('Pineapple Pickle', 299, 4.7, 92, 'Goa', 'Spicy & Sweet', 'Medium', 'Pineapple, Chilli, Turmeric, Jaggery, Oil', 'leaf', 'Tropical pineapple with spices. Fusion of South Indian and Portuguese influences.', 'Specialty'),
        ('Date & Tamarind Pickle', 319, 4.8, 61, 'Rajasthan', 'Sweet & Sour', 'Mild', 'Dates, Tamarind, Chilli, Salt, Oil', 'bottle', 'Premium mixture of sweet dates and tangy tamarind. Perfect for festive seasons.', 'Specialty'),
        ('Mango-Ginger Pickle', 289, 4.7, 98, 'Himachal Pradesh', 'Spicy & Tangy', 'Medium-Hot', 'Mango, Ginger, Chilli, Turmeric, Oil', 'mango', 'Warming combination of mango and ginger with traditional spices.', 'Specialty'),
        ('Honey & Lemon Pickle', 309, 4.9, 72, 'Kashmir', 'Sweet & Tangy', 'Mild', 'Lemon, Honey, Ginger, Chilli, Oil', 'lemon', 'Premium pickle infused with raw honey. Natural, healthy alternative.', 'Specialty'),
        ('Chilli-Garlic Fusion', 259, 4.6, 105, 'Himachal', 'Spicy & Pungent', 'Extra Hot', 'Chilli, Garlic, Oil, Salt, Spices', 'chilli', 'Intense fusion of ghost chillies and garlic. For extreme spice lovers.', 'Specialty'),
        ('South Indian Sambar Pickle', 279, 4.5, 87, 'Tamil Nadu', 'Tangy & Spicy', 'Medium', 'Mixed Vegetables, Chilli, Mustard, Turmeric, Oil', 'leaf', 'Pre-mixed pickle with sambar spices. Instant flavor for South Indian meals.', 'Regional'),
        
        # Non-Vegetarian (Premium)
        ('Mango Chicken Pickle', 449, 4.7, 43, 'Andhra Pradesh', 'Spicy & Tangy', 'Hot', 'Chicken, Mango, Chilli, Turmeric, Oil', 'drumstick', 'Premium non-vegetarian pickle with tender chicken pieces and mango tanginess.', 'Non-Veg'),
        ('Fish Pickle (Hilsa)', 549, 4.8, 36, 'West Bengal', 'Spicy', 'Medium-Hot', 'Hilsa Fish, Chilli, Turmeric, Mustard Oil', 'fish', 'Authentic Bengali fish pickle with authentic preparation. Protein-rich delicacy.', 'Non-Veg'),
        ('Prawn Pickle', 499, 4.6, 28, 'Kerala', 'Spicy & Tangy', 'Medium-Hot', 'Prawns, Chilli, Turmeric, Coconut Oil', 'fish', 'Seafood specialty with prawns and coconut oil. Kerala coast specialty.', 'Non-Veg'),
        ('Duck Pickle', 459, 4.7, 31, 'Assam', 'Spicy', 'Hot', 'Duck Meat, Chilli, Ginger, Turmeric, Oil', 'drumstick', 'northeastern specialty with tender duck and traditional spices.', 'Non-Veg'),
        
        # Gift Sets & Combos (Special)
        ('Classic Pickle Trio', 599, 4.8, 156, 'Pan India', 'Mixed', 'Varies', 'Mango, Lemon, Green Chilli Pickles', 'gift', 'Perfect gift set with three bestselling pickles. Great for gifting.', 'Gift'),
        ('Festival Special Pack', 799, 4.9, 98, 'Pan India', 'Mixed', 'Varies', '5 Premium Pickles Selection', 'gift', 'Curated collection of 5 premium pickles for celebrations and festivals.', 'Gift'),
        ('Royal Heritage Collection', 1299, 5.0, 67, 'Pan India', 'Premium Mix', 'Varies', '8 Artisanal Pickles Collection', 'gift', 'Exclusive collection of 8 rare and premium pickles for connoisseurs.', 'Gift'),
    ]
    
    with get_db_context() as db:
        # Check if products already exist
        count = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        if count == 0:
            db.executemany('''
                INSERT INTO products (name, price, rating, reviews_count, origin, taste_profile, 
                                     spice_level, ingredients, image_url, description, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', products)
            print(f"✓ Seeded {len(products)} products")

# Initialize database
init_db()
seed_products()

# ==================== API Routes ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/products')
def products_page():
    """Products listing page"""
    return render_template('products.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')

@app.route('/cart')
def cart_page():
    """Shopping cart page"""
    return render_template('cart.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    with get_db_context() as db:
        query = 'SELECT * FROM products WHERE in_stock = 1'
        params = []
        
        # Filtering
        taste = request.args.get('taste')
        origin = request.args.get('origin')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        min_rating = request.args.get('min_rating', type=float)
        category = request.args.get('category')
        
        if taste:
            query += ' AND taste_profile = ?'
            params.append(taste)
        if origin:
            query += ' AND origin = ?'
            params.append(origin)
        if min_price is not None:
            query += ' AND price >= ?'
            params.append(min_price)
        if max_price is not None:
            query += ' AND price <= ?'
            params.append(max_price)
        if min_rating is not None:
            query += ' AND rating >= ?'
            params.append(min_rating)
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        # Sorting
        sort_by = request.args.get('sort', 'name')
        if sort_by == 'price_low':
            query += ' ORDER BY price ASC'
        elif sort_by == 'price_high':
            query += ' ORDER BY price DESC'
        elif sort_by == 'rating':
            query += ' ORDER BY rating DESC'
        elif sort_by == 'newest':
            query += ' ORDER BY created_at DESC'
        else:
            query += ' ORDER BY name ASC'
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = 12
        offset = (page - 1) * per_page
        
        # Get total count
        count_query = query.replace('SELECT *', 'SELECT COUNT(*) as count')
        total = db.execute(count_query, params).fetchone()['count']
        
        query += f' LIMIT {per_page} OFFSET {offset}'
        products = db.execute(query, params).fetchall()
        
        return jsonify({
            'products': [dict(p) for p in products],
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get single product detail"""
    with get_db_context() as db:
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        if product:
            return jsonify(dict(product))
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items"""
    session_id = request.args.get('session_id', 'default')
    with get_db_context() as db:
        items = db.execute('''
            SELECT c.id, c.product_id, c.quantity, p.* 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        ''', (session_id,)).fetchall()
        
        total = sum(item['price'] * item['quantity'] for item in items)
        
        return jsonify({
            'items': [dict(item) for item in items],
            'total': total,
            'count': len(items)
        })

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    data = request.json
    session_id = data.get('session_id', 'default')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'error': 'Product ID required'}), 400
    
    with get_db_context() as db:
        # Check if product exists
        product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Insert or update cart
        db.execute('''
            INSERT INTO cart (product_id, quantity, session_id)
            VALUES (?, ?, ?)
            ON CONFLICT(product_id, session_id) 
            DO UPDATE SET quantity = quantity + ?
        ''', (product_id, quantity, session_id, quantity))
        
        # Get updated cart
        items = db.execute('''
            SELECT c.id, c.product_id, c.quantity, p.* 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        ''', (session_id,)).fetchall()
        
        total = sum(item['price'] * item['quantity'] for item in items)
        
        return jsonify({
            'message': 'Product added to cart',
            'items': [dict(item) for item in items],
            'total': total,
            'count': len(items)
        })

@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    """Update cart item quantity"""
    data = request.json
    quantity = data.get('quantity', 1)
    session_id = data.get('session_id', 'default')
    
    if quantity < 1:
        return delete_cart(cart_id)
    
    with get_db_context() as db:
        db.execute('UPDATE cart SET quantity = ? WHERE id = ?', (quantity, cart_id))
        
        items = db.execute('''
            SELECT c.id, c.product_id, c.quantity, p.* 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        ''', (session_id,)).fetchall()
        
        total = sum(item['price'] * item['quantity'] for item in items)
        
        return jsonify({
            'message': 'Cart updated',
            'items': [dict(item) for item in items],
            'total': total,
            'count': len(items)
        })

@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    """Remove item from cart"""
    session_id = request.args.get('session_id', 'default')
    
    with get_db_context() as db:
        db.execute('DELETE FROM cart WHERE id = ?', (cart_id,))
        
        items = db.execute('''
            SELECT c.id, c.product_id, c.quantity, p.* 
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        ''', (session_id,)).fetchall()
        
        total = sum(item['price'] * item['quantity'] for item in items)
        
        return jsonify({
            'message': 'Item removed from cart',
            'items': [dict(item) for item in items],
            'total': total,
            'count': len(items)
        })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create new order"""
    data = request.json
    
    # Validate required fields
    required = ['name', 'email', 'phone', 'address', 'items', 'total']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    with get_db_context() as db:
        db.execute('''
            INSERT INTO orders (customer_name, customer_email, customer_phone, 
                               customer_address, items, total_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, 'confirmed')
        ''', (
            data['name'],
            data['email'],
            data['phone'],
            data['address'],
            json.dumps(data['items']),
            data['total']
        ))
        
        order = db.execute('SELECT last_insert_rowid() as id').fetchone()
        
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order['id'],
            'total': data['total']
        })

@app.route('/api/search', methods=['GET'])
def search():
    """Search products"""
    query = request.args.get('q', '')
    if not query:
        return jsonify({'products': []})
    
    with get_db_context() as db:
        results = db.execute('''
            SELECT * FROM products 
            WHERE name LIKE ? OR description LIKE ? OR ingredients LIKE ?
            LIMIT 10
        ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()
        
        return jsonify({'products': [dict(p) for p in results]})

@app.route('/api/filters', methods=['GET'])
def get_filters():
    """Get available filter options"""
    with get_db_context() as db:
        tastes = [row['taste_profile'] for row in db.execute(
            'SELECT DISTINCT taste_profile FROM products ORDER BY taste_profile'
        ).fetchall()]
        
        origins = [row['origin'] for row in db.execute(
            'SELECT DISTINCT origin FROM products ORDER BY origin'
        ).fetchall()]
        
        categories = [row['category'] for row in db.execute(
            'SELECT DISTINCT category FROM products ORDER BY category'
        ).fetchall()]
        
        prices = db.execute('SELECT MIN(price) as min, MAX(price) as max FROM products').fetchone()
        
        return jsonify({
            'tastes': tastes,
            'origins': origins,
            'categories': categories,
            'price_range': {
                'min': prices['min'],
                'max': prices['max']
            }
        })

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🥒 PICKLE STORE - Starting Server")
    print("=" * 50)
    print("📍 Local:   http://localhost:5000")
    print("🎯 Press CTRL+C to stop")
    print("=" * 50)
    app.run(debug=True, host='localhost', port=5000)

# Helper function for product icons (accessible in templates)
def get_product_icon(icon_type):
    """Convert product image_url to Font Awesome icon class"""
    icon_map = {
        'mango': 'fas fa-leaf',
        'chilli': 'fas fa-pepper-hot',
        'garlic': 'fas fa-clove',
        'ginger': 'fas fa-crown',
        'lemon': 'fas fa-lemon',
        'carrot': 'fas fa-carrot',
        'apple': 'fas fa-apple-alt',
        'plant': 'fas fa-leaf',
        'leaf': 'fas fa-leaf',
        'bottle': 'fas fa-jar',
        'circle-notch': 'fas fa-ring',
        'drumstick': 'fas fa-drumstick-bite',
        'fish': 'fas fa-fish',
        'gift': 'fas fa-gift',
        'turmeric': 'fas fa-dharmachakra',
    }
    return icon_map.get(icon_type, 'fas fa-jar')

@app.context_processor
def inject_icon_helper():
    return dict(get_product_icon=get_product_icon)
