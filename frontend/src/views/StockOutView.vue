<template>
  <div class="stock-out-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <send-outlined />
          生产出库
        </span>
      </template>
      
      <a-alert
        v-if="message"
        :message="message"
        :type="messageType"
        show-icon
        closable
        style="margin-bottom: 24px"
        @close="message = ''"
      />
      
      <a-form
        :model="form"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
        @finish="handleSubmit"
      >
        <a-form-item
          label="选择成品"
          name="product_name"
          :rules="[{ required: true, message: '请选择要生产的成品' }]"
        >
          <a-select
            v-model:value="form.product_name"
            placeholder="请选择成品"
            show-search
            option-filter-prop="label"
            size="large"
          >
            <a-select-option
              v-for="p in finishedProducts"
              :key="p.product_id"
              :value="p.name"
              :label="p.name"
            >
              {{ p.name }} (库存: {{ p.quantity }})
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item
          label="生产分配"
          name="assignments"
          :rules="[{ required: true, message: '请至少添加一个生产人员' }]"
        >
          <div class="assignment-list">
            <a-card
              v-for="(assign, index) in form.assignments"
              :key="index"
              size="small"
              class="assignment-item"
            >
              <template #extra>
                <a-button
                  v-if="form.assignments.length > 1"
                  type="text"
                  danger
                  size="small"
                  @click="removeAssignment(index)"
                >
                  <delete-outlined />
                </a-button>
              </template>
              
              <a-row :gutter="16" align="middle">
                <a-col :span="14">
                  <a-select
                    v-model:value="assign.assigned_to"
                    placeholder="选择生产人员"
                    show-search
                    option-filter-prop="label"
                    style="width: 100%"
                  >
                    <a-select-option
                      v-for="w in workers"
                      :key="w.user_id"
                      :value="w.real_name"
                      :label="w.real_name"
                    >
                      {{ w.real_name }}
                    </a-select-option>
                  </a-select>
                </a-col>
                <a-col :span="10">
                  <a-input-number
                    v-model:value="assign.quantity"
                    placeholder="生产数量"
                    :min="1"
                    style="width: 100%"
                  />
                </a-col>
              </a-row>
            </a-card>
          </div>
          
          <a-button
            type="dashed"
            block
            @click="addAssignment"
            style="margin-top: 16px"
          >
            <plus-outlined />
            添加生产人员
          </a-button>
        </a-form-item>
        
        <a-form-item label="备注" name="note">
          <a-textarea
            v-model:value="form.note"
            placeholder="生产说明、注意事项等"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
          <a-space>
            <a-button type="primary" html-type="submit" size="large">
              <send-outlined />
              开始生产（配件出库）
            </a-button>
            <a-button @click="resetForm">
              重置
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  SendOutlined,
  PlusOutlined,
  DeleteOutlined,
  UserOutlined
} from '@ant-design/icons-vue'
import api from '../api'

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

const resetForm = () => {
  form.product_name = ''
  form.assignments = [{ assigned_to: '', quantity: null }]
  form.note = ''
}

const handleSubmit = async () => {
  if (form.assignments.length === 0) {
    message.value = '请至少添加一个生产人员分配'
    messageType.value = 'error'
    return
  }

  // 验证所有分配都已填写
  const hasEmptyAssignments = form.assignments.some(assign => 
    !assign.assigned_to || !assign.quantity || assign.quantity <= 0
  )
  
  if (hasEmptyAssignments) {
    message.value = '请完整填写所有生产人员分配信息'
    messageType.value = 'error'
    return
  }

  try {
    const { data } = await api.stockOut(form)
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      resetForm()
    }
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
  }
}

onMounted(async () => {
  try {
    const [productsRes, workersRes] = await Promise.all([
      api.getProducts({ type: 'FINISHED', per_page: 1000 }),
      api.getUsers('WORKER')
    ])
    finishedProducts.value = productsRes.data.data
    workers.value = workersRes.data.data
  } catch (error) {
    console.error('加载数据失败:', error)
    message.value = '加载数据失败，请刷新页面重试'
    messageType.value = 'error'
  }
})
</script>

<style scoped>
.stock-out-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.assignment-list {
  max-height: 400px;
  overflow-y: auto;
}

.assignment-item {
  margin-bottom: 12px;
}

.assignment-item:last-child {
  margin-bottom: 0;
}

/* 自定义滚动条 */
.assignment-list::-webkit-scrollbar {
  width: 6px;
}

.assignment-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.assignment-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.assignment-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
