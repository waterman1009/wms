<template>
  <div>
    <h2>👥 客户管理</h2>
    <button @click="showAddModal = true" style="margin: 15px 0;">+ 添加客户</button>
    
    <div class="form-group" style="max-width: 400px;">
      <input v-model="searchQuery" type="text" placeholder="搜索客户名称、联系人或电话..." @input="searchCustomers">
    </div>

    <table>
      <thead>
        <tr>
          <th>客户名称</th>
          <th>联系人</th>
          <th>电话</th>
          <th>地址</th>
          <th>备注</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="displayedCustomers.length === 0">
          <td colspan="7" style="text-align:center">暂无客户</td>
        </tr>
        <tr v-for="c in displayedCustomers" :key="c.customer_id">
          <td>{{ c.name }}</td>
          <td>{{ c.contact_person || '-' }}</td>
          <td>{{ c.phone || '-' }}</td>
          <td>{{ c.address || '-' }}</td>
          <td>{{ c.note || '-' }}</td>
          <td>{{ c.created_at }}</td>
          <td>
            <button class="action-btn edit-btn" @click="editCustomer(c)">编辑</button>
            <button class="action-btn delete-btn" @click="deleteCustomer(c.customer_id)">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <CustomerModal v-if="showAddModal || showEditModal"
                   :customer="selectedCustomer"
                   @close="closeModal"
                   @saved="handleSaved" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'
import CustomerModal from '../components/CustomerModal.vue'

const customers = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedCustomer = ref(null)

const displayedCustomers = computed(() => {
  if (!searchQuery.value) return customers.value
  
  const query = searchQuery.value.toLowerCase()
  return customers.value.filter(c => 
    c.name.toLowerCase().includes(query) ||
    (c.contact_person && c.contact_person.toLowerCase().includes(query)) ||
    (c.phone && c.phone.includes(query))
  )
})

const loadCustomers = async () => {
  try {
    const { data } = await api.getCustomers()
    customers.value = data.data
  } catch (error) {
    console.error('加载客户列表失败:', error)
  }
}

const searchCustomers = () => {
  // 搜索由 computed 自动处理
}

const editCustomer = (customer) => {
  selectedCustomer.value = customer
  showEditModal.value = true
}

const deleteCustomer = async (id) => {
  if (!confirm('确定要删除这个客户吗？')) return

  try {
    const { data } = await api.deleteCustomer(id)
    alert(data.message)
    if (data.success) loadCustomers()
  } catch (error) {
    alert('删除失败: ' + error.message)
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  selectedCustomer.value = null
}

const handleSaved = () => {
  closeModal()
  loadCustomers()
}

onMounted(() => {
  loadCustomers()
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
</style>
