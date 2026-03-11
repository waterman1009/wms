<template>
  <div class="shipment-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <car-outlined />
          成品发货
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
          label="客户名称"
          name="customer_name"
          :rules="[{ required: true, message: '请选择客户' }]"
        >
          <a-select
            v-model:value="form.customer_name"
            placeholder="请选择客户"
            show-search
            option-filter-prop="label"
            size="large"
          >
            <a-select-option
              v-for="c in customers"
              :key="c.customer_id"
              :value="c.name"
              :label="c.name"
            >
              {{ c.name }}
            </a-select-option>
          </a-select>
          <div class="form-help">
            如需添加新客户，请前往"客户管理"页面
          </div>
        </a-form-item>
        
        <a-form-item
          label="发货产品"
          name="shipments"
          :rules="[{ required: true, message: '请至少添加一个成品' }]"
        >
          <div class="shipment-list">
            <a-card
              v-for="(item, index) in form.shipments"
              :key="index"
              size="small"
              class="shipment-item"
            >
              <template #extra>
                <a-button
                  v-if="form.shipments.length > 1"
                  type="text"
                  danger
                  size="small"
                  @click="removeShipment(index)"
                >
                  <delete-outlined />
                </a-button>
              </template>
              
              <a-row :gutter="16" align="middle">
                <a-col :span="14">
                  <a-select
                    v-model:value="item.product_name"
                    placeholder="选择成品"
                    show-search
                    option-filter-prop="label"
                    style="width: 100%"
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
                </a-col>
                <a-col :span="10">
                  <a-input-number
                    v-model:value="item.quantity"
                    placeholder="数量"
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
            @click="addShipment"
            style="margin-top: 16px"
          >
            <plus-outlined />
            添加成品
          </a-button>
        </a-form-item>
        
        <a-form-item label="备注" name="note">
          <a-textarea
            v-model:value="form.note"
            placeholder="如：订单号、运输方式等"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
          <a-space>
            <a-button type="primary" html-type="submit" size="large">
              <car-outlined />
              确认发货
            </a-button>
            <a-button @click="resetForm">
              重置
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>

    <ShipmentConfirmModal
      v-if="showConfirmModal"
      :shipments="form.shipments"
      :customer-name="form.customer_name"
      :note="form.note"
      @confirm="confirmShipment"
      @cancel="showConfirmModal = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  CarOutlined,
  PlusOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'
import api from '../api'
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

const resetForm = () => {
  form.customer_name = ''
  form.shipments = [{ product_name: '', quantity: null }]
  form.note = ''
}

const handleSubmit = () => {
  if (form.shipments.length === 0) {
    message.value = '请至少添加一个成品'
    messageType.value = 'error'
    return
  }
  
  // 验证所有发货项都已填写
  const hasEmptyItems = form.shipments.some(item => 
    !item.product_name || !item.quantity || item.quantity <= 0
  )
  
  if (hasEmptyItems) {
    message.value = '请完整填写所有发货项信息'
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
      resetForm()
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
      api.getProducts({ type: 'FINISHED', per_page: 1000 })
    ])
    customers.value = customersRes.data.data
    finishedProducts.value = productsRes.data.data
  } catch (error) {
    console.error('加载数据失败:', error)
    message.value = '加载数据失败，请刷新页面重试'
    messageType.value = 'error'
  }
})
</script>

<style scoped>
.shipment-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.form-help {
  margin-top: 4px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 12px;
}

.shipment-list {
  max-height: 400px;
  overflow-y: auto;
}

.shipment-item {
  margin-bottom: 12px;
}

.shipment-item:last-child {
  margin-bottom: 0;
}

/* 自定义滚动条 */
.shipment-list::-webkit-scrollbar {
  width: 6px;
}

.shipment-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.shipment-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.shipment-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
