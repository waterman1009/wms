<template>
  <div>
    <h2>📤 生产出库</h2>
    <MessageAlert :message="message" :type="messageType" />
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>选择要生产的成品 *</label>
        <select v-model="form.product_name" required>
          <option value="">-- 请选择成品 --</option>
          <option v-for="p in finishedProducts" :key="p.product_id" :value="p.name">
            {{ p.name }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>生产人员分配 *</label>
        <div class="assignment-list">
          <div v-for="(assign, index) in form.assignments" :key="index" class="component-item">
            <select v-model="assign.assigned_to" required style="flex: 2;">
              <option value="">-- 选择生产人员 --</option>
              <option v-for="w in workers" :key="w.user_id" :value="w.real_name">
                {{ w.real_name }}
              </option>
            </select>
            <input v-model.number="assign.quantity" type="number" min="1" placeholder="数量" required style="flex: 1;">
            <button type="button" @click="removeAssignment(index)">删除</button>
          </div>
        </div>
        <button type="button" @click="addAssignment">+ 添加生产人员</button>
      </div>
      
      <div class="form-group">
        <label>备注</label>
        <textarea v-model="form.note" rows="2"></textarea>
      </div>
      
      <button type="submit">开始生产（配件出库）</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'

const form = reactive({
  product_name: '',
  assignments: [{ assigned_to: '', quantity: null }],
  note: ''
})

const finishedProducts = ref([])
const workers = ref([])
const message = ref('')
const messageType = ref('success')

const addAssignment = () => {
  form.assignments.push({ assigned_to: '', quantity: null })
}

const removeAssignment = (index) => {
  form.assignments.splice(index, 1)
}

const handleSubmit = async () => {
  if (form.assignments.length === 0) {
    message.value = '请至少添加一个生产人员分配'
    messageType.value = 'error'
    return
  }

  try {
    const { data } = await api.stockOut(form)
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      form.product_name = ''
      form.assignments = [{ assigned_to: '', quantity: null }]
      form.note = ''
    }
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
  }
}

onMounted(async () => {
  try {
    const [productsRes, workersRes] = await Promise.all([
      api.getProducts({ type: 'FINISHED' }),
      api.getUsers('WORKER')
    ])
    finishedProducts.value = productsRes.data.data
    workers.value = workersRes.data.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
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

.assignment-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
  padding: 5px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
}

.component-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}
</style>
