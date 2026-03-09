import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MainLayout from '../layouts/MainLayout.vue'

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
      component: MainLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'inventory',
          component: () => import('../views/InventoryView.vue')
        },
        {
          path: 'add-product',
          name: 'add-product',
          component: () => import('../views/AddProductView.vue')
        },
        {
          path: 'stock-in',
          name: 'stock-in',
          component: () => import('../views/StockInView.vue')
        },
        {
          path: 'stock-out',
          name: 'stock-out',
          component: () => import('../views/StockOutView.vue')
        },
        {
          path: 'defects',
          name: 'defects',
          component: () => import('../views/DefectsView.vue')
        },
        {
          path: 'shipment',
          name: 'shipment',
          component: () => import('../views/ShipmentView.vue')
        },
        {
          path: 'shipment-records',
          name: 'shipment-records',
          component: () => import('../views/ShipmentRecordsView.vue')
        },
        {
          path: 'history',
          name: 'history',
          component: () => import('../views/HistoryView.vue')
        },
        {
          path: 'customers',
          name: 'customers',
          component: () => import('../views/CustomersView.vue'),
          meta: { requiresAdmin: true }
        },
        {
          path: 'users',
          name: 'users',
          component: () => import('../views/UsersView.vue'),
          meta: { requiresAdmin: true }
        }
      ]
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
