"""
AI Chatbot Routes (Innovation Feature)
Uses OpenAI API for product consultation
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.models import Product, Category

chatbot_bp = Blueprint('chatbot', __name__)


def get_products_context():
    """Get products context for AI"""
    products = Product.query.limit(50).all()
    categories = Category.query.all()
    
    context = "Bạn là trợ lý bán hàng của Mini Shop. Dưới đây là danh sách sản phẩm:\n\n"
    
    context += "DANH MỤC:\n"
    for cat in categories:
        context += f"- {cat.name}\n"
    
    context += "\nSẢN PHẨM:\n"
    for product in products:
        category_name = product.category.name if product.category else "Không phân loại"
        stock_status = "Còn hàng" if product.stock > 0 else "Hết hàng"
        context += f"- {product.name} | Giá: {product.price:,.0f}đ | Danh mục: {category_name} | {stock_status}\n"
        if product.description:
            context += f"  Mô tả: {product.description[:100]}...\n"
    
    context += "\nHãy tư vấn sản phẩm phù hợp cho khách hàng dựa trên nhu cầu của họ. "
    context += "Trả lời bằng tiếng Việt, thân thiện và hữu ích."
    
    return context


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """
    Chat with AI assistant
    ---
    Request Body:
        - message: string (required) - User's message
        - history: array (optional) - Previous conversation history
    """
    data = request.get_json()
    raw_message = data.get('message', '')
    # Strip and sanitize server-side to be robust against client variants (leading emojis, invisible chars)
    import re
    user_message = raw_message.strip()
    user_message = re.sub(r'^[^\w\d]+', '', user_message, flags=re.UNICODE)
    history = data.get('history', [])
    # Safe logging: avoid UnicodeEncodeError when printing to consoles with limited encodings
    try:
        print(f"[chatbot] /chat received from {request.remote_addr} origin={request.headers.get('Origin')} message={repr(raw_message)} sanitized={repr(user_message)} history_len={len(history)}")
    except Exception:
        try:
            print("[chatbot] /chat received (print encoding error). message_bytes=", raw_message.encode('utf-8', errors='replace'))
            print("[chatbot] sanitized_bytes=", user_message.encode('utf-8', errors='replace'))
        except Exception:
            print(f"[chatbot] /chat received (unprintable). msg_len={len(raw_message)} sanitized_len={len(user_message)} history_len={len(history)}")
    
    if not user_message:
        return jsonify({
            'success': False,
            'message': 'Vui lòng nhập tin nhắn'
        }), 400
    
    api_key = current_app.config.get('OPENAI_API_KEY')
    
    if not api_key:
        # Fallback response when OpenAI is not configured
        return jsonify({
            'success': True,
            'data': {
                'response': get_fallback_response(user_message),
                'is_fallback': True
            }
        }), 200
    
    try:
        import openai
        
        client = openai.OpenAI(api_key=api_key)
        
        # Build messages
        messages = [
            {
                "role": "system",
                "content": get_products_context()
            }
        ]
        
        # Add conversation history
        for msg in history[-10:]:  # Keep last 10 messages
            messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        assistant_message = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'data': {
                'response': assistant_message,
                'is_fallback': False
            }
        }), 200
        
    except Exception as e:
        # Return fallback on error
        return jsonify({
            'success': True,
            'data': {
                'response': get_fallback_response(user_message),
                'is_fallback': True,
                'error': str(e)
            }
        }), 200


def get_fallback_response(message):
    import re
    # Debug: log incoming message to help diagnose suggestion handling
    try:
        print(f"[chatbot] get_fallback_response called with message: {repr(message)}")
    except Exception:
        pass

    # Helper: parse price from message (dưới xx triệu)
    def extract_price_limit(msg):
        match = re.search(r'(?:dưới|giá dưới|giá dưới|<|<=|thấp hơn|ít hơn)\s*([0-9]+)\s*(tr|triệu|trieu|tr\.|m)', msg)
        if match:
            val = int(match.group(1))
            return val * 1_000_000
        match2 = re.search(r'([0-9]+)\s*(tr|triệu|trieu|tr\.|m)\s*(?:trở xuống|hoặc ít hơn|hoặc thấp hơn)', msg)
        if match2:
            val = int(match2.group(1))
            return val * 1_000_000
        return None
    """Generate smart fallback response without AI"""
    message_lower = message.lower()
    try:
        print(f"[chatbot] normalized message_lower: {repr(message_lower)}")
    except Exception:
        pass

    # Greeting - match only when the message *starts* with a greeting to avoid false positives inside longer phrases
    if re.search(r"^\s*(?:xin chào|hello|chào|hey)\b", message_lower):
        try:
            print('[chatbot] matched greeting branch (start regex)')
        except Exception:
            pass
        return "Xin chào! 👋 Tôi là trợ lý của Mini Shop. Tôi có thể giúp bạn:\n• Tìm điện thoại, laptop, tablet\n• Tư vấn đồng hồ thông minh\n• Giới thiệu phụ kiện công nghệ\n• Thông tin giao hàng & bảo hành\n\nBạn đang quan tâm đến sản phẩm nào?"

    # Điện thoại - tìm category linh hoạt
    if any(word in message_lower for word in ['điện thoại', 'phone', 'iphone', 'samsung', 'oppo', 'xiaomi', 'dt', 'đt']):
        # Tìm category phù hợp
        cat = Category.query.filter(Category.name.ilike('%điện thoại%')).first()
        if not cat:
            # Tìm category chứa từ khóa liên quan
            cat = Category.query.filter(Category.name.ilike('%phone%')).first()
        if cat:
            products = Product.query.filter(Product.category_id == cat.id, Product.stock > 0).limit(4).all()
        else:
            # fallback: tìm sản phẩm theo tên
            products = Product.query.filter(Product.name.ilike('%điện thoại%'), Product.stock > 0).limit(4).all()
        if not products:
            # fallback: tìm theo các từ khóa khác
            for kw in ['phone', 'iphone', 'samsung', 'oppo', 'xiaomi']:
                products = Product.query.filter(Product.name.ilike(f'%{kw}%'), Product.stock > 0).limit(4).all()
                if products:
                    break
        if products:
            response = "📱 **Điện thoại nổi bật tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Bạn muốn xem chi tiết sản phẩm nào? Hoặc cần tư vấn theo ngân sách?"
            return response
        return "Hiện tại shop chưa có sản phẩm điện thoại phù hợp. Bạn có thể xem laptop hoặc tablet!"

    # Laptop
    if any(word in message_lower for word in ['laptop', 'macbook', 'máy tính', 'notebook', 'dell', 'asus', 'hp', 'lenovo', 'thinkpad']):
        products = Product.query.join(Category).filter(
            Category.name.ilike('%laptop%')
        ).limit(4).all()

        if products:
            response = "💻 **Laptop hot nhất tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Bạn cần laptop cho công việc văn phòng, học tập hay gaming?"
            return response
        return "Hiện tại shop đang cập nhật sản phẩm laptop. Bạn có thể xem các sản phẩm khác!"
    
    # Tablet / iPad
    if any(word in message_lower for word in ['tablet', 'ipad', 'máy tính bảng', 'tab', 'galaxy tab']):
        print('[chatbot] matched tablet branch')
        # Tìm category phù hợp
        cat = Category.query.filter(Category.name.ilike('%tablet%')).first()
        if not cat:
            cat = Category.query.filter(Category.name.ilike('%bảng%')).first()
        if cat:
            products = Product.query.filter(Product.category_id == cat.id, Product.stock > 0).limit(4).all()
        else:
            # fallback: tìm sản phẩm theo tên
            products = Product.query.filter(Product.name.ilike('%tablet%'), Product.stock > 0).limit(4).all()
        if not products:
            for kw in ['ipad', 'tab', 'galaxy tab']:
                products = Product.query.filter(Product.name.ilike(f'%{kw}%'), Product.stock > 0).limit(4).all()
                if products:
                    break
        print(f"[chatbot] tablet products found: {len(products) if products else 0}")
        if products:
            response = "📲 **Tablet chính hãng tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Tablet phù hợp cho giải trí, học tập online và làm việc nhẹ!"
            return response
        return "Hiện tại shop chưa có tablet phù hợp. Bạn có thể xem điện thoại hoặc laptop!"
    # Tai nghe / AirPods / Phụ kiện âm thanh
    if any(word in message_lower for word in ['airpods', 'tai nghe', 'earbuds', 'headphone', 'loa bluetooth', 'loa', 'sound', 'audio']):
        print('[chatbot] matched airpods/earbuds branch')
        # Tìm category phụ kiện hoặc tên sản phẩm
        cat = Category.query.filter(Category.name.ilike('%phụ kiện%')).first()
        if cat:
            products = Product.query.filter(Product.category_id == cat.id, Product.name.ilike('%airpods%') | Product.name.ilike('%tai nghe%') | Product.name.ilike('%earbuds%') | Product.name.ilike('%headphone%'), Product.stock > 0).limit(4).all()
        else:
            products = Product.query.filter((Product.name.ilike('%airpods%') | Product.name.ilike('%tai nghe%') | Product.name.ilike('%earbuds%') | Product.name.ilike('%headphone%')), Product.stock > 0).limit(4).all()
        print(f"[chatbot] airpods products found: {len(products) if products else 0}")
        if products:
            response = "🎧 **Phụ kiện âm thanh tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Tai nghe, AirPods, loa bluetooth chính hãng, bảo hành đầy đủ!"
            return response
        return "Hiện tại shop chưa có tai nghe/AirPods phù hợp. Bạn có thể xem các sản phẩm khác!"
    
    # Đồng hồ thông minh / Smartwatch - tìm category linh hoạt
    if any(word in message_lower for word in ['đồng hồ', 'watch', 'smartwatch', 'apple watch', 'garmin', 'samsung watch', 'thông minh']):
        # Tìm category phù hợp
        cat = Category.query.filter(Category.name.ilike('%đồng hồ%')).first()
        if not cat:
            # Tìm category chứa từ khóa liên quan
            cat = Category.query.filter(Category.name.ilike('%watch%')).first()
        if cat:
            products = Product.query.filter(Product.category_id == cat.id, Product.stock > 0).limit(4).all()
        else:
            # fallback: tìm sản phẩm theo tên
            products = Product.query.filter(Product.name.ilike('%đồng hồ%'), Product.stock > 0).limit(4).all()
        if not products:
            # fallback: tìm theo các từ khóa khác
            for kw in ['watch', 'smartwatch', 'apple watch', 'garmin', 'samsung']:
                products = Product.query.filter(Product.name.ilike(f'%{kw}%'), Product.stock > 0).limit(4).all()
                if products:
                    break
        if products:
            response = "⌚ **Đồng hồ thông minh tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Đồng hồ thông minh giúp theo dõi sức khỏe, thể thao và nhận thông báo tiện lợi!"
            return response
        return "Hiện tại shop chưa có đồng hồ thông minh phù hợp. Bạn có thể xem phụ kiện khác!"
    
    # Phụ kiện
    if any(word in message_lower for word in ['phụ kiện', 'tai nghe', 'airpods', 'sạc', 'cáp', 'ốp lưng', 'bao da', 'headphone', 'earbuds']):
        products = Product.query.join(Category).filter(
            Category.name.ilike('%phụ kiện%')
        ).limit(4).all()
        
        if products:
            response = "🎧 **Phụ kiện công nghệ tại Mini Shop:**\n"
            for p in products:
                stock_text = "✅ Còn hàng" if p.stock > 0 else "❌ Hết hàng"
                response += f"• {p.name} - **{p.price:,.0f}đ** ({stock_text})\n"
            response += "\n💡 Phụ kiện chính hãng, bảo hành đầy đủ!"
            return response
        return "Hiện tại shop đang cập nhật phụ kiện. Bạn có thể xem các sản phẩm khác!"
    
    # Giá cả / Ngân sách hoặc điện thoại dưới xx triệu
    price_limit = extract_price_limit(message_lower)
    if price_limit:
        # Ưu tiên lọc điện thoại dưới giá
        cat = Category.query.filter(Category.name.ilike('%điện thoại%')).first()
        if cat:
            products = Product.query.filter(Product.category_id == cat.id, Product.price <= price_limit, Product.stock > 0).order_by(Product.price.asc()).limit(4).all()
        else:
            products = Product.query.filter(Product.name.ilike('%điện thoại%'), Product.price <= price_limit, Product.stock > 0).order_by(Product.price.asc()).limit(4).all()
        if products:
            response = f"💰 **Điện thoại dưới {price_limit//1_000_000} triệu tại Mini Shop:**\n"
            for p in products:
                response += f"• {p.name} - **{p.price:,.0f}đ** (✅ Còn hàng)\n"
            response += "\nBạn muốn xem chi tiết sản phẩm nào? Hoặc cần tư vấn thêm?"
            return response
        return f"Hiện tại shop chưa có điện thoại nào dưới {price_limit//1_000_000} triệu. Bạn có thể xem các sản phẩm khác!"
    # Nếu hỏi ngân sách chung chung
    if any(word in message_lower for word in ['giá', 'bao nhiêu', 'price', 'rẻ', 'đắt', 'ngân sách', 'tiền']):
        return "💰 **Tư vấn theo ngân sách:**\n• Dưới 10 triệu: Điện thoại tầm trung, phụ kiện\n• 10-20 triệu: iPhone, Samsung flagship, Laptop văn phòng\n• 20-30 triệu: MacBook, Laptop gaming\n• Trên 30 triệu: Sản phẩm cao cấp\n\nBạn có ngân sách khoảng bao nhiêu? Tôi sẽ gợi ý phù hợp!"
    
    # Giao hàng
    if any(word in message_lower for word in ['giao hàng', 'ship', 'delivery', 'vận chuyển', 'freeship']):
        return "🚚 **Chính sách giao hàng Mini Shop:**\n• Giao hàng toàn quốc trong 2-5 ngày\n• **MIỄN PHÍ** giao hàng cho đơn từ 500.000đ\n• Hỗ trợ giao hàng nhanh trong ngày (nội thành)\n• Đóng gói cẩn thận, an toàn\n\nBạn ở khu vực nào? Tôi kiểm tra thời gian giao hàng cho bạn!"
    
    # Thanh toán
    if any(word in message_lower for word in ['thanh toán', 'payment', 'trả tiền', 'cod', 'chuyển khoản']):
        return "💳 **Phương thức thanh toán:**\n• **COD** - Thanh toán khi nhận hàng (phổ biến nhất)\n• Chuyển khoản ngân hàng\n• Ví điện tử (MoMo, ZaloPay)\n\nBạn cứ yên tâm đặt hàng, chỉ thanh toán khi nhận được sản phẩm ưng ý!"
    
    # Bảo hành / Đổi trả
    if any(word in message_lower for word in ['đổi trả', 'bảo hành', 'warranty', 'lỗi', 'hỏng', 'sửa chữa']):
        return "🛡️ **Chính sách bảo hành Mini Shop:**\n• Bảo hành chính hãng 12-24 tháng\n• Đổi trả trong 7 ngày nếu lỗi nhà sản xuất\n• Hỗ trợ 1 đổi 1 trong 30 ngày đầu\n• Trung tâm bảo hành ủy quyền toàn quốc\n\nBạn cần hỗ trợ bảo hành sản phẩm nào?"
    
    # Khuyến mãi
    if any(word in message_lower for word in ['khuyến mãi', 'giảm giá', 'sale', 'voucher', 'mã giảm', 'ưu đãi', 'promotion']):
        return "🎉 **Ưu đãi đang có tại Mini Shop:**\n• Giảm 5% cho khách hàng mới\n• Freeship đơn từ 500K\n• Tặng phụ kiện khi mua điện thoại\n• Trả góp 0% lãi suất\n\nĐừng bỏ lỡ! Đặt hàng ngay hôm nay!"
    
    # So sánh sản phẩm
    if any(word in message_lower for word in ['so sánh', 'khác nhau', 'nên mua', 'tốt hơn', 'hay hơn', 'chọn']):
        return "🔍 **Cần tư vấn so sánh sản phẩm?**\nHãy cho tôi biết:\n• 2 sản phẩm bạn đang phân vân\n• Hoặc nhu cầu sử dụng của bạn\n\nTôi sẽ phân tích ưu nhược điểm để bạn chọn được sản phẩm phù hợp nhất!"
    
    # Cảm ơn
    if any(word in message_lower for word in ['cảm ơn', 'thank', 'thanks', 'tks', 'ok', 'được rồi']):
        return "😊 Không có gì! Rất vui được hỗ trợ bạn!\n\nNếu cần thêm thông tin gì, đừng ngại hỏi tôi nhé. Chúc bạn mua sắm vui vẻ! 🛒"
    
    # Tìm sản phẩm theo tên cụ thể
    # Tìm trong database nếu có từ khóa dài hơn 3 ký tự
    words = message_lower.split()
    for word in words:
        if len(word) > 3:
            products = Product.query.filter(
                Product.name.ilike(f'%{word}%')
            ).limit(3).all()
            
            if products:
                response = f"🔎 Tôi tìm thấy các sản phẩm liên quan đến '{word}':\n"
                for p in products:
                    response += f"• {p.name} - **{p.price:,.0f}đ**\n"
                response += "\nBạn muốn xem chi tiết sản phẩm nào?"
                return response
    
    # Default response - thân thiện và gợi ý
    categories = Category.query.all()
    cat_list = ", ".join([c.name for c in categories]) if categories else "điện thoại, laptop, tablet"
    
    return f"🤔 Tôi chưa hiểu rõ yêu cầu của bạn. Tôi có thể giúp bạn với:\n\n📦 **Sản phẩm:** {cat_list}\n🚚 **Dịch vụ:** Giao hàng, thanh toán, bảo hành\n💰 **Tư vấn:** So sánh, gợi ý theo ngân sách\n\nBạn thử hỏi cụ thể hơn nhé! Ví dụ: 'Tôi muốn mua đồng hồ thông minh' hoặc 'Laptop nào tốt dưới 20 triệu?'"


@chatbot_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get diverse chat suggestions"""
    suggestions = [
        "📱 Tôi muốn xem điện thoại",
        "💻 Laptop nào phù hợp cho sinh viên?",
        "⌚ Có đồng hồ thông minh nào?",
        "📲 Giới thiệu tablet cho tôi",
        "🎧 Tai nghe AirPods giá bao nhiêu?",
        "🚚 Chính sách giao hàng thế nào?",
        "🛡️ Bảo hành sản phẩm ra sao?",
        "🎉 Có khuyến mãi gì không?"
    ]
    
    return jsonify({
        'success': True,
        'data': suggestions
    }), 200
