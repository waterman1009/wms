<template>
  <div class="history-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <history-outlined />
          交易历史
        </span>
      </template>
      
      <template #extra>
        <a-space>
          <a-button @click="loadHistory()" :loading="loading">
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
          <a-form-item label="日期筛选">
            <a-range-picker
              v-model:value="dateRange"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              placeholder="['开始日期', '结束日期']"
              style="width: 240px"
              @change="onDateRangeChange"
            />
          </a-form-item>
          
          <a-form-item>
            <a-space>
              <a-button type="primary" @click="loadHistory()" :loading="loading">
                <search-outlined />
                应用筛选
              </a-button>
              <a-button @click="clearDateFilter">
                <clear-outlined />
                清除筛选
              </a-button>
            </a-space>
          </a-form-item>
        </a-form>
      </div>

      <!-- 交易类型筛选 -->
      <div class="type-filter-section">
        <a-button-group>
          <a-button 
            :type="currentType === 'all' ? 'primary' : 'default'"
            @click="loadHistory('all')"
          >
            <unordered-list-outlined />
            全部
          </a-button>
          <a-button 
            :type="currentType === 'IN' ? 'primary' : 'default'"
            @click="loadHistory('IN')"
          >
            <import-outlined />
            入库记录
          </a-button>
          <a-button 
            :type="currentType === 'OUT' ? 'primary' : 'default'"
            @click="loadHistory('OUT')"
          >
            <export-outlined />
            配件出库
          </a-button>
          <a-button 
            :type="currentType === 'PRODUCTION' ? 'primary' : 'default'"
            @click="loadHistory('PRODUCTION')"
          >
            <tool-outlined />
            生产记录
          </a-button>
          <a-button 
            :type="currentType === 'SHIPMENT' ? 'primary' : 'default'"
            @click="loadHistory('SHIPMENT')"
          >
            <car-outlined />
            发货记录
          </a-button>
          <a-button 
            :type="currentType === 'DEFECT' ? 'primary' : 'default'"
            @click="loadHistory('DEFECT')"
          >
            <warning-outlined />
            次品记录
          </a-button>
        </a-button-group>
      </div>

      <!-- 交易历史表格 -->
      <a-table
        :columns="columns"
        :data-source="transactions"
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
          
          <template v-if="column.key === 'trans_type'">
            <a-tag :color="getTypeColor(record.trans_type)">
              {{ getTypeName(record.trans_type) }}
            </a-tag>
          </template>
          
          <template v-if="column.key === 'quantity'">
            <a-statistic
              :value="record.quantity"
              :value-style="{ 
                color: getQuantityColor(record.trans_type),
                fontSize: '14px',
                fontWeight: 'bold'
              }"
            />
          </template>
          
          <template v-if="column.key === 'operator'">
            <span>
              <user-outlined />
              {{ record.operator }}
            </span>
          </template>
          
          <template v-if="column.key === 'assigned_to'">
            <span v-if="record.assigned_to">
              <team-outlined />
              {{ record.assigned_to }}
            </span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'defect_quantity'">
            <span v-if="record.defect_quantity" style="color: #ff4d4f; font-weight: bold;">
              {{ record.defect_quantity }}
            </span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'trans_date'">
            <span style="color: #666;">{{ record.trans_date }}</span>
          </template>
          
          <template v-if="column.key === 'note'">
            <span v-if="record.note" style="color: #666;">{{ record.note }}</span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'action'">
            <a-popconfirm
              v-if="canCancel(record)"
              title="确定要取消这条交易记录吗？"
              ok-text="确定"
              cancel-text="取消"
              @confirm="cancelTransaction(record.trans_id)"
            >
              <template #description>
                <div style="color: #ff4d4f;">
                  取消后将自动恢复库存，此操作不可撤销！
                </div>
              </template>
              <a-button type="primary" danger size="small">
                <stop-outlined />
                取消
              </a-button>
            </a-popconfirm>
            <span v-else style="color: #ccc;">-</span>
          </template>
        </template>
        
        <template #emptyText>
          <a-empty description="暂无交易记录">
            <a-button type="primary" @click="$router.push('/stock-in')">
              <plus-outlined />
              开始记录
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
  HistoryOutlined,
  ReloadOutlined,
  DownloadOutlined,
  SearchOutlined,
  ClearOutlined,
  UnorderedListOutlined,
  ImportOutlined,
  ExportOutlined,
  ToolOutlined,
  CarOutlined,
  WarningOutlined,
  UserOutlined,
  TeamOutlined,
  StopOutlined,
  PlusOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

const transactions = ref([])
const currentType = ref('all')
const loading = ref(false)
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 0 })
const dateRange = ref([])

const filters = reactive({
  start_date: '',
  end_date: ''
})

