import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/',
      name: 'inventory',
      component: () => import('../views/InventoryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/inventory',
      redirect: '/'
    },
    {
      path: '/add-product',
      name: 'add-product',
      component: () => import('../views/AddProductView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/stock-in',
      name: 'stock-in',
      component: () => import('../views/StockInView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/stock-out',
      name: 'stock-out',
      component: () => import('../views/StockOutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/defects',
      name: 'defects',
      component: () => import('../views/DefectsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/shipment',
      name: 'shipment',
      component: () => import('../views/ShipmentView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/shipment-records',
      name: 'shipment-records',
      component: () => import('../views/ShipmentRecordsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('../views/HistoryView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/customers',
      name: 'customers',
      component: () => import('../views/CustomersView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/UsersView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(sessionStorage.getItem('user') || 'null')
  
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else if (to.meta.requiresAdmin && user && !['ADMIN', 'MANAGER'].includes(user.role)) {
    next('/')
  } else {
    next()
  }
})

export default router
