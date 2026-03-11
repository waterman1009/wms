<template>
  <div class="main-layout">
    <TopHeader :user="user" @logout="handleLogout" />
    <div class="content-wrapper">
      <Sidebar :user="user" />
      <div class="main-content">
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

const router = useRouter()
const user = ref(null)

onMounted(() => {
  const userData = sessionStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  }
})

const handleLogout = () => {
  sessionStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

.content-wrapper {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background: #f5f5f5;
}
</style>
