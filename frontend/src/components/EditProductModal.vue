<template>
  <a-modal
    :open="true"
    title="编辑产品"
    :footer="null"
    width="800px"
    @cancel="$emit('close')"
  >
    <a-form
      :model="form"
      layout="vertical"
      @finish="handleSubmit"
    >
      <a-row :gutter="16">
        <a-col :span="8">
          <a-form-item label="产品名称" required>
            <a-input v-model:value="form.name" placeholder="请输入产品名称" />
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item label="单位" required>
            <a-input v-model:value="form.unit" placeholder="请输入单位" />
          </a-form-item>
        </a-col>
        <a-col :span="6">
          <a-form-item label="库存数量" required>
            <a-input-number 
              v-model:value="form.quantity" 
              :min="0" 
              style="width: 100%"
              placeholder="库存数量"
            />
          </a-form-item>
        </a-col>
        <a-col :span="4">
          <a-form-item label="产品类型">
            <a-tag :color="product.product_type === 'COMPONENT' ? 'blue' : 'green'" style="font-size: 12px; padding: 2px 6px;">
              {{ product.product_type === 'COMPONENT' ? '配件' : '成品' }}
            </a-tag>
          </a-form-item>
        </a-col>
      </a-row>

      <a-form-item label="描述">
        <a-textarea 
          v-model:value="form.description" 
          :rows="2" 
          placeholder="请输入产品描述"
        />
      </a-form-item>

      <!-- 成品配件配置 -->
      <div v-if="product.product_type === 'FINISHED'" class="components-section">
        <a-divider orientation="left">
          <span style="font-size: 14px; font-weight: 600;">配件配置</span>
        </a-divider>
        
        <div v-if="form.components.length > 0" class="component-list">
          <div 
            v-for="(comp, index) in form.components" 
            :key="index" 
            class="component-item"
          >
            <a-row :gutter="12" align="middle">
              <a-col :span="2">
                <div class="component-index">{{ index + 1 }}</div>
              </a-col>
              <a-col :span="14">
                <a-select
                  v-model:value="comp.component_id"
                  placeholder="请选择配件"
                  show-search
                  :filter-option="filterOption"
                  style="width: 100%"
                  size="small"
                >
                  <a-select-option 
                    v-for="component in allComponents" 
                    :key="component.product_id" 
                    :value="component.product_id"
                    :label="component.name"
                  >
                    {{ component.name }} <span style="color: #999;">(库存: {{ component.quantity }})</span>
                  </a-select-option>
                </a-select>
              </a-col>
              <a-col :span="6">
                <a-input-number 
                  v-model:value="comp.quantity" 
                  :min="1" 
                  style="width: 100%"
                  placeholder="数量"
                  size="small"
                />
              </a-col>
              <a-col :span="2">
                <a-button 
                  type="text" 
                  danger 
                  size="small" 
                  @click="removeComponent(index)"
                  style="padding: 0; width: 24px; height: 24px;"
                >
                  <delete-outlined />
                </a-button>
              </a-col>
            </a-row>
          </div>
        </div>

        <a-empty v-else description="暂未配置配件" :image="false" style="margin: 20px 0;">
          <template #description>
            <span style="color: #999; font-size: 12px;">暂未配置配件</span>
          </template>
        </a-empty>

        <a-button 
          type="dashed" 
          block 
          @click="addComponent"
          size="small"
          style="margin-top: 12px; height: 32px;"
        >
          <plus-outlined />
          添加配件
        </a-button>
      </div>

      <a-divider style="margin: 20px 0;" />

      <a-form-item style="margin-bottom: 0; text-align: right;">
        <a-space>
          <a-button @click="$emit('close')">
            取消
          </a-button>
          <a-button type="primary" html-type="submit" :loading="loading">
            <save-outlined />
            保存修改
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { 
  DeleteOutlined, 
  PlusOutlined, 
  SaveOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

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
const loading = ref(false)

// 修复搜索过滤函数 - 解决 [object Object] 问题
const filterOption = (input, option) => {
  const label = option.label || option.children || ''
  return label.toString().toLowerCase().indexOf(input.toLowerCase()) >= 0
}

onMounted(async () => {
  if (props.product.product_type === 'FINISHED') {
    try {
      loading.value = true
      const [componentsRes, productCompsRes] = await Promise.all([
        api.getProducts({ type: 'COMPONENT', per_page: 1000 }),
        api.getProductComponents(props.product.product_id)
      ])
      
      allComponents.value = componentsRes.data.data
      form.components = productCompsRes.data.data.map(c => ({
        component_id: c.component_id,
        quantity: c.required_quantity
      }))
    } catch (error) {
      console.error('加载配件失败:', error)
      message.error('加载配件信息失败')
    } finally {
      loading.value = false
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
  // 验证表单
  if (!form.name || !form.unit || form.quantity < 0) {
    message.error('请填写完整的产品信息')
    return
  }

  // 如果是成品，验证配件配置
  if (props.product.product_type === 'FINISHED' && form.components.length > 0) {
    const hasInvalidComponent = form.components.some(comp => !comp.component_id || !comp.quantity || comp.quantity < 1)
    if (hasInvalidComponent) {
      message.error('请完善配件配置信息')
      return
    }
  }

  try {
    loading.value = true
    const { data } = await api.updateProduct(props.product.product_id, form)
    
    if (data.success) {
      message.success(data.message)
      emit('saved')
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('操作失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.components-section {
  margin-top: 16px;
}

.component-list {
  max-height: 280px;
  overflow-y: auto;
  padding: 8px;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}

.component-item {
  background: white;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  border: 1px solid #e8e8e8;
  transition: all 0.2s;
}

.component-item:hover {
  border-color: #1890ff;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.1);
}

.component-item:last-child {
  margin-bottom: 0;
}

.component-index {
  width: 20px;
  height: 20px;
  background: #1890ff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

:deep(.ant-form-item) {
  margin-bottom: 12px;
}

:deep(.ant-form-item-label) {
  font-weight: 500;
  padding-bottom: 4px;
}

:deep(.ant-form-item-label > label) {
  font-size: 13px;
}

/* 紧凑的表单项间距 */
:deep(.ant-row) {
  margin-bottom: 0;
}

/* 选择框样式优化 */
:deep(.ant-select-selector) {
  border-radius: 4px;
}

:deep(.ant-input-number) {
  border-radius: 4px;
}

/* 删除按钮样式 */
:deep(.ant-btn-text.ant-btn-dangerous) {
  color: #ff4d4f;
  border: 1px solid transparent;
  border-radius: 4px;
}

:deep(.ant-btn-text.ant-btn-dangerous:hover) {
  background: #fff2f0;
  border-color: #ffccc7;
}
</style>
