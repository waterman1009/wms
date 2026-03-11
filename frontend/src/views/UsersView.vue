<template>
  <div class="users-page">
    <a-card>
      <template #title>
        <span class="page-title">
          <team-outlined />
          用户管理
        </span>
      </template>
      
      <template #extra>
        <a-button type="primary" @click="showAddModal = true">
          <user-add-outlined />
          添加用户
        </a-button>
      </template>
      
      <a-table
        :columns="columns"
        :data-source="users"
        :loading="loading"
        row-key="user_id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'role'">
            <a-tag :color="getRoleColor(record.role)">
              {{ getRoleText(record.role) }}
            </a-tag>
          </template>
          
          <template v-if="column.key === 'created_at'">
            {{ formatDate(record.created_at) }}
          </template>
          
          <template v-if="column.key === 'action'">
            <a-space>
              <a-button type="primary" size="small">
                <edit-outlined />
                编辑
              </a-button>
              <a-popconfirm
                v-if="record.username !== 'admin'"
                title="确定要删除这个用户吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="deleteUser(record.user_id)"
              >
                <a-button type="primary" danger size="small">
                  <delete-outlined />
                  删除
                </a-button>
              </a-popconfirm>
              <span v-else>-</span>
            </a-space>
          </template>
        </template>
        
        <template #emptyText>
          <a-empty description="暂无用户数据">
            <a-button type="primary" @click="showAddModal = true">
              <user-add-outlined />
              添加用户
            </a-button>
          </a-empty>
        </template>
      </a-table>
    </a-card>

    <!-- 添加用户模态框 -->
    <a-modal
      v-model:open="showAddModal"
      title="添加新用户"
      :confirm-loading="submitting"
      @ok="handleAddUser"
      @cancel="resetAddForm"
    >
      <a-form
        :model="addForm"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-item
          label="用户名"
          name="username"
          :rules="[{ required: true, message: '请输入用户名' }]"
        >
          <a-input
            v-model:value="addForm.username"
            placeholder="请输入用户名"
          />
        </a-form-item>
        
        <a-form-item
          label="密码"
          name="password"
          :rules="[{ required: true, message: '请输入密码' }]"
        >
          <a-input-password
            v-model:value="addForm.password"
            placeholder="请输入密码"
          />
        </a-form-item>
        
        <a-form-item
          label="真实姓名"
          name="real_name"
          :rules="[{ required: true, message: '请输入真实姓名' }]"
        >
          <a-input
            v-model:value="addForm.real_name"
            placeholder="请输入真实姓名"
          />
        </a-form-item>
        
        <a-form-item
          label="角色"
          name="role"
          :rules="[{ required: true, message: '请选择角色' }]"
        >
          <a-select
            v-model:value="addForm.role"
            placeholder="请选择角色"
          >
            <a-select-option value="ADMIN">
              <div class="role-option">
                <safety-certificate-outlined />
                <span>系统管理员</span>
              </div>
            </a-select-option>
            <a-select-option value="MANAGER">
              <div class="role-option">
                <user-outlined />
                <span>仓库管理员</span>
              </div>
            </a-select-option>
            <a-select-option value="WORKER">
              <div class="role-option">
                <team-outlined />
                <span>生产人员</span>
              </div>
            </a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  TeamOutlined,
  UserAddOutlined,
  EditOutlined,
  DeleteOutlined,
  SafetyCertificateOutlined,
  UserOutlined
} from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import api from '../api'

const users = ref([])
const loading = ref(false)
const showAddModal = ref(false)
const submitting = ref(false)

const addForm = reactive({
  username: '',
  password: '',
  real_name: '',
  role: ''
})

const columns = [
  {
    title: 'ID',
    dataIndex: 'user_id',
    key: 'user_id',
    width: 80
  },
  {
    title: '用户名',
    dataIndex: 'username',
    key: 'username'
  },
  {
    title: '真实姓名',
    dataIndex: 'real_name',
    key: 'real_name'
  },
  {
    title: '角色',
    dataIndex: 'role',
    key: 'role',
    width: 120,
    filters: [
      { text: '系统管理员', value: 'ADMIN' },
      { text: '仓库管理员', value: 'MANAGER' },
      { text: '生产人员', value: 'WORKER' }
    ]
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at',
    width: 180
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    fixed: 'right'
  }
]

const getRoleColor = (role) => {
  const colors = {
    'ADMIN': 'red',
    'MANAGER': 'blue',
    'WORKER': 'green'
  }
  return colors[role] || 'default'
}

const getRoleText = (role) => {
  const texts = {
    'ADMIN': '系统管理员',
    'MANAGER': '仓库管理员',
    'WORKER': '生产人员'
  }
  return texts[role] || role
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const resetAddForm = () => {
  Object.assign(addForm, {
    username: '',
    password: '',
    real_name: '',
    role: ''
  })
}

const loadUsers = async () => {
  loading.value = true
  try {
    const { data } = await api.getUsers()
    if (data.success) {
      users.value = data.data
    }
  } catch (error) {
    console.error('加载用户失败:', error)
    message.error('加载用户数据失败')
  } finally {
    loading.value = false
  }
}

const handleAddUser = async () => {
  // 简单验证
  if (!addForm.username || !addForm.password || !addForm.real_name || !addForm.role) {
    message.error('请填写完整信息')
    return
  }

  submitting.value = true
  try {
    const { data } = await api.addUser(addForm)
    if (data.success) {
      message.success(data.message)
      showAddModal.value = false
      resetAddForm()
      loadUsers()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('添加用户失败: ' + error.message)
  } finally {
    submitting.value = false
  }
}

const deleteUser = async (userId) => {
  try {
    const { data } = await api.deleteUser(userId)
    if (data.success) {
      message.success(data.message)
      loadUsers()
    } else {
      message.error(data.message)
    }
  } catch (error) {
    message.error('删除用户失败: ' + error.message)
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-page {
  padding: 24px;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
}

.role-option {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
