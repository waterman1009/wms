<template>
  <div>
    <h2>📜 交易历史</h2>
    
    <div class="date-filter">
      <div class="filter-item">
        <label>📅 开始日期：</label>
        <input v-model="filters.start_date" type="date">
      </div>
      <div class="filter-item">
        <label>📅 结束日期：</label>
        <input v-model="filters.end_date" type="date">
      </div>
      <button @click="loadHistory()">🔍 应用筛选</button>
      <button @click="clearDateFilter">🔄 清除筛选</button>
    </div>

    <div class="toolbar">
      <div>
        <button @click="loadHistory('all')">全部</button>
        <button @click="loadHistory('IN')">入库记录</button>
        <button @click="loadHistory('OUT')">配件出库</button>
        <button @click="loadHistory('PRODUCTION')">生产记录</button>
        <button @click="loadHistory('SHIPMENT')">发货记录</button>
        <button @click="loadHistory('DEFECT')">次品记录</button>
      </div>
      <button @click="exportData" class="btn-export">📥 导出Excel</button>
    </div>

    <table>
      <thead>
        <tr>
          <th>记录ID</th>
          <th>产品名称</th>
          <th>类型</th>
          <th>数量</th>
          <th>操作员</th>
          <th>分配给</th>
          <th>次品数</th>
          <th>时间</th>
          <th>备注</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="transactions.length === 0">
          <td colspan="10" style="text-align:center">暂无记录</td>
        </tr>
        <tr v-for="trans in transactions" :key="trans.trans_id">
          <td>{{ trans.trans_id }}</td>
          <td>{{ trans.product_name }}</td>
          <td><span :class="['badge', getTypeClass(trans.trans_type)]">{{ getTypeName(trans.trans_type) }}</span></td>
          <td>{{ trans.quantity }}</td>
          <td>{{ trans.operator }}</td>
          <td>{{ trans.assigned_to || '-' }}</td>
          <td>{{ trans.defect_quantity || '-' }}</td>
          <td>{{ trans.trans_date }}</td>
          <td>{{ trans.note || '-' }}</td>
          <td>
            <button v-if="canCancel(trans)" 
                    class="btn-danger action-btn" 
                    @click="cancelTransaction(trans.trans_id)">
              取消
            </button>
            <span v-else style="color: #999;">-</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../api'

const transactions = ref([])
const currentType = ref('all')
const filters = reactive({
  start_date: '',
  end_date: ''
})

const currentUser = computed(() => {
  return JSON.parse(sessionStorage.getItem('user') || 'null')
})

const canCancel = (trans) => {
  return currentUser.value && 
         ['ADMIN', 'MANAGER'].includes(currentUser.value.role) && 
         trans.trans_type !== 'CANCEL'
}

const getTypeClass = (type) => {
  const map = {
    'IN': 'in',
    'OUT': 'out',
    'PRODUCTION': 'production',
    'SHIPMENT': 'shipment',
    'CANCEL': 'defect',
    'DEFECT': 'defect'
  }
  return map[type] || 'defect'
}

const getTypeName = (type) => {
  const map = {
    'IN': '入库',
    'OUT': '配件出库',
    'PRODUCTION': '生产',
    'SHIPMENT': '发货',
    'CANCEL': '已取消',
    'DEFECT': '次品'
  }
  return map[type] || type
}

const loadHistory = async (type) => {
  if (type !== undefined) currentType.value = type

  try {
    const params = {}
    if (currentType.value !== 'all') params.type = currentType.value
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date

    const { data } = await api.getTransactions(params)
    transactions.value = data.data
  } catch (error) {
    console.error('加载交易历史失败:', error)
  }
}

const clearDateFilter = () => {
  filters.start_date = ''
  filters.end_date = ''
  loadHistory()
}

const cancelTransaction = async (id) => {
  if (!confirm('确定要取消这条交易记录吗？\n\n取消后将自动恢复库存，此操作不可撤销！')) return

  try {
    const { data } = await api.cancelTransaction(id)
    alert(data.message)
    if (data.success) loadHistory()
  } catch (error) {
    alert('操作失败: ' + error.message)
  }
}

const exportData = () => {
  const params = { limit: 1000 }
  if (currentType.value !== 'all') params.type = currentType.value
  if (filters.start_date) params.start_date = filters.start_date
  if (filters.end_date) params.end_date = filters.end_date
  
  window.location.href = api.exportTransactions(params)
}

onMounted(() => {
  loadHistory('all')
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

.date-filter {
  margin: 15px 0;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-item label {
  font-weight: bold;
  color: #667eea;
  margin: 0;
}

.filter-item input {
  width: auto;
  padding: 8px;
}

.toolbar {
  margin: 15px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-export {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}
</style>
