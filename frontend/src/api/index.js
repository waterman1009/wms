import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  withCredentials: true  // 重要：携带 cookie 用于 session
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      sessionStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // 用户相关
  login: (data) => api.post('/login', data),
  logout: () => api.post('/logout'),
  getCurrentUser: () => api.get('/current-user'),
  getUsers: (role) => api.get('/users', { params: { role } }),
  addUser: (data) => api.post('/users', data),
  deleteUser: (id) => api.delete(`/users/${id}`),

  // 产品相关
  getProducts: (params) => api.get('/products', { params }),
  getProduct: (id) => api.get(`/products/${id}`),
  addProduct: (data) => api.post('/products', data),
  updateProduct: (id, data) => api.put(`/products/${id}`, data),
  deleteProduct: (id) => api.delete(`/products/${id}`),
  getProductComponents: (id) => api.get(`/products/${id}/components`),
  importProducts: (formData) => api.post('/products/import', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000  // 导入可能需要更长时间
  }),

  // 库存操作
  stockIn: (data) => api.post('/stock/in', data),
  stockOut: (data) => api.post('/stock/out', data),
  recordDefects: (data) => api.post('/defects', data),

  // 发货相关
  createShipment: (data) => api.post('/shipments', data),
  getShipments: (params) => api.get('/shipments', { params }),
  exportShipments: (params) => `/api/shipments/export?${new URLSearchParams(params)}`,

  // 交易历史
  getTransactions: (params) => api.get('/transactions', { params }),
  cancelTransaction: (id) => api.post(`/transactions/${id}/cancel`),
  exportTransactions: (params) => `/api/transactions/export?${new URLSearchParams(params)}`,

  // 客户管理
  getCustomers: (search) => api.get('/customers', { params: { search } }),
  getCustomer: (id) => api.get(`/customers/${id}`),
  addCustomer: (data) => api.post('/customers', data),
  updateCustomer: (id, data) => api.put(`/customers/${id}`, data),
  deleteCustomer: (id) => api.delete(`/customers/${id}`)
}
