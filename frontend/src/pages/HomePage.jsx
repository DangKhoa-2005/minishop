import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Truck, Shield, Headphones, CreditCard } from 'lucide-react'
import { productsAPI, categoriesAPI } from '../services/api'
import ProductCard from '../components/ProductCard'
import { useAuthStore } from '../store'

function HomePage() {
  const [featuredProducts, setFeaturedProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const isAuthenticated = useAuthStore(state => state.isAuthenticated)
  
  useEffect(() => {
    loadData()
  }, [])
  
  const loadData = async () => {
    try {
      const [productsRes, categoriesRes] = await Promise.all([
        productsAPI.getAll({ per_page: 8 }),
        categoriesAPI.getAll()
      ])
      
      setFeaturedProducts(productsRes.data.data.products)
      setCategories(categoriesRes.data.data)
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div className="animate-fadeIn">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                Mua sắm thông minh
                <br />
                <span className="text-primary-200">với Mini Shop</span>
              </h1>
              <p className="mt-6 text-lg text-primary-100">
                Khám phá hàng ngàn sản phẩm công nghệ chất lượng cao với giá tốt nhất.
                Giao hàng nhanh chóng, bảo hành uy tín.
              </p>
              <div className="mt-8 flex flex-wrap gap-4">
                <Link
                  to="/products"
                  className="inline-flex items-center px-6 py-3 bg-white text-primary-600 rounded-lg font-semibold hover:bg-primary-50 transition-colors"
                >
                  Xem sản phẩm
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Link>
                {!isAuthenticated && (
                  <Link
                    to="/register"
                    className="inline-flex items-center px-6 py-3 border-2 border-white text-white rounded-lg font-semibold hover:bg-white/10 transition-colors"
                  >
                    Đăng ký ngay
                  </Link>
                )}
              </div>
            </div>
            <div className="hidden md:block">
              <img
                src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=500&h=400&fit=crop"
                alt="Shopping"
                className="w-full rounded-2xl shadow-2xl"
              />
            </div>
          </div>
        </div>
      </section>
      
      {/* Features */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center mx-auto">
                <Truck className="w-7 h-7 text-primary-600" />
              </div>
              <h3 className="mt-4 font-semibold text-gray-900">Giao hàng nhanh</h3>
              <p className="mt-2 text-sm text-gray-500">Miễn phí đơn từ 500K</p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mx-auto">
                <Shield className="w-7 h-7 text-green-600" />
              </div>
              <h3 className="mt-4 font-semibold text-gray-900">Bảo hành chính hãng</h3>
              <p className="mt-2 text-sm text-gray-500">100% sản phẩm chính hãng</p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center mx-auto">
                <Headphones className="w-7 h-7 text-orange-600" />
              </div>
              <h3 className="mt-4 font-semibold text-gray-900">Hỗ trợ 24/7</h3>
              <p className="mt-2 text-sm text-gray-500">Tư vấn AI thông minh</p>
            </div>
            <div className="text-center">
              <div className="w-14 h-14 bg-purple-100 rounded-full flex items-center justify-center mx-auto">
                <CreditCard className="w-7 h-7 text-purple-600" />
              </div>
              <h3 className="mt-4 font-semibold text-gray-900">Thanh toán dễ dàng</h3>
              <p className="mt-2 text-sm text-gray-500">COD toàn quốc</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Categories */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold text-gray-900">Danh mục sản phẩm</h2>
            <Link
              to="/products"
              className="text-primary-600 hover:text-primary-700 font-medium flex items-center"
            >
              Xem tất cả
              <ArrowRight className="ml-1 w-4 h-4" />
            </Link>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {categories.map((category) => (
              <Link
                key={category.id}
                to={`/products?category_id=${category.id}`}
                className="bg-white rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow text-center group"
              >
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform">
                  <span className="text-3xl">
                    {category.name === 'Điện thoại' && '📱'}
                    {category.name === 'Laptop' && '💻'}
                    {category.name === 'Phụ kiện' && '🎧'}
                    {category.name === 'Tablet' && '📲'}
                    {category.name === 'Đồng hồ thông minh' && '⌚'}
                  </span>
                </div>
                <h3 className="mt-4 font-medium text-gray-900">{category.name}</h3>
                <p className="mt-1 text-sm text-gray-500">{category.product_count} sản phẩm</p>
              </Link>
            ))}
          </div>
        </div>
      </section>
      
      {/* Featured Products */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-2xl font-bold text-gray-900">Sản phẩm nổi bật</h2>
            <Link
              to="/products"
              className="text-primary-600 hover:text-primary-700 font-medium flex items-center"
            >
              Xem tất cả
              <ArrowRight className="ml-1 w-4 h-4" />
            </Link>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="bg-white rounded-xl p-4 animate-pulse">
                  <div className="aspect-square bg-gray-200 rounded-lg"></div>
                  <div className="h-4 bg-gray-200 rounded mt-4"></div>
                  <div className="h-4 bg-gray-200 rounded mt-2 w-2/3"></div>
                  <div className="h-8 bg-gray-200 rounded mt-4"></div>
                </div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {featuredProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>
      </section>
      
      {/* CTA Section (guest only) */}
      {!isAuthenticated && (
        <section className="bg-gray-900 text-white py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold">Bắt đầu mua sắm ngay hôm nay</h2>
            <p className="mt-4 text-gray-400 max-w-2xl mx-auto">
              Đăng ký tài khoản để nhận thông tin khuyến mãi và tận hưởng trải nghiệm mua sắm tuyệt vời cùng Mini Shop.
            </p>
            <Link
              to="/register"
              className="mt-8 inline-flex items-center px-8 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
            >
              Đăng ký miễn phí
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </section>
      )}
    </div>
  )
}

export default HomePage
