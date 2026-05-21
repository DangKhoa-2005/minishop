import { Link } from 'react-router-dom'
import { ShoppingCart } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuthStore, useCartStore } from '../store'
import { useNavigate } from 'react-router-dom'

function ProductCard({ product }) {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuthStore()
  const { addToCart, isLoading } = useCartStore()
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }
  
  const handleAddToCart = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (!isAuthenticated) {
      toast.error('Vui lòng đăng nhập để thêm vào giỏ hàng')
      navigate('/login')
      return
    }
    
    const result = await addToCart(product.id, 1)
    if (result.success) {
      toast.success(result.message || 'Đã thêm vào giỏ hàng')
    } else {
      toast.error(result.message)
    }
  }
  
  return (
    <Link
      to={`/products/${product.id}`}
      className="bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow duration-200 overflow-hidden group"
    >
      {/* Image */}
      <div className="aspect-square overflow-hidden bg-gray-100">
        <img
          src={product.image_url || 'https://via.placeholder.com/400x400?text=No+Image'}
          alt={product.name}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
      </div>
      
      {/* Content */}
      <div className="p-4">
        {/* Category */}
        {product.category && (
          <span className="text-xs text-primary-600 font-medium">
            {product.category.name}
          </span>
        )}
        
        {/* Name */}
        <h3 className="font-medium text-gray-900 mt-1 line-clamp-2 min-h-[48px]">
          {product.name}
        </h3>
        
        {/* Price & Stock */}
        <div className="mt-2 flex items-center justify-between">
          <span className="text-lg font-bold text-primary-600">
            {formatPrice(product.price)}
          </span>
          <span className={`text-xs px-2 py-1 rounded-full ${
            product.in_stock 
              ? 'bg-green-100 text-green-700' 
              : 'bg-red-100 text-red-700'
          }`}>
            {product.in_stock ? 'Còn hàng' : 'Hết hàng'}
          </span>
        </div>
        
        {/* Add to cart button */}
        <button
          onClick={handleAddToCart}
          disabled={!product.in_stock || isLoading}
          className={`mt-3 w-full flex items-center justify-center gap-2 py-2 rounded-lg text-sm font-medium transition-colors ${
            product.in_stock
              ? 'bg-primary-600 text-white hover:bg-primary-700'
              : 'bg-gray-100 text-gray-400 cursor-not-allowed'
          }`}
        >
          <ShoppingCart className="w-4 h-4" />
          {product.in_stock ? 'Thêm vào giỏ' : 'Hết hàng'}
        </button>
      </div>
    </Link>
  )
}

export default ProductCard
