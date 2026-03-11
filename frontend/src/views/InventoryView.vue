<template>
  <div class="inventory-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <database-outlined />
          当前库存
        </span>
      </template>
      
      <template #extra>
        <a-space>
          <a-button @click="loadInventory()" :loading="loading">
            <reload-outlined />
            刷新
          </a-button>
          <a-button-group>
            <a-button 
              :type="currentType === null ? 'primary' : 'default'"
              @click="loadInventory(null)"
            >
              全部
            </a-button>
            <a-button 
              :type="currentType === 'COMPONENT' ? 'primary' : 'default'"
              @click="loadInventory('COMPONENT')"
            >
              配件
            </a-button>
            <a-button 
              :type="currentType === 'FINISHED' ? 'primary' : 'default'"
              @click="loadInventory('FINISHED')"
            >
              成品
            </a-button>
          </a-button-group>
        </a-space>
      </template>
      
      <div class="search-bar">
        <a-input-search
          v-model:value="searchQuery"
          placeholder="搜索产品名称..."
          enter-button="搜索"
          size="large"
          style="max-width: 400px"
          @search="searchInventory"
          @clear="clearSearch"
          allow-clear
        />
      </div>
      
      <a-table
        :columns="columns"
        :data-source="products"
        :pagination="paginationConfig"
        :loading="loading"
        :scroll="{ x: 800 }"
        row-key="product_id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'product_type'">
            <a-tag :color="record.product_type === 'COMPONENT' ? 'blue' : 'green'">
              {{ record.product_type === 'COMPONENT' ? '配件' : '成品' }}
            </a-tag>
          </template>
          
          <template v-if="column.key === 'quantity'">
            <a-statistic
              :value="record.quantity"
              :value-style="{ 
                color: record.quantity > 0 ? '#3f8600' : '#cf1322',
                fontSize: '16px',
                fontWeight: 'bold'
              }"
            />
          </template>
          
          <template v-if="column.key === 'description'">
            <span>{{ record.description || '-' }}</span>
          </template>
          
          <template v-if="column.key === 'action'">
            <a-space size="small">
              <a-tooltip title="查看详情">
                <a-button 
                  type="default" 
                  size="small" 
                  @click="viewProductDetails(record)"
                >
                  <eye-outlined />
                </a-button>
              </a-tooltip>
              <a-tooltip title="编辑产品">
                <a-button 
                  type="primary" 
                  size="small" 
                  @click="editProduct(record)"
                >
                  <edit-outlined />
                </a-button>
              </a-tooltip>
              <a-popconfirm
                title="确定要删除这个产品吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="deleteProduct(record.product_id)"
              >
                <a-tooltip title="删除产品">
                  <a-button 
                    type="primary" 
                    danger 
                    size="small"
                  >
                    <delete-outlined />
                  </a-button>
                </a-tooltip>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
        
        <template #emptyText>
          <a-empty description="暂无产品数据">
            <a-button type="primary" @click="$router.push('/add-product')">
              <plus-outlined />
              添加产品
            </a-button>
          </a-empty>
        </template>
      </a-table>
    </a-card>

    <EditProductModal
      v-if="showEditModal"
      :product="selectedProduct"
      @close="showEditModal = false"
      @saved="handleProductSaved"
    />

    <!-- 产品详情模态框 -->
    <a-modal
      v-model:open="showDetailsModal"
      title="产品详情"
      :footer="null"
      width="600px"
    >
      <div v-if="selectedProduct" class="product-details">
        <a-descriptions :column="2" bordered>
          <a-descriptions-item label="产品ID">
            {{ selectedProduct.product_id }}
          </a-descriptions-item>
          <a-descriptions-item label="产品名称">
            {{ selectedProduct.name }}
          </a-descriptions-item>
          <a-descriptions-item label="产品类型">
            <a-tag :color="selectedProduct.product_type === 'COMPONENT' ? 'blue' : 'green'">
              {{ selectedProduct.product_type === 'COMPONENT' ? '配件' : '成品' }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="库存数量">
            <a-statistic
              :value="selectedProduct.quantity"
              :value-style="{ 
                color: selectedProduct.quantity > 0 ? '#3f8600' : '#cf1322',
                fontSize: '16px',
                fontWeight: 'bold'
              }"
            />
          </a-descriptions-item>
          <a-descriptions-item label="单位">
            {{ selectedProduct.unit }}
          </a-descriptions-item>
          <a-descriptions-item label="描述" :span="2">
            {{ selectedProduct.description || '无描述' }}
          </a-descriptions-item>
        </a-descriptions>

        <!-- 成品配件信息 -->
        <div v-if="selectedProduct.product_type === 'FINISHED'" class="components-info">
          <a-divider>配件构成</a-divider>
          
          <a-table
            v-if="productComponents.length > 0"
            :columns="componentColumns"
            :data-source="productComponents"
            :pagination="false"
            size="small"
            row-key="component_id"
          >
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'name'">
                <a-tag color="blue">{{ record.name }}</a-tag>
              </template>
              <template v-if="column.key === 'required_quantity'">
                <a-statistic
                  :value="record.required_quantity"
                  :value-style="{ fontSize: '14px', fontWeight: 'bold' }"
                />
              </template>
            </template>
          </a-table>
          
          <a-empty v-else description="该成品暂未配置配件" />
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import {
  DatabaseOutlined,
  ReloadOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  EyeOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'
import EditProductModal from '../components/EditProductModal.vue'

const products = ref([])
const searchQuery = ref('')
const currentType = ref(null)
const loading = ref(false)
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 0 })
const showEditModal = ref(false)
const showDetailsModal = ref(false)
const selectedProduct = ref(null)
const productComponents = ref([])

