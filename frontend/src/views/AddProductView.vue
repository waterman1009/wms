<template>
  <div>
    <h2>➕ 添加新产品</h2>
    <MessageAlert :message="message" :type="messageType" />
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>产品名称 *</label>
        <input v-model="form.name" type="text" required>
      </div>
      <div class="form-group">
        <label>产品类型 *</label>
        <select v-model="form.product_type" required>
          <option value="">-- 请选择 --</option>
          <option value="COMPONENT">配件</option>
          <option value="FINISHED">成品</option>
        </select>
      </div>
      <div class="form-group">
        <label>单位 *</label>
        <input v-model="form.unit" type="text" placeholder="如: 个/箱/kg" required>
      </div>
      <div class="form-group">
        <label>描述</label>
        <textarea v-model="form.description" rows="2"></textarea>
      </div>

      <div v-if="form.product_type === 'FINISHED'" class="components-section">
        <label>配件配置</label>
        <div class="component-list">
          <div v-for="(comp, index) in form.components" :key="index" class="component-item">
            <select v-model="comp.component_id" required>
              <option value="">-- 选择配件 --</option>
              <option v-for="c in allComponents" :key="c.product_id" :value="c.product_id">
                {{ c.name }} (库存: {{ c.quantity }})
              </option>
            </select>
            <input v-model.number="comp.quantity" type="number" min="1" placeholder="数量" required>
            <button type="button" @click="removeComponent(index)">删除</button>
          </div>
        </div>
        <button type="button" @click="addComponent">+ 添加配件</button>
      </div>

      <button type="submit">添加产品</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'

const form = reactive({
  name: '',
  product_type: '',
  unit: '',
  description: '',
  components: []
})

const allComponents = ref([])
const message = ref('')
const messageType = ref('success')

watch(() => form.product_type, (newType) => {
  if (newType === 'FINISHED' && form.components.length === 0) {
    addComponent()
  }
})

const addComponent = () => {
  form.components.push({ component_id: null, quantity: 1 })
}

const removeComponent = (index) => {
  form.components.splice(index, 1)
}

const handleSubmit = async () => {
  if (form.product_type === 'FINISHED' && form.components.length === 0) {
    message.value = '成品必须至少配置一个配件'
    messageType.value = 'error'
    return
  }

  try {
    const { data } = await api.addProduct(form)
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      Object.assign(form, {
        name: '',
        product_type: '',
        unit: '',
        description: '',
        components: []
      })
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

.components-section {
  margin-top: 15px;
  padding: 15px;
  background: #f9f9f9;
  border-radius: 5px;
}

.component-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.component-item {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  align-items: center;
}

.component-item select,
.component-item input {
  flex: 1;
}
</style>
