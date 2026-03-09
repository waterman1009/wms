<template>
  <div>
    <h2>📥 配件入库</h2>
    <MessageAlert :message="message" :type="messageType" />
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>选择配件 * (可输入搜索)</label>
        <AutocompleteInput v-model="form.product_name" 
                          :items="allComponents"
                          placeholder="输入配件名称搜索..." />
      </div>
      <div class="form-group">
        <label>入库数量 *</label>
        <input v-model.number="form.quantity" type="number" min="1" required>
      </div>
      <div class="form-group">
        <label>备注</label>
        <textarea v-model="form.note" rows="2"></textarea>
      </div>
      <button type="submit">确认入库</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'
import AutocompleteInput from '../components/AutocompleteInput.vue'

const form = reactive({
  product_name: '',
  quantity: null,
  note: ''
})

const allComponents = ref([])
const message = ref('')
const messageType = ref('success')

const handleSubmit = async () => {
  try {
    const productName = allComponents.value.find(c => c.product_id === form.product_name)?.name
    if (!productName) {
      message.value = '请选择配件'
      messageType.value = 'error'
      return
    }

    const { data } = await api.stockIn({
      product_name: productName,
      quantity: form.quantity,
      note: form.note
    })
    
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      form.product_name = ''
      form.quantity = null
      form.note = ''
    }
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
  }
}

onMounted(async () => {
  try {
    const { data } = await api.getProducts({ type: 'COMPONENT' })
    allComponents.value = data.data
  } catch (error) {
    console.error('加载配件失败:', error)
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
</style>
