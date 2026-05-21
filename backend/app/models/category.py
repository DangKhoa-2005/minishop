"""
Category Model
"""
from datetime import datetime
from app import db


class Category(db.Model):
    """Category model for product categorization"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self, include_products=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url,
            'product_count': self.products.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_products:
            data['products'] = [p.to_dict() for p in self.products.all()]
        
        return data