const currentUser = computed(() => {
  return JSON.parse(sessionStorage.getItem('user') || 'null')
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
    title: '类型',
    dataIndex: 'trans_type',
    key: 'trans_type',
    width: 100,
    filters: [
      { text: '入库', value: 'IN' },
      { text: '配件出库', value: 'OUT' },
      { text: '生产', value: 'PRODUCTION' },
      { text: '发货', value: 'SHIPMENT' },
      { text: '次品', value: 'DEFECT' },
      { text: '已取消', value: 'CANCEL' }
    ]
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
    title: '操作员',
    dataIndex: 'operator',
    key: 'operator',
    width: 120
  },
  {
    title: '分配给',
    dataIndex: 'assigned_to',
    key: 'assigned_to',
    width: 120
  },
  {
    title: '次品数',
    dataIndex: 'defect_quantity',
    key: 'defect_quantity',
    width: 80,
    align: 'center'
  },
  {
    title: '时间',
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
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    fixed: 'right'
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

const canCancel = (trans) => {
  return currentUser.value && 
         ['ADMIN', 'MANAGER'].includes(currentUser.value.role) && 
         trans.trans_type !== 'CANCEL'
}

const getTypeColor = (type) => {
  const colorMap = {
    'IN': 'green',
    'OUT': 'orange',
    'PRODUCTION': 'blue',
    'SHIPMENT': 'purple',
    'CANCEL': 'red',
    'DEFECT': 'volcano'
  }
  return colorMap[type] || 'default'
}

const getQuantityColor = (type) => {
  const colorMap = {
    'IN': '#52c41a',
    'OUT': '#fa8c16',
    'PRODUCTION': '#1890ff',
    'SHIPMENT': '#722ed1',
    'CANCEL': '#ff4d4f',
    'DEFECT': '#ff4d4f'
  }
  return colorMap[type] || '#666'
}

const getTypeName = (type) => {
  const nameMap = {
    'IN': '入库',
    'OUT': '配件出库',
    'PRODUCTION': '生产',
    'SHIPMENT': '发货',
    'CANCEL': '已取消',
    'DEFECT': '次品'
  }
  return nameMap[type] || type
}

const onDateRangeChange = (dates) => {
  if (dates && dates.length === 2) {
    filters.start_date = dates[0]
    filters.end_date = dates[1]
  } else {
    filters.start_date = ''
    filters.end_date = ''
  }
}

const loadHistory = async (type, page = 1, pageSize = 20) => {
  if (type !== undefined) {
    currentType.value = type
    pagination.value.page = 1
  } else {
    pagination.value.page = page
    pagination.value.per_page = pageSize
  }

  loading.value = true

  try {
    const params = {
      page: pagination.value.page,
      per_page: pagination.value.per_page
    }
    
    if (currentType.value !== 'all') params.type = currentType.value
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date

    const { data } = await api.getTransactions(params)
    
    if (data.success) {
      transactions.value = data.data
      if (data.pagination) {
        pagination.value = data.pagination
      }
    } else {
      message.error(data.message || '加载交易历史失败')
    }
  } catch (error) {
    console.error('加载交易历史失败:', error)
    message.error('加载交易历史失败，请重试')
  } finally {
    loading.value = false
  }
}

const handleTableChange = (pag, filters, sorter) => {
  loadHistory(undefined, pag.current, pag.pageSize)
}

const clearDateFilter = () => {
  dateRange.value = []
  filters.start_date = ''
  filters.end_date = ''
  loadHistory()
}

const cancelTransaction = async (id) => {
  try {
    const { data } = await api.cancelTransaction(id)
    
    if (data.success) {
      message.success(data.message)
      loadHistory()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('操作失败: ' + error.message)
  }
}

const exportData = () => {
  try {
    const params = { limit: 1000 }
    if (currentType.value !== 'all') params.type = currentType.value
    if (filters.start_date) params.start_date = filters.start_date
    if (filters.end_date) params.end_date = filters.end_date
    
    window.location.href = api.exportTransactions(params)
    message.success('导出任务已开始，请稍候下载')
  } catch (error) {
    message.error('导出失败，请重试')
  }
}

onMounted(() => {
  loadHistory('all')
})
</script>

<style scoped>
.history-page {
  padding: 24px;
  background: #f5f5f5;
  min-height: 100vh;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1890ff;
}

.filter-section {
  margin-bottom: 16px;
  padding: 16px;
  background: #fafafa;
  border-radius: 6px;
  border: 1px solid #d9d9d9;
}

.type-filter-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #fff;
  border-radius: 6px;
  border: 1px solid #d9d9d9;
}

:deep(.ant-table) {
  background: #fff;
  border-radius: 6px;
  overflow: hidden;
}

:deep(.ant-table-thead > tr > th) {
  background: #fafafa;
  font-weight: 600;
  color: #262626;
  border-bottom: 2px solid #f0f0f0;
}

:deep(.ant-table-tbody > tr > td) {
  border-bottom: 1px solid #f0f0f0;
}

:deep(.ant-table-tbody > tr:hover > td) {
  background: #f5f5f5;
}

:deep(.ant-statistic-content) {
  font-size: 14px !important;
}

:deep(.ant-tag) {
  border-radius: 4px;
  font-weight: 500;
}

:deep(.ant-btn-group .ant-btn) {
  border-radius: 0;
}

:deep(.ant-btn-group .ant-btn:first-child) {
  border-top-left-radius: 6px;
  border-bottom-left-radius: 6px;
}

:deep(.ant-btn-group .ant-btn:last-child) {
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
}

:deep(.ant-empty) {
  padding: 40px 0;
}

:deep(.ant-card-head) {
  border-bottom: 2px solid #f0f0f0;
}

:deep(.ant-card-head-title) {
  font-size: 18px;
  font-weight: 600;
}

:deep(.ant-form-item-label > label) {
  font-weight: 600;
  color: #262626;
}

:deep(.ant-picker) {
  border-radius: 6px;
}

:deep(.ant-btn) {
  border-radius: 6px;
  font-weight: 500;
}

:deep(.ant-popconfirm .ant-popover-inner-content) {
  padding: 16px;
}
</style>
