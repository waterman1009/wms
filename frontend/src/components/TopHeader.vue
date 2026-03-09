<template>
  <div class="top-header">
    <h1>📦 仓库管理系统</h1>
    <div class="user-info">
      <span v-if="user">{{ user.real_name }} ({{ getRoleName(user.role) }})</span>
      <button class="logout-btn" @click="$emit('logout')">退出登录</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: Object
})

defineEmits(['logout'])

const getRoleName = (role) => {
  const roleNames = {
    'ADMIN': '系统管理员',
    'MANAGER': '仓库管理员',
    'WORKER': '生产人员'
  }
  return roleNames[role] || role
}
</script>

<style scoped>
.top-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.top-header h1 {
  font-size: 1.8em;
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.user-info span {
  font-size: 14px;
}

.logout-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  margin: 0;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: none;
}
</style>
