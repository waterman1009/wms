<template>
  <div class="stock-in-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <import-outlined />
          配件入库
        </span>
      </template>
      
      <a-form
        :model="form"
        :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }"
        @finish="handleSubmit"
      >
        <a-form-item
          label="选择配件"
          name="product_name"
          :rules="[{ required: true, message: '请选择配件' }]"
        >
          <a-select
            v-model:value="form.product_name"
            placeholder="输入配件名称搜索..."
            show-search
            size="large"
            :loading="loading"
            option-filter-prop="label"
          >
            <a-select-option
              v-for="c in allComponents"
              :key="c.product_id"
              :value="c.name"
              :label="c.name"
            >
              {{ c.name }} (库存: {{ c.quantity }})
            </a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item
          label="入库数量"
          name="quantity"
          :rules="[
            { required: true, message: '请输入入库数量' },
            { type: 'number', min: 1, message: '数量必须大于0' }
          ]"
        >
          <a-input-number
            v-model:value="form.quantity"
            placeholder="请输入入库数量"
            :min="1"
            :max="999999"
            size="large"
            style="width: 100%"
          />
        </a-form-item>
        
        <a-form-item label="备注" name="note">
          <a-textarea
            v-model:value="form.note"
            placeholder="入库说明、供应商信息等"
            :rows="3"
            show-count
            :maxlength="200"
          />
        </a-form-item>
        
        <a-form-item :wrapper-col="{ offset: 4, span: 20 }">
          <a-space>
            <a-button type="primary" html-type="submit" size="large" :loading="submitting">
              <import-outlined />
              确认入库
            </a-button>
            <a-button @click="resetForm">
              重置
            </a-button>
            <a-button @click="$router.push('/inventory')">
              查看库存
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
      
      <!-- 最近入库记录 -->
      <a-divider>最近入库记录</a-divider>
      
      <a-table
        :columns="recentColumns"
        :data-source="recentRecords"
        :pagination="false"
        size="small"
        :loading="loadingRecords"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'trans_type'">
            <a-tag color="green">入库</a-tag>
          </template>
          <template v-if="column.key === 'quantity'">
            <a-statistic
              :value="record.quantity"
              :value-style="{ color: '#3f8600', fontSize: '14px' }"
            />
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ImportOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

const form = reactive({
  product_name: '',
  quantity: null,
  note: ''
})

const allComponents = ref([])
const recentRecords = ref([])
const loading = ref(false)
const loadingRecords = ref(false)
const submitting = ref(false)

const recentColumns = [
  {
    title: '配件名称',
    dataIndex: 'product_name',
    key: 'product_name'
  },
  {
    title: '类型',
    dataIndex: 'trans_type',
    key: 'trans_type',
    width: 80
  },
  {
    title: '数量',
    dataIndex: 'quantity',
    key: 'quantity',
    width: 100,
    align: 'center'
  },
  {
    title: '操作员',
    dataIndex: 'operator',
    key: 'operator',
    width: 100
  },
  {
    title: '时间',
    dataIndex: 'trans_date',
    key: 'trans_date',
    width: 160
  },
  {
    title: '备注',
    dataIndex: 'note',
    key: 'note',
    ellipsis: true
  }
]

const resetForm = () => {
  form.product_name = ''
  form.quantity = null
  form.note = ''
}

const handleSubmit = async () => {
  submitting.value = true
  
  try {
    const { data } = await api.stockIn({
      product_name: form.product_name,
      quantity: form.quantity,
      note: form.note
    })
    
    if (data.success) {
      message.success(data.message)
      resetForm()
      loadRecentRecords() // 刷新最近记录
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('操作失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

const loadRecentRecords = async () => {
  loadingRecords.value = true
  try {
    const { data } = await api.getTransactions({ type: 'IN', limit: 10 })
    if (data.success) {
      recentRecords.value = data.data
    }
  } catch (error) {
    console.error('加载最近记录失败:', error)
  } finally {
    loadingRecords.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    const [componentsRes] = await Promise.all([
      api.getProducts({ type: 'COMPONENT', per_page: 1000 })
    ])
    allComponents.value = componentsRes.data.data
    
    // 加载最近入库记录
    loadRecentRecords()
  } catch (error) {
    console.error('加载配件失败:', error)
    message.error('加载配件数据失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.stock-in-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}
</style>
