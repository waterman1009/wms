<template>
  <div>
    <h2>📋 发货记录</h2>
    
    <div class="filter-bar">
      <select v-model="filters.customer_name">
        <option value="">全部客户</option>
        <option v-for="c in customers" :key="c.customer_id" :value="c.name">
          {{ c.name }}
        </option>
      </select>
      <label style="margin-left: 15px;">开始日期：</label>
      <input v-model="filters.start_date" type="date">
      <label style="margin-left: 10px;">结束日期：</label>
      <input v-model="filters.end_date" type="date">
      <button @click="loadShipments">🔍 查询</button>
      <button @click="clearFilters">清除筛选</button>
      <button @click="exportData">📥 导出Excel</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>记录ID</th>
          <th>产品名称</th>
          <th>数量</th>
          <th>客户名称</th>
          <th>操作员</th>
          <th>发货时间</th>
          <th>备注</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="shipments.length === 0">
          <td colspan="7" style="text-align:center">暂无发货记录</td>
        </tr>
        <tr v-for="s in shipments" :key="s.trans_id">
          <td>{{ s.trans_id }}</td>
          <td>{{ s.product_name }}</td>
          <td>{{ s.quantity }}</td>
          <td>{{ s.customer_name || '-' }}</td>
          <td>{{ s.operator }}</td>
          <td>{{ s.trans_date }}</td>
          <td>{{ s.note || '-' }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'

const shipments = ref([])
const customers = ref([])
const filters = reactive({
  customer_name: '',
  start_date: '',
  end_date: ''
})

const loadShipments = async () => {
  try {
    const params = { limit: 100 }
    if (filters.customer_name) params.customer_name = filters.customer_name
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date

    const { data } = await api.getShipments(params)
    shipments.value = data.data
  } catch (error) {
    console.error('加载发货记录失败:', error)
  }
}

const clearFilters = () => {
  filters.customer_name = ''
  filters.start_date = ''
  filters.end_date = ''
  loadShipments()
}

const exportData = () => {
  const params = { limit: 1000 }
  if (filters.customer_name) params.customer_name = filters.customer_name
  if (filters.start_date) params.start_date = filters.start_date
  if (filters.end_date) params.end_date = filters.end_date
  
  window.location.href = api.exportShipments(params)
}

onMounted(async () => {
  try {
    const { data } = await api.getCustomers()
    customers.value = data.data
  } catch (error) {
    console.error('加载客户列表失败:', error)
  }
  loadShipments()
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

.filter-bar {
  margin: 15px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-bar select,
.filter-bar input {
  width: auto;
}
</style>
