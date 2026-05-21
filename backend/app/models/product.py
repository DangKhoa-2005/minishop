"""
Product Model
"""
from datetime import datetime
from app import db


class Product(db.Model):
    """Product model for shop items"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cart_items = db.relationship('CartItem', backref='product', lazy='dynamic')
    order_items = db.relationship('OrderItem', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def is_in_stock(self, quantity=1):
        """Check if product is in stock"""
        return self.stock >= quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock after order"""
        if self.is_in_stock(quantity):
            self.stock -= quantity
            return True
        return False
    
    def to_dict(self, include_category=True):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0,
            'stock': self.stock,
            'image_url': self.image_url,
            'category_id': self.category_id,
            'in_stock': self.stock > 0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_category and self.category:
            data['category'] = {
                'id': self.category.id,
                'name': self.category.name
            }
        
        return data
