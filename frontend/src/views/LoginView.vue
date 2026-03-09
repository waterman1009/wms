<template>
  <div class="login-page">
    <div class="login-container">
      <h1>📦 仓库管理系统</h1>
      <div v-if="errorMessage" class="message error">{{ errorMessage }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="username" type="text" required autofocus>
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" required>
        </div>
        <button type="submit">登录</button>
      </form>
      <div class="info">默认账号：admin / admin123</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  try {
    console.log('Attempting login...', { username: username.value })
    const { data } = await api.login({ username: username.value, password: password.value })
    console.log('Login response:', data)
    if (data.success) {
      sessionStorage.setItem('user', JSON.stringify(data.user))
      router.push('/')
    } else {
      errorMessage.value = data.message
    }
  } catch (error) {
    console.error('Login error:', error)
    console.error('Error response:', error.response)
    errorMessage.value = '登录失败: ' + (error.response?.data?.message || error.message)
  }
}
</script>

<style scoped>
.login-page {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  background: white;
  padding: 40px;
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 400px;
}

h1 {
  text-align: center;
  color: #667eea;
  margin-bottom: 30px;
  font-size: 2em;
}

button {
  width: 100%;
}

.info {
  text-align: center;
  margin-top: 20px;
  color: #666;
  font-size: 14px;
}
</style>
