<template>
  <div class="add-product-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <plus-outlined />
          添加新产品
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
          label="产品名称"
          name="name"
          :rules="[{ required: true, message: '请输入产品名称' }]"
        >
          <a-input
            v-model:value="form.name"
            placeholder="请输入产品名称"
            size="large"
            show-count
            :maxlength="50"
          />
        </a-form-item>
        
        <a-form-item
          label="产品类型"
          name="product_type"
          :rules="[{ required: true, message: '请选择产品类型' }]"
        >
          <a-select
            v-model:value="form.product_type"
            placeholder="请选择产品类型"
            size="large"
          >
            <a-select-option value="COMPONENT">
              <div class="type-option">
                <tool-outlined />
                <span>配件</span>
              </div>
            </a-select-option>
            <a-select-option value="FINISHED">
              <div class="type-option">
                <gift-outlined />
                <span>成品</span>
              </div>
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item
          label="单位"
          name="unit"
          :rules="[{ required: true, message: '请输入单位' }]"
        >
          <a-input
            v-model:value="form.unit"
            placeholder="如: 个/箱/kg"
            size="large"
            show-count
            :maxlength="10"
          />
        </a-form-item>
        
        <a-form-item label="描述" name="description">
          <a-textarea
            v-model:value="form.description"
            placeholder="产品描述信息"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>

        <a-form-item
          v-if="form.product_type === 'FINISHED'"
          label="配件配置"
          name="components"
        >
          <a-card size="small" title="成品配件关系">
            <template #extra>
              <a-button type="link" @click="addComponent">
                <plus-outlined />
                添加配件
              </a-button>
            </template>
            
            <div v-if="form.components.length === 0" class="empty-components">
              <a-empty description="暂未配置配件">
                <a-button type="primary" @click="addComponent">
                  <plus-outlined />
                  添加配件
                </a-button>
              </a-empty>
            </div>
            
            <div v-else class="component-list">
              <a-card
                v-for="(comp, index) in form.components"
                :key="index"
                size="small"
                class="component-item"
              >
                <template #extra>
                  <a-button
                    type="text"
                    danger
                    size="small"
                    @click="removeComponent(index)"
                  >
                    <delete-outlined />
                  </a-button>
                </template>
                
                <a-row :gutter="16" align="middle">
                  <a-col :span="16">
                    <a-select
                      v-model:value="comp.component_id"
                      placeholder="选择配件"
                      show-search
                      option-filter-prop="label"
                      style="width: 100%"
                    >
                      <a-select-option
                        v-for="c in allComponents"
                        :key="c.product_id"
                        :value="c.product_id"
                        :label="c.name"
                      >
                        {{ c.name }} (库存: {{ c.quantity }})
                      </a-select-option>
                    </a-select>
                  </a-col>
                  <a-col :span="8">
                    <a-input-number
                      v-model:value="comp.quantity"
                      placeholder="所需数量"
                      :min="1"
                      style="width: 100%"
                    />
                  </a-col>
                </a-row>
              </a-card>
            </div>
          </a-card>
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
          <a-space>
            <a-button type="primary" html-type="submit" size="large">
              <plus-outlined />
              添加产品
            </a-button>
            <a-button @click="resetForm">
              重置
            </a-button>
            <a-button @click="$router.push('/inventory')">
              返回库存
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import {
  PlusOutlined,
  DeleteOutlined,
  ToolOutlined,
  GiftOutlined
} from '@ant-design/icons-vue'
import api from '../api'

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
  } else if (newType === 'COMPONENT') {
    form.components = []
  }
})

const addComponent = () => {
  form.components.push({ component_id: null, quantity: 1 })
}

const removeComponent = (index) => {
  form.components.splice(index, 1)
}

const resetForm = () => {
  Object.assign(form, {
    name: '',
    product_type: '',
    unit: '',
    description: '',
    components: []
  })
  message.value = ''
}

const handleSubmit = async () => {
  if (form.product_type === 'FINISHED' && form.components.length === 0) {
    message.value = '成品必须至少配置一个配件'
    messageType.value = 'error'
    return
  }

  // 验证成品配件配置
  if (form.product_type === 'FINISHED') {
    const hasEmptyComponents = form.components.some(comp => 
      !comp.component_id || !comp.quantity || comp.quantity <= 0
    )
    
    if (hasEmptyComponents) {
      message.value = '请完整填写所有配件配置信息'
      messageType.value = 'error'
      return
    }
  }

  try {
    const { data } = await api.addProduct(form)
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
    const { data } = await api.getProducts({ type: 'COMPONENT', per_page: 1000 })
    allComponents.value = data.data
  } catch (error) {
    console.error('加载配件失败:', error)
    message.value = '加载配件数据失败，请刷新页面重试'
    messageType.value = 'error'
  }
})
</script>

<style scoped>
.add-product-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 8px;
}

.empty-components {
  padding: 24px;
  text-align: center;
}

.component-list {
  max-height: 400px;
  overflow-y: auto;
}

.component-item {
  margin-bottom: 12px;
}

.component-item:last-child {
  margin-bottom: 0;
}

/* 自定义滚动条 */
.component-list::-webkit-scrollbar {
  width: 6px;
}

.component-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.component-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.component-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
