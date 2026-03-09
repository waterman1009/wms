<template>
  <div>
    <TopHeader :user="currentUser" @logout="handleLogout" />
    <div class="main-container">
      <Sidebar :user="currentUser" />
      <div class="content-area">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import TopHeader from '../components/TopHeader.vue'
import Sidebar from '../components/Sidebar.vue'
import api from '../api'

const router = useRouter()
const currentUser = ref(null)

onMounted(async () => {
  try {
    const { data } = await api.getCurrentUser()
    if (data.success) {
      currentUser.value = data.user
      sessionStorage.setItem('user', JSON.stringify(data.user))
    }
  } catch (error) {
    router.push('/login')
  }
})

const handleLogout = async () => {
  try {
    await api.logout()
    sessionStorage.removeItem('user')
    router.push('/login')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}
</script>

<style scoped>
.main-container {
  display: flex;
  height: calc(100vh - 70px);
}

.content-area {
  flex: 1;
  background: white;
  overflow-y: auto;
  padding: 30px;
}
</style>
