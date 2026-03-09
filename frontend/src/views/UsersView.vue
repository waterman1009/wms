<template>
  <div>
    <h2>👥 用户管理</h2>
    <button @click="showAddForm = !showAddForm" style="margin: 15px 0;">+ 添加用户</button>
    
    <div v-if="showAddForm" class="add-form">
      <h3 style="color:#667eea; margin-bottom:15px;">添加新用户</h3>
      <MessageAlert :message="addMessage" :type="addMessageType" />
      
      <form @submit.prevent="handleAddUser">
        <div class="form-group">
          <label>用户名 *</label>
          <input v-model="addForm.username" type="text" required>
        </div>
        <div class="form-group">
          <label>密码 *</label>
          <input v-model="addForm.password" type="password" required>
        </div>
        <div class="form-group">
          <label>真实姓名 *</label>
          <input v-model="addForm.real_name" type="text" required>
        </div>
        <div class="form-group">
          <label>角色 *</label>
          <select v-model="addForm.role" required>
            <option value="">-- 请选择 --</option>
            <option value="ADMIN">系统管理员</option>
            <option value="MANAGER">仓库管理员</option>
            <option value="WORKER">生产人员</option>
          </select>
        </div>
        <button type="submit">添加</button>
        <button type="button" @click="showAddForm = false">取消</button>
      </form>
    </div>

    <table>
      <thead>
        <tr>
          <th>用户ID</th>
          <th>用户名</th>
          <th>真实姓名</th>
          <th>角色</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="users.length === 0">
          <td colspan="6" style="text-align:center">暂无用户</td>
        </tr>
        <tr v-for="u in users" :key="u.user_id">
          <td>{{ u.user_id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.real_name }}</td>
          <td>{{ getRoleName(u.role) }}</td>
          <td>{{ u.created_at }}</td>
          <td>
            <button v-if="u.username !== 'admin'" 
                    class="action-btn delete-btn" 
                    @click="deleteUser(u.user_id)">
              删除
            </button>
            <span v-else>-</span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '../api'
import MessageAlert from '../components/MessageAlert.vue'

const users = ref([])
const showAddForm = ref(false)
const addForm = reactive({
  username: '',
  password: '',
  real_name: '',
  role: ''
})
const addMessage = ref('')
const addMessageType = ref('success')

const getRoleName = (role) => {
  const roleNames = {
    'ADMIN': '系统管理员',
    'MANAGER': '仓库管理员',
    'WORKER': '生产人员'
  }
  return roleNames[role] || role
}

const loadUsers = async () => {
  try {
    const { data } = await api.getUsers()
    users.value = data.data
  } catch (error) {
    console.error('加载用户列表失败:', error)
  }
}

const handleAddUser = async () => {
  try {
    const { data } = await api.addUser(addForm)
    addMessage.value = data.message
    addMessageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      setTimeout(() => {
        showAddForm.value = false
        Object.assign(addForm, { username: '', password: '', real_name: '', role: '' })
        loadUsers()
      }, 1000)
    }
  } catch (error) {
    addMessage.value = '操作失败: ' + error.message
    addMessageType.value = 'error'
  }
}

const deleteUser = async (id) => {
  if (!confirm('确定要删除这个用户吗？')) return

  try {
    const { data } = await api.deleteUser(id)
    alert(data.message)
    if (data.success) loadUsers()
  } catch (error) {
    alert('删除失败: ' + error.message)
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
h2 {
  color: #2c3e50;
  padding-bottom: 15px;
  margin-bottom: 25px;
  border-bottom: 3px solid #667eea;
  font-size: 24px;
}

.add-form {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
}
</style>
