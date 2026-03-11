<template>
  <div class="shipment-records-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <file-text-outlined />
          发货记录
        </span>
      </template>
      
      <template #extra>
        <a-space>
          <a-button @click="loadShipments()" :loading="loading">
            <reload-outlined />
            刷新
          </a-button>
          <a-button type="primary" @click="exportData">
            <download-outlined />
            导出Excel
          </a-button>
        </a-space>
      </template>

      <!-- 筛选条件 -->
      <div class="filter-section">
        <a-form layout="inline" :model="filters">
          <a-form-item label="客户筛选">
            <a-select
              v-model:value="filters.customer_name"
              placeholder="全部客户"
              style="width: 200px"
              allow-clear
              show-search
              option-filter-prop="label"
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
          </a-form-item>
          
          <a-form-item label="开始日期">
            <a-date-picker
              v-model:value="filters.start_date"
              placeholder="选择开始日期"
              style="width: 150px"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </a-form-item>
          
          <a-form-item label="结束日期">
            <a-date-picker
              v-model:value="filters.end_date"
              placeholder="选择结束日期"
              style="width: 150px"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </a-form-item>
          
          <a-form-item>
            <a-space>
              <a-button type="primary" @click="loadShipments()" :loading="loading">
                <search-outlined />
                查询
              </a-button>
              <a-button @click="clearFilters">
                <clear-outlined />
                清除筛选
              </a-button>
            </a-space>
          </a-form-item>
        </a-form>
      </div>

      <!-- 发货记录表格 -->
      <a-table
        :columns="columns"
        :data-source="shipments"
        :pagination="paginationConfig"
        :loading="loading"
        row-key="trans_id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'trans_id'">
            <a-tag color="blue">#{{ record.trans_id }}</a-tag>
          </template>
          
          <template v-if="column.key === 'product_name'">
            <span style="font-weight: 500;">{{ record.product_name }}</span>
          </template>
          
          <template v-if="column.key === 'quantity'">
            <a-statistic
              :value="record.quantity"
              :value-style="{ 
                color: '#1890ff',
                fontSize: '14px',
                fontWeight: 'bold'
              }"
            />
          </template>
          
          <template v-if="column.key === 'customer_name'">
            <a-tag v-if="record.customer_name" color="green">
              {{ record.customer_name }}
            </a-tag>
            <span v-else style="color: #999;">-</span>
          </template>
          
          <template v-if="column.key === 'operator'">
            <span>
              <user-outlined />
              {{ record.operator }}
            </span>
          </template>
          
          <template v-if="column.key === 'trans_date'">
            <span style="color: #666;">{{ record.trans_date }}</span>
          </template>
          
          <template v-if="column.key === 'note'">
            <span v-if="record.note" style="color: #666;">{{ record.note }}</span>
            <span v-else style="color: #ccc;">-</span>
          </template>
        </template>
        
        <template #emptyText>
          <a-empty description="暂无发货记录">
            <a-button type="primary" @click="$router.push('/shipment')">
              <plus-outlined />
              立即发货
            </a-button>
          </a-empty>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {
  FileTextOutlined,
  ReloadOutlined,
  DownloadOutlined,
  SearchOutlined,
  ClearOutlined,
  UserOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

const shipments = ref([])
const customers = ref([])
const loading = ref(false)
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 0 })

const filters = reactive({
  customer_name: '',
  start_date: '',
  end_date: ''
})

// 表格列配置
const columns = [
  {
    title: '记录ID',
    dataIndex: 'trans_id',
    key: 'trans_id',
    width: 100,
    sorter: true
  },
  {
    title: '产品名称',
    dataIndex: 'product_name',
    key: 'product_name',
    ellipsis: true
  },
  {
    title: '数量',
    dataIndex: 'quantity',
    key: 'quantity',
    width: 100,
    align: 'center',
    sorter: true
  },
  {
    title: '客户名称',
    dataIndex: 'customer_name',
    key: 'customer_name',
    width: 150,
    ellipsis: true
  },
  {
    title: '操作员',
    dataIndex: 'operator',
    key: 'operator',
    width: 120
  },
  {
    title: '发货时间',
    dataIndex: 'trans_date',
    key: 'trans_date',
    width: 160,
    sorter: true
  },
  {
    title: '备注',
    dataIndex: 'note',
    key: 'note',
    ellipsis: true
  }
]

// 分页配置
const paginationConfig = computed(() => ({
  current: pagination.value.page,
  pageSize: pagination.value.per_page,
  total: pagination.value.total,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
  pageSizeOptions: ['10', '20', '50', '100']
}))

const loadShipments = async (page = 1, pageSize = 20) => {
  loading.value = true
  
  try {
    const params = { 
      page,
      per_page: pageSize
    }
    
    if (filters.customer_name) params.customer_name = filters.customer_name
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date

    const { data } = await api.getShipments(params)
    
    if (data.success) {
      shipments.value = data.data
      if (data.pagination) {
        pagination.value = data.pagination
      }
    } else {
      message.error(data.message || '加载发货记录失败')
    }
  } catch (error) {
    console.error('加载发货记录失败:', error)
    message.error('加载发货记录失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (pag, filters, sorter) => {
  loadShipments(pag.current, pag.pageSize)
}

const clearFilters = () => {
  filters.customer_name = ''
  filters.start_date = ''
  filters.end_date = ''
  loadShipments()
}

const exportData = () => {
  try {
    const params = { limit: 1000 }
    if (filters.customer_name) params.customer_name = filters.customer_name
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date
    
    window.location.href = api.exportShipments(params)
    message.success('导出任务已开始，请稍候下载')
  } catch (error) {
    message.error('导出失败，请重试')
  }
}

onMounted(async () => {
  try {
    const { data } = await api.getCustomers()
    if (data.success) {
      customers.value = data.data
    }
  } catch (error) {
    console.error('加载客户列表失败:', error)
    message.error('加载客户列表失败')
  }
  
  loadShipments()
})
</script>

<style scoped>
.shipment-records-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.filter-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

:deep(.ant-form-inline .ant-form-item) {
  margin-right: 16px;
  margin-bottom: 8px;
}

:deep(.ant-form-item-label) {
  font-weight: 500;
}

/* 表格样式优化 */
:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #f5f5f5;
}

/* 标签样式 */
:deep(.ant-tag) {
  border-radius: 4px;
  font-size: 12px;
}

/* 统计数字样式 */
:deep(.ant-statistic-content) {
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .shipment-records-page {
    padding: 16px;
  }
  
  .filter-section {
    padding: 12px;
  }
  
  :deep(.ant-form-inline .ant-form-item) {
    margin-right: 8px;
    margin-bottom: 12px;
  }
  
  :deep(.ant-table-thead > tr > th),
  :deep(.ant-table-tbody > tr > td) {
    padding: 8px 4px;
    font-size: 12px;
  }
}
</style>
