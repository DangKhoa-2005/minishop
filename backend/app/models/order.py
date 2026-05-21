"""
Order Models
"""
from datetime import datetime
from app import db


class Order(db.Model):
    """Order model for customer purchases"""
    __tablename__ = 'orders'
    
    # Order status constants
    STATUS_CONFIRMED = 'confirmed'
    STATUS_SHIPPING = 'shipping'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    
    VALID_STATUSES = [
        STATUS_CONFIRMED,
        STATUS_SHIPPING,
        STATUS_DELIVERED,
        STATUS_CANCELLED
    ]

    PAYMENT_METHOD_COD = 'cod'
    PAYMENT_METHOD_BANK_TRANSFER = 'bank_transfer'
    PAYMENT_METHOD_E_WALLET = 'e_wallet'

    VALID_PAYMENT_METHODS = [
        PAYMENT_METHOD_COD,
        PAYMENT_METHOD_BANK_TRANSFER,
        PAYMENT_METHOD_E_WALLET
    ]
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    user_order_number = db.Column(db.Integer, nullable=True)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(50), default=STATUS_CONFIRMED, index=True)
    shipping_address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False, default=PAYMENT_METHOD_COD)
    customer_name = db.Column(db.String(255), nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan', lazy='dynamic')
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'
    
    def get_status_display(self):
        """Get display text for status"""
        status_map = {
            self.STATUS_CONFIRMED: 'Đã xác nhận',
            self.STATUS_SHIPPING: 'Đang giao hàng',
            self.STATUS_DELIVERED: 'Đã giao hàng',
            self.STATUS_CANCELLED: 'Đã hủy'
        }
        return status_map.get(self.status, self.status)

    def get_payment_method_display(self):
        """Get display text for payment method"""
        payment_map = {
            self.PAYMENT_METHOD_COD: 'COD - Khi nhận hàng',
            self.PAYMENT_METHOD_BANK_TRANSFER: 'Chuyển khoản ngân hàng',
            self.PAYMENT_METHOD_E_WALLET: 'Ví điện tử (MoMo/ZaloPay)'
        }
        method = self.payment_method or self.PAYMENT_METHOD_COD
        return payment_map.get(method, method)
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.status == self.STATUS_CONFIRMED
    
    def to_dict(self, include_items=True):
        """Convert to dictionary"""
        payment_method = self.payment_method or self.PAYMENT_METHOD_COD
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'user_order_number': self.user_order_number,
            'user': self.user.to_dict() if getattr(self, 'user', None) else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'status': self.status,
            'status_display': self.get_status_display(),
            'shipping_address': self.shipping_address,
            'phone': self.phone,
            'payment_method': payment_method,
            'payment_method_display': self.get_payment_method_display(),
            'customer_name': self.customer_name,
            'note': self.note,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
            data['item_count'] = sum(item.quantity for item in self.items)
        
        return data


class OrderItem(db.Model):
    """Order item model - product in order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)  # Price at time of order
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<OrderItem {self.product_id} x{self.quantity}>'
    
    def get_subtotal(self):
        """Calculate item subtotal"""
        return float(self.price) * self.quantity
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'price': float(self.price) if self.price else 0,
            'subtotal': self.get_subtotal()
        }
