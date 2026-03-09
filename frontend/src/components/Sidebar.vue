<template>
  <div class="sidebar">
    <div class="nav-section">
      <div class="nav-section-title">库存管理</div>
      <router-link to="/" class="nav-item">
        <span class="icon">📦</span>
        <span>库存查询</span>
      </router-link>
      <router-link to="/add-product" class="nav-item">
        <span class="icon">➕</span>
        <span>添加产品</span>
      </router-link>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">出入库管理</div>
      <router-link to="/stock-in" class="nav-item">
        <span class="icon">📥</span>
        <span>配件入库</span>
      </router-link>
      <router-link to="/stock-out" class="nav-item">
        <span class="icon">📤</span>
        <span>生产出库</span>
      </router-link>
      <router-link to="/defects" class="nav-item">
        <span class="icon">⚠️</span>
        <span>配件损耗</span>
      </router-link>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">销售管理</div>
      <router-link to="/shipment" class="nav-item">
        <span class="icon">🚚</span>
        <span>成品发货</span>
      </router-link>
      <router-link to="/shipment-records" class="nav-item">
        <span class="icon">📋</span>
        <span>发货记录</span>
      </router-link>
    </div>

    <div class="nav-section">
      <div class="nav-section-title">统计查询</div>
      <router-link to="/history" class="nav-item">
        <span class="icon">📊</span>
        <span>交易历史</span>
      </router-link>
    </div>

    <div v-if="isAdmin" class="nav-section">
      <div class="nav-section-title">系统管理</div>
      <router-link to="/customers" class="nav-item">
        <span class="icon">👥</span>
        <span>客户管理</span>
      </router-link>
      <router-link to="/users" class="nav-item">
        <span class="icon">👤</span>
        <span>用户管理</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: Object
})

const isAdmin = computed(() => {
  return props.user && ['ADMIN', 'MANAGER'].includes(props.user.role)
})
</script>

<style scoped>
.sidebar {
  width: 220px;
  background: #2c3e50;
  color: white;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}

.nav-section {
  padding: 20px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-section-title {
  padding: 10px 20px;
  font-size: 12px;
  color: #95a5a6;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: bold;
}

.nav-item {
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ecf0f1;
  border-left: 3px solid transparent;
  text-decoration: none;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-left-color: #667eea;
}

.nav-item.router-link-active {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.2) 0%, transparent 100%);
  border-left-color: #667eea;
  color: white;
  font-weight: bold;
}

.nav-item .icon {
  font-size: 18px;
  width: 20px;
  text-align: center;
}
</style>
