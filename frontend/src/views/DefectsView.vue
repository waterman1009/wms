<template>
  <div class="defects-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <warning-outlined />
          配件损耗登记
        </span>
      </template>
      
      <a-form
        :model="form"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
        @finish="handleSubmit"
      >
        <a-form-item
          label="配件损耗列表"
          name="defects"
          :rules="[{ required: true, message: '请至少添加一个配件损耗' }]"
        >
          <div class="defect-list">
            <div 
              v-for="(defect, index) in form.defects" 
              :key="index" 
              class="defect-item"
            >
              <a-row :gutter="12" align="middle">
                <a-col :span="2">
                  <div class="defect-index">{{ index + 1 }}</div>
                </a-col>
                <a-col :span="14">
                  <a-select
                    v-model:value="defect.component_id"
                    placeholder="请选择配件"
                    show-search
                    option-filter-prop="label"
                    style="width: 100%"
                    size="small"
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
                <a-col :span="6">
                  <a-input-number
                    v-model:value="defect.quantity"
                    :min="1"
                    placeholder="损耗数量"
                    style="width: 100%"
                    size="small"
                  />
                </a-col>
                <a-col :span="2">
                  <a-button
                    type="text"
                    danger
                    size="small"
                    @click="removeDefect(index)"
                    style="padding: 0; width: 24px; height: 24px;"
                  >
                    <delete-outlined />
                  </a-button>
                </a-col>
              </a-row>
            </div>
          </div>

          <a-empty v-if="form.defects.length === 0" description="暂未添加配件损耗" :image="false" style="margin: 20px 0;">
            <template #description>
              <span style="color: #999; font-size: 12px;">暂未添加配件损耗</span>
            </template>
          </a-empty>

          <a-button
            type="dashed"
            block
            @click="addDefect"
            size="small"
            style="margin-top: 12px; height: 32px;"
          >
            <plus-outlined />
            添加配件损耗
          </a-button>
        </a-form-item>

        <a-form-item label="损耗原因" name="note">
          <a-textarea
            v-model:value="form.note"
            placeholder="如：破损、过期、质量不合格等"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
          <a-space>
            <a-button type="primary" html-type="submit" size="large" :loading="submitting">
              <warning-outlined />
              提交损耗记录
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
  WarningOutlined,
  PlusOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

const form = reactive({
  defects: [{ component_id: null, quantity: null }],
  note: ''
})

const allComponents = ref([])
const submitting = ref(false)

const addDefect = () => {
  form.defects.push({ component_id: null, quantity: null })
}

const removeDefect = (index) => {
  if (form.defects.length > 1) {
    form.defects.splice(index, 1)
  }
}

const resetForm = () => {
  form.defects = [{ component_id: null, quantity: null }]
  form.note = ''
}

const handleSubmit = async () => {
  // 验证表单
  if (form.defects.length === 0) {
    message.error('请至少添加一个配件损耗')
    return
  }

  const hasInvalidDefect = form.defects.some(d => !d.component_id || !d.quantity || d.quantity < 1)
  if (hasInvalidDefect) {
    message.error('请完善配件损耗信息')
    return
  }

  submitting.value = true

  try {
    const defects = form.defects.map(d => ({
      component_name: allComponents.value.find(c => c.product_id === d.component_id)?.name,
      quantity: d.quantity
    }))

    const { data } = await api.recordDefects({ defects, note: form.note })
    
    if (data.success) {
      message.success(data.message)
      resetForm()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('操作失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await api.getProducts({ type: 'COMPONENT', per_page: 1000 })
    allComponents.value = data.data
  } catch (error) {
    console.error('加载配件失败:', error)
    message.error('加载配件数据失败，请刷新页面重试')
  }
})
</script>

<style scoped>
.defects-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.defect-list {
  max-height: 280px;
  overflow-y: auto;
  padding: 8px;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid #f0f0f0;
}

.defect-item {
  background: white;
  padding: 8px 12px;
  margin-bottom: 8px;
  border-radius: 4px;
  border: 1px solid #e8e8e8;
  transition: all 0.2s;
}

.defect-item:hover {
  border-color: #faad14;
  box-shadow: 0 2px 4px rgba(250, 173, 20, 0.1);
}

.defect-item:last-child {
  margin-bottom: 0;
}

.defect-index {
  width: 20px;
  height: 20px;
  background: #faad14;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: bold;
}

:deep(.ant-form-item) {
  margin-bottom: 16px;
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
