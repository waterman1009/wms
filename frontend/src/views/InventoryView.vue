<template>
  <div>
    <h2>📊 当前库存</h2>
    <div class="toolbar">
      <button @click="loadInventory()">🔄 刷新</button>
      <button @click="loadInventory('COMPONENT')">配件</button>
      <button @click="loadInventory('FINISHED')">成品</button>
      <input v-model="searchQuery" type="text" placeholder="搜索产品名称..." class="search-input">
      <button @click="searchInventory">🔍 搜索</button>
      <button @click="clearSearch">清除</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>产品ID</th>
          <th>产品名称</th>
          <th>类型</th>
          <th>库存数量</th>
          <th>单位</th>
          <th>描述</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="products.length === 0">
          <td colspan="7" style="text-align:center">暂无产品</td>
        </tr>
        <tr v-for="product in products" :key="product.product_id">
          <td>{{ product.product_id }}</td>
          <td>{{ product.name }}</td>
          <td>
            <span :class="['badge', product.product_type === 'COMPONENT' ? 'component' : 'finished']">
              {{ product.product_type === 'COMPONENT' ? '配件' : '成品' }}
            </span>
          </td>
          <td><strong>{{ product.quantity }}</strong></td>
          <td>{{ product.unit }}</td>
          <td>{{ product.description || '-' }}</td>
          <td>
            <button class="action-btn edit-btn" @click="editProduct(product)">编辑</button>
            <button class="action-btn delete-btn" @click="deleteProduct(product.product_id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="pagination.total_pages > 1" class="pagination">
      <span>共 {{ pagination.total }} 条记录，第 {{ pagination.page }} / {{ pagination.total_pages }} 页</span>
      <button v-if="pagination.page > 1" @click="loadInventory(undefined, 1)">首页</button>
      <button v-if="pagination.page > 1" @click="loadInventory(undefined, pagination.page - 1)">上一页</button>
      <button v-for="p in visiblePages" :key="p" 
              :class="{ active: p === pagination.page }"
              @click="loadInventory(undefined, p)">
        {{ p }}
      </button>
      <button v-if="pagination.page < pagination.total_pages" @click="loadInventory(undefined, pagination.page + 1)">下一页</button>
      <button v-if="pagination.page < pagination.total_pages" @click="loadInventory(undefined, pagination.total_pages)">末页</button>
    </div>

    <EditProductModal v-if="showEditModal" 
                      :product="selectedProduct" 
                      @close="showEditModal = false"
                      @saved="handleProductSaved" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import EditProductModal from '../components/EditProductModal.vue'

const products = ref([])
const searchQuery = ref('')
const currentType = ref(null)
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 0 })
const showEditModal = ref(false)
const selectedProduct = ref(null)

const visiblePages = computed(() => {
  const start = Math.max(1, pagination.value.page - 2)
  const end = Math.min(pagination.value.total_pages, pagination.value.page + 2)
  return Array.from({ length: end - start + 1 }, (_, i) => start + i)
})

const loadInventory = async (type, page = 1) => {
  if (type !== undefined) {
    currentType.value = type
    pagination.value.page = 1
  } else {
    pagination.value.page = page
  }

  try {
    const params = { page: pagination.value.page, per_page: 20 }
    if (currentType.value) params.type = currentType.value
    if (searchQuery.value) params.search = searchQuery.value

    const { data } = await api.getProducts(params)
    products.value = data.data
    pagination.value = data.pagination
  } catch (error) {
    console.error('加载库存失败:', error)
  }
}

const searchInventory = () => {
  loadInventory(undefined, 1)
}

const clearSearch = () => {
  searchQuery.value = ''
  loadInventory(undefined, 1)
}

const editProduct = (product) => {
  selectedProduct.value = product
  showEditModal.value = true
}

const deleteProduct = async (id) => {
  if (!confirm('确定要删除这个产品吗？此操作不可恢复！')) return

  try {
    const { data } = await api.deleteProduct(id)
    alert(data.message)
    if (data.success) loadInventory()
  } catch (error) {
    alert('删除失败: ' + error.message)
  }
}

const handleProductSaved = () => {
  showEditModal.value = false
  loadInventory()
}

onMounted(() => {
  loadInventory()
})
</script>

<style scoped>
h2 {
  color: #2c3e50;
  padding-bottom: 15px;
  margin-bottom: 25px;
  border-bottom: 3px solid #667eea;
  font-size: 24px;
}

.toolbar {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.search-input {
  width: 250px;
  margin-left: 20px;
}

.pagination {
  margin-top: 15px;
  text-align: center;
}

.pagination button {
  margin: 0 5px;
  padding: 8px 15px;
}

.pagination button.active {
  background: #667eea;
  color: white;
}
</style>
