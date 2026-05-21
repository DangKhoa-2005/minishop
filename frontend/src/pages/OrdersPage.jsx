import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Package, ChevronRight, Search } from 'lucide-react'
import { ordersAPI } from '../services/api'

function OrdersPage() {
  const [orders, setOrders] = useState([])
  const [pagination, setPagination] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [statusFilter, setStatusFilter] = useState('')
  const [currentPage, setCurrentPage] = useState(1)
  
  useEffect(() => {
    loadOrders()
  }, [statusFilter, currentPage])
  
  const loadOrders = async () => {
    setIsLoading(true)
    try {
      const params = { page: currentPage, per_page: 10 }
      if (statusFilter) params.status = statusFilter
      
      const response = await ordersAPI.getAll(params)
      setOrders(response.data.data.orders)
      setPagination(response.data.data.pagination)
    } catch (error) {
      console.error('Failed to load orders:', error)
    } finally {
      setIsLoading(false)
    }
  }
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }
  
  const formatDate = (dateString) => {
    // If dateString doesn't end with Z, append it to treat as UTC
    const utcDateString = dateString.endsWith('Z') ? dateString : `${dateString}Z`
    return new Date(utcDateString).toLocaleDateString('vi-VN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
      timeZone: 'Asia/Ho_Chi_Minh'
    })
  }
  
  const getStatusColor = (status) => {
    const colors = {
      confirmed: 'bg-blue-100 text-blue-700',
      shipping: 'bg-purple-100 text-purple-700',
      delivered: 'bg-green-100 text-green-700',
      cancelled: 'bg-red-100 text-red-700'
    }
    return colors[status] || 'bg-gray-100 text-gray-700'
  }
  
  const statuses = [
    { value: '', label: 'Tất cả' },
    { value: 'confirmed', label: 'Đã xác nhận' },
    { value: 'shipping', label: 'Đang giao' },
    { value: 'delivered', label: 'Đã giao' },
    { value: 'cancelled', label: 'Đã hủy' }
  ]
  
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fadeIn">
      <h1 className="text-2xl font-bold text-gray-900 mb-8">Đơn hàng của tôi</h1>
      
      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6 rounded-md">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-blue-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3 text-sm text-blue-700">
            <p>
              <strong>Lưu ý:</strong> Bạn có thể chủ động hủy đơn hàng vì lý do sai sót khi đặt mua. Tuy nhiên, xin lưu ý rằng <strong>đơn hàng chỉ có thể được hủy trong trạng thái "Đã xác nhận"</strong> (tức là trước khi shop bàn giao cho đơn vị vận chuyển). Nếu có vấn đề phát sinh sau khi đơn đã giao, vui lòng liên hệ trực tiếp với chúng tôi hoặc xem <Link to="/support/returns" className="font-semibold underline text-blue-800">Chính sách đổi trả</Link>.
            </p>
          </div>
        </div>
      </div>
      
      {/* Filters */}
      <div className="mb-6 flex flex-wrap gap-2">
        {statuses.map((status) => (
          <button
            key={status.value}
            onClick={() => {
              setStatusFilter(status.value)
              setCurrentPage(1)
            }}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              statusFilter === status.value
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {status.label}
          </button>
        ))}
      </div>
      
      {/* Orders List */}
      {isLoading ? (
        <div className="space-y-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-white rounded-xl p-6 animate-pulse">
              <div className="h-6 w-32 bg-gray-200 rounded mb-4"></div>
              <div className="h-4 w-full bg-gray-200 rounded mb-2"></div>
              <div className="h-4 w-2/3 bg-gray-200 rounded"></div>
            </div>
          ))}
        </div>
      ) : orders.length > 0 ? (
        <>
          <div className="space-y-4">
            {orders.map((order) => (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                className="block bg-white rounded-xl shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-4">
                      <span className="text-sm font-medium text-gray-500">
                        Đơn hàng #{order.user_order_number || order.id}
                      </span>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
                        {order.status_display}
                      </span>
                    </div>
                    <ChevronRight className="w-5 h-5 text-gray-400" />
                  </div>
                  
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500">
                    <span>{formatDate(order.created_at)}</span>
                    <span>•</span>
                    <span>{order.item_count} sản phẩm</span>
                    <span>•</span>
                    <span className="font-semibold text-gray-900">
                      {formatPrice(order.total_amount)}
                    </span>
                  </div>
                  
                  {/* First few items preview */}
                  <div className="mt-4 flex gap-2">
                    {order.items?.slice(0, 4).map((item) => (
                      <div
                        key={item.id}
                        className="w-14 h-14 rounded-lg overflow-hidden bg-gray-100"
                      >
                        <img
                          src={item.product?.image_url || 'https://via.placeholder.com/56'}
                          alt={item.product?.name}
                          className="w-full h-full object-cover"
                        />
                      </div>
                    ))}
                    {order.items?.length > 4 && (
                      <div className="w-14 h-14 rounded-lg bg-gray-100 flex items-center justify-center text-sm text-gray-500">
                        +{order.items.length - 4}
                      </div>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
          
          {/* Pagination */}
          {pagination.pages > 1 && (
            <div className="flex justify-center mt-8 gap-2">
              <button
                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Trước
              </button>
              
              <span className="px-4 py-2 text-gray-600">
                Trang {currentPage} / {pagination.pages}
              </span>
              
              <button
                onClick={() => setCurrentPage(p => Math.min(pagination.pages, p + 1))}
                disabled={currentPage === pagination.pages}
                className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Sau
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-16">
          <Package className="w-24 h-24 text-gray-300 mx-auto" />
          <h2 className="mt-6 text-xl font-semibold text-gray-900">
            Chưa có đơn hàng nào
          </h2>
          <p className="mt-2 text-gray-500">
            Bạn chưa đặt đơn hàng nào. Hãy bắt đầu mua sắm!
          </p>
          <Link
            to="/products"
            className="mt-6 inline-block px-6 py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 transition-colors"
          >
            Khám phá sản phẩm
          </Link>
        </div>
      )}
    </div>
  )
}

export default OrdersPage
