"""
Cart Models
"""
from datetime import datetime
from app import db


class Cart(db.Model):
    """Shopping cart model - one per user"""
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Cart {self.id} - User {self.user_id}>'
    
    def get_total(self):
        """Calculate total cart value"""
        total = 0
        for item in self.items:
            if item.product:
                total += float(item.product.price) * item.quantity
        return total
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items)
    
    def clear(self):
        """Remove all items from cart"""
        for item in self.items:
            db.session.delete(item)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': self.get_total(),
            'item_count': self.get_item_count(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CartItem(db.Model):
    """Cart item model - product in cart"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint: each product only once per cart
    __table_args__ = (
        db.UniqueConstraint('cart_id', 'product_id', name='unique_cart_product'),
    )
    
    def __repr__(self):
        return f'<CartItem {self.product_id} x{self.quantity}>'
    
    def get_subtotal(self):
        """Calculate item subtotal"""
        if self.product:
            return float(self.product.price) * self.quantity
        return 0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.get_subtotal()
        }
