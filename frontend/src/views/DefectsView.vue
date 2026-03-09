<template>
  <div>
    <h2>⚠️ 配件损耗登记</h2>
    <MessageAlert :message="message" :type="messageType" />
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>配件损耗列表 *</label>
        <div class="defect-list">
          <div v-for="(defect, index) in form.defects" :key="index" class="component-item">
            <AutocompleteInput v-model="defect.component_id" 
                              :items="allComponents"
                              placeholder="输入配件名称搜索..."
                              style="flex: 2;" />
            <input v-model.number="defect.quantity" type="number" min="1" placeholder="损耗数量" required style="flex: 1;">
            <button type="button" @click="removeDefect(index)">删除</button>
          </div>
        </div>
        <button type="button" @click="addDefect">+ 添加配件</button>
      </div>
      
      <div class="form-group">
        <label>备注（损耗原因）</label>
        <textarea v-model="form.note" rows="2" placeholder="如：破损、过期、质量不合格等"></textarea>
      </div>
      
      <button type="submit">提交损耗记录</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'
import AutocompleteInput from '../components/AutocompleteInput.vue'

const form = reactive({
  defects: [{ component_id: null, quantity: null }],
  note: ''
})

const allComponents = ref([])
const message = ref('')
const messageType = ref('success')

const addDefect = () => {
  form.defects.push({ component_id: null, quantity: null })
}

const removeDefect = (index) => {
  form.defects.splice(index, 1)
}

const handleSubmit = async () => {
  if (form.defects.length === 0) {
    message.value = '请至少添加一个配件损耗'
    messageType.value = 'error'
    return
  }

  try {
    const defects = form.defects.map(d => ({
      component_name: allComponents.value.find(c => c.product_id === d.component_id)?.name,
      quantity: d.quantity
    }))

    const { data } = await api.recordDefects({ defects, note: form.note })
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      form.defects = [{ component_id: null, quantity: null }]
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

.defect-list {
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
