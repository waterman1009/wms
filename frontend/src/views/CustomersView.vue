<template>
  <div class="customers-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <team-outlined />
          客户管理
        </span>
      </template>
      
      <template #extra>
        <a-space>
          <a-button @click="loadCustomers()" :loading="loading">
            <reload-outlined />
            刷新
          </a-button>
          <a-button type="primary" @click="showAddModal = true">
            <plus-outlined />
            添加客户
          </a-button>
        </a-space>
      </template>

      <!-- 搜索筛选 -->
      <div class="search-section">
        <a-form layout="inline">
          <a-form-item label="搜索客户">
            <a-input
              v-model:value="searchQuery"
              placeholder="搜索客户名称、联系人或电话..."
              style="width: 300px"
              allow-clear
              @input="searchCustomers"
            >
              <template #prefix>
                <search-outlined />
              </template>
            </a-input>
          </a-form-item>
        </a-form>
      </div>

      <!-- 客户列表表格 -->
      <a-table
        :columns="columns"
        :data-source="displayedCustomers"
        :pagination="paginationConfig"
        :loading="loading"
        row-key="customer_id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'name'">
            <span style="font-weight: 500; color: #1890ff;">{{ record.name }}</span>
          </template>
          
          <template v-if="column.key === 'contact_person'">
            <span v-if="record.contact_person">
              <user-outlined />
              {{ record.contact_person }}
            </span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'phone'">
            <span v-if="record.phone">
              <phone-outlined />
              {{ record.phone }}
            </span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'address'">
            <span v-if="record.address">
              <environment-outlined />
              {{ record.address }}
            </span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'note'">
            <span v-if="record.note" style="color: #666;">{{ record.note }}</span>
            <span v-else style="color: #ccc;">-</span>
          </template>
          
          <template v-if="column.key === 'created_at'">
            <span style="color: #666;">{{ record.created_at }}</span>
          </template>
          
          <template v-if="column.key === 'action'">
            <a-space>
              <a-tooltip title="编辑客户信息">
                <a-button type="primary" size="small" @click="editCustomer(record)">
                  <edit-outlined />
                  编辑
                </a-button>
              </a-tooltip>
              
              <a-popconfirm
                title="确定要删除这个客户吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="deleteCustomer(record.customer_id)"
              >
                <template #description>
                  <div style="color: #ff4d4f;">
                    删除后无法恢复，请谨慎操作！
                  </div>
                </template>
                <a-tooltip title="删除客户">
                  <a-button type="primary" danger size="small">
                    <delete-outlined />
                    删除
                  </a-button>
                </a-tooltip>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
        
        <template #emptyText>
          <a-empty description="暂无客户信息">
            <a-button type="primary" @click="showAddModal = true">
              <plus-outlined />
              添加第一个客户
            </a-button>
          </a-empty>
        </template>
      </a-table>
    </a-card>

    <!-- 客户信息弹窗 -->
    <CustomerModal 
      v-if="showAddModal || showEditModal"
      :customer="selectedCustomer"
      @close="closeModal"
      @saved="handleSaved" 
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  TeamOutlined,
  ReloadOutlined,
  PlusOutlined,
  SearchOutlined,
  UserOutlined,
  PhoneOutlined,
  EnvironmentOutlined,
  EditOutlined,
  DeleteOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'
import CustomerModal from '../components/CustomerModal.vue'

const customers = ref([])
const searchQuery = ref('')
const showAddModal = ref(false)
const showEditModal = ref(false)
const selectedCustomer = ref(null)
const loading = ref(false)

const displayedCustomers = computed(() => {
  if (!searchQuery.value) return customers.value
  
  const query = searchQuery.value.toLowerCase()
  return customers.value.filter(c => 
    c.name.toLowerCase().includes(query) ||
    (c.contact_person && c.contact_person.toLowerCase().includes(query)) ||
    (c.phone && c.phone.includes(query))
  )
})

// 表格列配置
const columns = [
  {
    title: '客户名称',
    dataIndex: 'name',
    key: 'name',
    ellipsis: true,
    sorter: (a, b) => a.name.localeCompare(b.name)
  },
  {
    title: '联系人',
    dataIndex: 'contact_person',
    key: 'contact_person',
    width: 120
  },
  {
    title: '电话',
    dataIndex: 'phone',
    key: 'phone',
    width: 140
  },
  {
    title: '地址',
    dataIndex: 'address',
    key: 'address',
    ellipsis: true
  },
  {
    title: '备注',
    dataIndex: 'note',
    key: 'note',
    ellipsis: true
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 160,
    sorter: (a, b) => new Date(a.created_at) - new Date(b.created_at)
  },
  {
    title: '操作',
    key: 'action',
    width: 160,
    fixed: 'right'
  }
]

// 分页配置
const paginationConfig = {
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
  pageSizeOptions: ['10', '20', '50', '100'],
  defaultPageSize: 20
}

const loadCustomers = async () => {
  loading.value = true
  try {
    const { data } = await api.getCustomers()
    if (data.success) {
      customers.value = data.data
    } else {
      message.error(data.message || '加载客户列表失败')
    }
  } catch (error) {
    console.error('加载客户列表失败:', error)
    message.error('加载客户列表失败，请重试')
  } finally {
    loading.value = false
  }
}

const searchCustomers = () => {
  // 搜索由 computed 自动处理
}

const editCustomer = (customer) => {
  selectedCustomer.value = customer
  showEditModal.value = true
}

const deleteCustomer = async (id) => {
  try {
    const { data } = await api.deleteCustomer(id)
    
    if (data.success) {
      message.success(data.message)
      loadCustomers()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    console.error('删除客户失败:', error)
    message.error('删除失败: ' + error.message)
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  selectedCustomer.value = null
}

const handleSaved = () => {
  closeModal()
  loadCustomers()
}

onMounted(() => {
  loadCustomers()
})
</script>

<style scoped>
.customers-page {
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

.search-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #fafafa;
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

:deep(.ant-input) {
  border-radius: 6px;
}

:deep(.ant-btn) {
  border-radius: 6px;
  font-weight: 500;
}

:deep(.ant-popconfirm .ant-popover-inner-content) {
  padding: 16px;
}

:deep(.ant-tooltip) {
  font-size: 12px;
}
</style>
