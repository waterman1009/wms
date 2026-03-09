<template>
  <div class="autocomplete-container">
    <input v-model="searchText"
           type="text"
           class="autocomplete-input"
           :placeholder="placeholder"
           @input="handleInput"
           @focus="handleFocus"
           @keydown="handleKeydown"
           autocomplete="off">
    <div v-if="showList" ref="listRef" class="autocomplete-list">
      <div v-for="(item, index) in filteredItems" 
           :key="item.product_id || item.customer_id"
           :class="['autocomplete-item', { selected: index === selectedIndex }]"
           @click="selectItem(item)"
           @mouseenter="selectedIndex = index">
        {{ item.name }} <span v-if="item.quantity !== undefined">(库存: {{ item.quantity }})</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: [String, Number],
  items: Array,
  placeholder: String
})

const emit = defineEmits(['update:modelValue'])

const searchText = ref('')
const showList = ref(false)
const selectedIndex = ref(-1)
const listRef = ref(null)

const filteredItems = computed(() => {
  if (!searchText.value) return props.items.slice(0, 10)
  return props.items
    .filter(item => item.name.toLowerCase().includes(searchText.value.toLowerCase()))
    .slice(0, 10)
})

watch(() => props.modelValue, (val) => {
  if (val) {
    const item = props.items.find(i => i.product_id === val || i.customer_id === val)
    if (item) searchText.value = item.name
  }
})

const handleInput = () => {
  showList.value = true
  selectedIndex.value = -1
  emit('update:modelValue', null)
}

const handleFocus = () => {
  if (filteredItems.value.length > 0) {
    showList.value = true
  }
}

const handleKeydown = (e) => {
  if (!showList.value) return

  if (e.key === 'ArrowDown') {
    e.preventDefault()
    selectedIndex.value = Math.min(selectedIndex.value + 1, filteredItems.value.length - 1)
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    selectedIndex.value = Math.max(selectedIndex.value - 1, -1)
  } else if (e.key === 'Enter' && selectedIndex.value >= 0) {
    e.preventDefault()
    selectItem(filteredItems.value[selectedIndex.value])
  } else if (e.key === 'Escape') {
    showList.value = false
  }
}

const selectItem = (item) => {
  searchText.value = item.name
  emit('update:modelValue', item.product_id || item.customer_id)
  showList.value = false
}

// 点击外部关闭
document.addEventListener('click', (e) => {
  if (listRef.value && !listRef.value.contains(e.target)) {
    showList.value = false
  }
})
</script>