const columns = [
  {
    title: 'ID',
    dataIndex: 'product_id',
    key: 'product_id',
    width: 70,
    sorter: true
  },
  {
    title: '产品名称',
    dataIndex: 'name',
    key: 'name',
    ellipsis: true,
    width: 200
  },
  {
    title: '类型',
    dataIndex: 'product_type',
    key: 'product_type',
    width: 80,
    filters: [
      { text: '配件', value: 'COMPONENT' },
      { text: '成品', value: 'FINISHED' }
    ]
  },
  {
    title: '库存',
    dataIndex: 'quantity',
    key: 'quantity',
    width: 100,
    sorter: true,
    align: 'center'
  },
  {
    title: '单位',
    dataIndex: 'unit',
    key: 'unit',
    width: 60
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
    width: 150
  },
  {
    title: '操作',
    key: 'action',
    width: 140,
    fixed: 'right'
  }
]

const paginationConfig = computed(() => ({
  current: pagination.value.page,
  pageSize: pagination.value.per_page,
  total: pagination.value.total,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
  pageSizeOptions: ['10', '20', '50', '100']
}))

// 配件表格列配置
const componentColumns = [
  {
    title: '配件名称',
    dataIndex: 'name',
    key: 'name'
  },
  {
    title: '所需数量',
    dataIndex: 'required_quantity',
    key: 'required_quantity',
    align: 'center',
    width: 120
  }
]

const loadInventory = async (type, page = 1, pageSize = 20) => {
  loading.value = true
  
  if (type !== undefined) {
    currentType.value = type
    pagination.value.page = 1
  } else {
    pagination.value.page = page
    pagination.value.per_page = pageSize
  }

  try {
    const params = { 
      page: pagination.value.page, 
      per_page: pagination.value.per_page 
    }
    if (currentType.value) params.type = currentType.value
    if (searchQuery.value) params.search = searchQuery.value

    const { data } = await api.getProducts(params)
    products.value = data.data
    pagination.value = data.pagination
  } catch (error) {
    console.error('加载库存失败:', error)
    message.error('加载库存失败，请重试')
  } finally {
    loading.value = false
  }
}

const searchInventory = () => {
  loadInventory(undefined, 1)
}

const clearSearch = () => {
  searchQuery.value = ''
  loadInventory(undefined, 1)
}

const handleTableChange = (pag, filters, sorter) => {
  loadInventory(undefined, pag.current, pag.pageSize)
}

const editProduct = (product) => {
  selectedProduct.value = product
  showEditModal.value = true
}

const viewProductDetails = async (product) => {
  selectedProduct.value = product
  
  // 如果是成品，加载配件信息
  if (product.product_type === 'FINISHED') {
    try {
      const { data } = await api.getProductComponents(product.product_id)
      productComponents.value = data.data || []
    } catch (error) {
      console.error('加载配件信息失败:', error)
      message.error('加载配件信息失败')
      productComponents.value = []
    }
  } else {
    productComponents.value = []
  }
  
  showDetailsModal.value = true
}

const deleteProduct = async (id) => {
  try {
    const { data } = await api.deleteProduct(id)
    if (data.success) {
      message.success(data.message)
      loadInventory()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('删除失败: ' + error.message)
  }
}

const handleProductSaved = () => {
  showEditModal.value = false
  loadInventory()
  message.success('产品更新成功')
}

onMounted(() => {
  loadInventory()
})
</script>

<style scoped>
.inventory-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.search-bar {
  margin-bottom: 16px;
}

.product-details {
  padding: 16px 0;
}

.components-info {
  margin-top: 24px;
}

.no-components {
  margin-top: 24px;
}

/* 响应式表格样式 */
:deep(.ant-table-wrapper) {
  overflow-x: auto;
}

:deep(.ant-table-tbody > tr > td) {
  white-space: nowrap;
}

/* 小屏幕适配 */
@media (max-width: 768px) {
  .inventory-page {
    padding: 16px;
  }
  
  :deep(.ant-table-thead > tr > th),
  :deep(.ant-table-tbody > tr > td) {
    padding: 8px 4px;
    font-size: 12px;
  }
  
  :deep(.ant-btn-sm) {
    padding: 0 4px;
    font-size: 12px;
  }
}
</style>
