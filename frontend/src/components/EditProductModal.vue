<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h2>编辑产品</h2>
      <MessageAlert :message="message" :type="messageType" />
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>产品名称 *</label>
          <input v-model="form.name" type="text" required>
        </div>
        <div class="form-group">
          <label>单位 *</label>
          <input v-model="form.unit" type="text" required>
        </div>
        <div class="form-group">
          <label>库存数量 *</label>
          <input v-model.number="form.quantity" type="number" min="0" required>
        </div>
        <div class="form-group">
          <label>描述</label>
          <textarea v-model="form.description" rows="2"></textarea>
        </div>

        <div v-if="product.product_type === 'FINISHED'" class="components-section">
          <label>配件配置</label>
          <div class="component-list">
            <div v-for="(comp, index) in form.components" :key="index" class="component-item">
              <AutocompleteInput v-model="comp.component_id" 
                                :items="allComponents"
                                placeholder="输入配件名称搜索..." />
              <input v-model.number="comp.quantity" type="number" min="1" placeholder="数量" required>
              <button type="button" @click="removeComponent(index)">删除</button>
            </div>
          </div>
          <button type="button" @click="addComponent">+ 添加配件</button>
        </div>

        <div class="button-group">
          <button type="submit">保存</button>
          <button type="button" @click="$emit('close')">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from './MessageAlert.vue'
import AutocompleteInput from './AutocompleteInput.vue'

const props = defineProps({
  product: Object
})

const emit = defineEmits(['close', 'saved'])

const form = reactive({
  name: props.product.name,
  unit: props.product.unit,
  quantity: props.product.quantity,
  description: props.product.description || '',
  components: []
})

const allComponents = ref([])
const message = ref('')
const messageType = ref('success')

onMounted(async () => {
  if (props.product.product_type === 'FINISHED') {
    try {
      const [componentsRes, productCompsRes] = await Promise.all([
        api.getProducts({ type: 'COMPONENT' }),
        api.getProductComponents(props.product.product_id)
      ])
      
      allComponents.value = componentsRes.data.data
      form.components = productCompsRes.data.data.map(c => ({
        component_id: c.component_id,
        quantity: c.required_quantity
      }))
    } catch (error) {
      console.error('加载配件失败:', error)
    }
  }
})

const addComponent = () => {
  form.components.push({ component_id: null, quantity: 1 })
}

const removeComponent = (index) => {
  form.components.splice(index, 1)
}

const handleSubmit = async () => {
  try {
    const { data } = await api.updateProduct(props.product.product_id, form)
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      setTimeout(() => emit('saved'), 1000)
    }
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
  }
}
</script>

<style scoped>
.components-section {
  margin-top: 15px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 5px;
}

.component-list {
  max-height: 250px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.component-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.button-group {
  margin-top: 20px;
}
</style>
