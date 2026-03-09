<template>
  <div>
    <h2>🚚 成品发货</h2>
    <MessageAlert :message="message" :type="messageType" />
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>客户名称 *</label>
        <select v-model="form.customer_name" required>
          <option value="">请选择客户</option>
          <option v-for="c in customers" :key="c.customer_id" :value="c.name">
            {{ c.name }}
          </option>
        </select>
        <small style="color: #666;">如需添加新客户，请前往"客户管理"页面</small>
      </div>
      
      <div class="form-group">
        <label>发货产品列表 *</label>
        <div class="shipment-list">
          <div v-for="(item, index) in form.shipments" :key="index" class="component-item">
            <input v-model="item.product_name" 
                   list="finished-products-list" 
                   placeholder="选择成品" 
                   required
                   style="flex: 2;">
            <input v-model.number="item.quantity" type="number" min="1" placeholder="数量" required style="flex: 1;">
            <button type="button" @click="removeShipment(index)">删除</button>
          </div>
        </div>
        <button type="button" @click="addShipment">+ 添加成品</button>
        <datalist id="finished-products-list">
          <option v-for="p in finishedProducts" :key="p.product_id" :value="p.name">
            库存: {{ p.quantity }}
          </option>
        </datalist>
      </div>
      
      <div class="form-group">
        <label>备注</label>
        <textarea v-model="form.note" rows="2" placeholder="如：订单号、运输方式等"></textarea>
      </div>
      
      <button type="submit">确认发货</button>
    </form>

    <ShipmentConfirmModal v-if="showConfirmModal"
                          :shipments="form.shipments"
                          :customer-name="form.customer_name"
                          :note="form.note"
                          @confirm="confirmShipment"
                          @cancel="showConfirmModal = false" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'
import ShipmentConfirmModal from '../components/ShipmentConfirmModal.vue'

const form = reactive({
  customer_name: '',
  shipments: [{ product_name: '', quantity: null }],
  note: ''
})

const customers = ref([])
const finishedProducts = ref([])
const message = ref('')
const messageType = ref('success')
const showConfirmModal = ref(false)

const addShipment = () => {
  form.shipments.push({ product_name: '', quantity: null })
}

const removeShipment = (index) => {
  form.shipments.splice(index, 1)
}

const handleSubmit = () => {
  if (form.shipments.length === 0) {
    message.value = '请至少添加一个成品'
    messageType.value = 'error'
    return
  }
  showConfirmModal.value = true
}

const confirmShipment = async () => {
  try {
    const { data } = await api.createShipment(form)
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      form.customer_name = ''
      form.shipments = [{ product_name: '', quantity: null }]
      form.note = ''
    }
    showConfirmModal.value = false
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
    showConfirmModal.value = false
  }
}

onMounted(async () => {
  try {
    const [customersRes, productsRes] = await Promise.all([
      api.getCustomers(),
      api.getProducts({ type: 'FINISHED' })
    ])
    customers.value = customersRes.data.data
    finishedProducts.value = productsRes.data.data
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

.shipment-list {
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
