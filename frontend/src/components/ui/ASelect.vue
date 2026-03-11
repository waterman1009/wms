<template>
  <div class="a-select" :class="selectClass" ref="selectRef">
    <div 
      class="a-select-selector" 
      :class="selectorClass"
      @click="handleToggle"
      @keydown="handleKeydown"
      tabindex="0"
    >
      <div class="a-select-selection-search">
        <input
          v-if="showSearch && open"
          ref="searchInputRef"
          v-model="searchValue"
          class="a-select-selection-search-input"
          :placeholder="searchPlaceholder"
          @input="handleSearch"
          @keydown.stop="handleSearchKeydown"
        />
        <span v-else class="a-select-selection-item">
          {{ displayValue || placeholder }}
        </span>
      </div>
      <span class="a-select-arrow" :class="{ 'a-select-arrow-open': open }">
        <svg viewBox="64 64 896 896" width="1em" height="1em" fill="currentColor">
          <path d="M884 256h-75c-5.1 0-9.9 2.5-12.9 6.6L512 654.2 227.9 262.6c-3-4.1-7.8-6.6-12.9-6.6h-75c-6.5 0-10.3 7.4-6.5 12.7l352.6 486.1c12.8 17.6 39 17.6 51.8 0l352.6-486.1c3.9-5.3.1-12.7-6.5-12.7z"/>
        </svg>
      </span>
    </div>
    
    <transition name="slide-up">
      <div v-if="open" class="a-select-dropdown" :style="dropdownStyle">
        <div class="a-select-dropdown-content">
          <div v-if="loading" class="a-select-dropdown-loading">
            <ASpin size="small" />
            <span>加载中...</span>
          </div>
          <div v-else-if="filteredOptions.length === 0" class="a-select-dropdown-empty">
            <AEmpty :description="searchValue ? '无匹配数据' : '暂无数据'" size="small" />
          </div>
          <div v-else class="a-select-dropdown-menu">
            <div
              v-for="(option, index) in filteredOptions"
              :key="getOptionKey(option)"
              class="a-select-dropdown-menu-item"
              :class="{
                'a-select-dropdown-menu-item-selected': isSelected(option),
                'a-select-dropdown-menu-item-active': activeIndex === index,
                'a-select-dropdown-menu-item-disabled': isDisabled(option)
              }"
              @click="handleSelect(option)"
              @mouseenter="activeIndex = index"
            >
              <div class="a-select-dropdown-menu-item-content">
                <slot name="option" :option="option" :index="index">
                  {{ getOptionLabel(option) }}
                </slot>
              </div>
              <span v-if="isSelected(option)" class="a-select-dropdown-menu-item-icon">
                <svg viewBox="64 64 896 896" width="1em" height="1em" fill="currentColor">
                  <path d="M912 190h-69.9c-9.8 0-19.1 4.5-25.1 12.2L404.7 724.5 207 474a32 32 0 0 0-25.1-12.2H112c-6.7 0-10.4 7.7-6.3 12.9l273.9 347c12.8 16.2 37.4 16.2 50.3 0l488.4-618.9c4.1-5.1.4-12.8-6.3-12.8z"/>
                </svg>
              </span>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { onClickOutside } from '@vueuse/core'
import ASpin from './ASpin.vue'
import AEmpty from './AEmpty.vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, Array],
    default: undefined
  },
  options: {
    type: Array,
    default: () => []
  },
  placeholder: {
    type: String,
    default: '请选择'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  allowClear: {
    type: Boolean,
    default: false
  },
  showSearch: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: '请输入搜索内容'
  },
  filterOption: {
    type: [Boolean, Function],
    default: true
  },
  size: {
    type: String,
    default: 'middle',
    validator: (value) => ['small', 'middle', 'large'].includes(value)
  },
  status: {
    type: String,
    validator: (value) => ['error', 'warning'].includes(value)
  },
  fieldNames: {
    type: Object,
    default: () => ({
      label: 'label',
      value: 'value',
      disabled: 'disabled'
    })
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'search', 'focus', 'blur'])

const selectRef = ref(null)
const searchInputRef = ref(null)
const open = ref(false)
const searchValue = ref('')
const activeIndex = ref(-1)

// 计算属性
const selectClass = computed(() => ({
  'a-select-open': open.value,
  'a-select-disabled': props.disabled,
  'a-select-loading': props.loading,
  [`a-select-${props.size}`]: props.size !== 'middle',
  [`a-select-status-${props.status}`]: props.status
}))

const selectorClass = computed(() => ({
  'a-select-selector-focused': open.value,
  'a-select-selector-disabled': props.disabled
}))

const dropdownStyle = computed(() => ({
  minWidth: selectRef.value ? `${selectRef.value.offsetWidth}px` : 'auto'
}))

const displayValue = computed(() => {
  if (props.modelValue === undefined || props.modelValue === null) return ''
  
  const selectedOption = props.options.find(option => 
    getOptionValue(option) === props.modelValue
  )
  
  return selectedOption ? getOptionLabel(selectedOption) : props.modelValue
})

const filteredOptions = computed(() => {
  if (!props.showSearch || !searchValue.value) {
    return props.options
  }
  
  if (typeof props.filterOption === 'function') {
    return props.options.filter(option => props.filterOption(searchValue.value, option))
  }
  
  if (props.filterOption === false) {
    return props.options
  }
  
  return props.options.filter(option => {
    const label = getOptionLabel(option).toString().toLowerCase()
    return label.includes(searchValue.value.toLowerCase())
  })
})

// 工具函数
const getOptionValue = (option) => {
  if (typeof option === 'object' && option !== null) {
    return option[props.fieldNames.value]
  }
  return option
}

const getOptionLabel = (option) => {
  if (typeof option === 'object' && option !== null) {
    return option[props.fieldNames.label]
  }
  return option
}

const getOptionKey = (option) => {
  return getOptionValue(option)
}

const isSelected = (option) => {
  return getOptionValue(option) === props.modelValue
}

const isDisabled = (option) => {
  if (typeof option === 'object' && option !== null) {
    return option[props.fieldNames.disabled]
  }
  return false
}

// 事件处理
const handleToggle = () => {
  if (props.disabled) return
  
  open.value = !open.value
  
  if (open.value) {
    emit('focus')
    if (props.showSearch) {
      nextTick(() => {
        searchInputRef.value?.focus()
      })
    }
  } else {
    emit('blur')
    searchValue.value = ''
    activeIndex.value = -1
  }
}

const handleSelect = (option) => {
  if (isDisabled(option)) return
  
  const value = getOptionValue(option)
  emit('update:modelValue', value)
  emit('change', value, option)
  
  open.value = false
  searchValue.value = ''
  activeIndex.value = -1
}

const handleSearch = (e) => {
  const value = e.target.value
  searchValue.value = value
  emit('search', value)
}

const handleKeydown = (e) => {
  if (props.disabled) return
  
  switch (e.key) {
    case 'Enter':
    case ' ':
      e.preventDefault()
      if (!open.value) {
        handleToggle()
      } else if (activeIndex.value >= 0) {
        handleSelect(filteredOptions.value[activeIndex.value])
      }
      break
    case 'Escape':
      if (open.value) {
        e.preventDefault()
        open.value = false
      }
      break
    case 'ArrowDown':
      e.preventDefault()
      if (!open.value) {
        handleToggle()
      } else {
        activeIndex.value = Math.min(activeIndex.value + 1, filteredOptions.value.length - 1)
      }
      break
    case 'ArrowUp':
      e.preventDefault()
      if (open.value) {
        activeIndex.value = Math.max(activeIndex.value - 1, 0)
      }
      break
  }
}

const handleSearchKeydown = (e) => {
  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      activeIndex.value = Math.min(activeIndex.value + 1, filteredOptions.value.length - 1)
      break
    case 'ArrowUp':
      e.preventDefault()
      activeIndex.value = Math.max(activeIndex.value - 1, 0)
      break
    case 'Enter':
      e.preventDefault()
      if (activeIndex.value >= 0) {
        handleSelect(filteredOptions.value[activeIndex.value])
      }
      break
    case 'Escape':
      e.preventDefault()
      open.value = false
      break
  }
}

// 点击外部关闭
onClickOutside(selectRef, () => {
  if (open.value) {
    open.value = false
    searchValue.value = ''
    activeIndex.value = -1
  }
})

// 监听选项变化，重置活跃索引
watch(filteredOptions, () => {
  activeIndex.value = -1
})
</script>

<style scoped>
.a-select {
  position: relative;
  display: inline-block;
  width: 100%;
  font-size: 14px;
  line-height: 1.5715;
  color: rgba(0, 0, 0, 0.85);
}

.a-select-selector {
  position: relative;
  background-color: #fff;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  transition: all 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  cursor: pointer;
  display: flex;
  align-items: center;
  min-height: 32px;
  padding: 4px 11px;
}

.a-select-selector:hover {
  border-color: #4096ff;
}

.a-select-selector-focused {
  border-color: #4096ff;
  box-shadow: 0 0 0 2px rgba(5, 145, 255, 0.1);
  outline: 0;
}

.a-select-selector-disabled {
  color: rgba(0, 0, 0, 0.25);
  background-color: #f5f5f5;
  cursor: not-allowed;
  border-color: #d9d9d9;
}

.a-select-selector-disabled:hover {
  border-color: #d9d9d9;
}

.a-select-selection-search {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.a-select-selection-search-input {
  border: none;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: inherit;
  line-height: inherit;
  color: inherit;
}

.a-select-selection-item {
  flex: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  color: rgba(0, 0, 0, 0.85);
}

.a-select-selector:not(.a-select-selector-disabled) .a-select-selection-item:empty::before {
  content: attr(data-placeholder);
  color: rgba(0, 0, 0, 0.25);
}

.a-select-arrow {
  display: flex;
  align-items: center;
  width: 12px;
  height: 12px;
  margin-left: 8px;
  color: rgba(0, 0, 0, 0.25);
  font-size: 12px;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.a-select-arrow-open {
  transform: rotate(180deg);
}

.a-select-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1050;
  width: 100%;
  margin-top: 4px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 6px 16px 0 rgba(0, 0, 0, 0.08), 0 3px 6px -4px rgba(0, 0, 0, 0.12), 0 9px 28px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(5, 5, 5, 0.06);
}

.a-select-dropdown-content {
  max-height: 256px;
  overflow-y: auto;
}

.a-select-dropdown-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  color: rgba(0, 0, 0, 0.45);
  gap: 8px;
}

.a-select-dropdown-empty {
  padding: 12px;
  text-align: center;
}

.a-select-dropdown-menu-item {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 12px;
  color: rgba(0, 0, 0, 0.85);
  font-weight: normal;
  font-size: 14px;
  line-height: 22px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.a-select-dropdown-menu-item:hover,
.a-select-dropdown-menu-item-active {
  background-color: #f5f5f5;
}

.a-select-dropdown-menu-item-selected {
  background-color: #e6f4ff;
  font-weight: 600;
}

.a-select-dropdown-menu-item-disabled {
  color: rgba(0, 0, 0, 0.25);
  cursor: not-allowed;
}

.a-select-dropdown-menu-item-disabled:hover {
  background-color: transparent;
}

.a-select-dropdown-menu-item-content {
  flex: 1;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.a-select-dropdown-menu-item-icon {
  display: flex;
  align-items: center;
  width: 16px;
  height: 16px;
  color: #1890ff;
  font-size: 12px;
  margin-left: 8px;
}

/* 尺寸变体 */
.a-select-small .a-select-selector {
  min-height: 24px;
  padding: 0 7px;
  font-size: 12px;
}

.a-select-large .a-select-selector {
  min-height: 40px;
  padding: 6px 11px;
  font-size: 16px;
}

/* 状态样式 */
.a-select-status-error .a-select-selector {
  border-color: #ff4d4f;
}

.a-select-status-error .a-select-selector:hover {
  border-color: #ff4d4f;
}

.a-select-status-error .a-select-selector-focused {
  border-color: #ff4d4f;
  box-shadow: 0 0 0 2px rgba(255, 77, 79, 0.1);
}

.a-select-status-warning .a-select-selector {
  border-color: #faad14;
}

.a-select-status-warning .a-select-selector:hover {
  border-color: #faad14;
}

.a-select-status-warning .a-select-selector-focused {
  border-color: #faad14;
  box-shadow: 0 0 0 2px rgba(250, 173, 20, 0.1);
}

/* 动画 */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s cubic-bezier(0.645, 0.045, 0.355, 1);
  transform-origin: 0 0;
}

.slide-up-enter-from {
  opacity: 0;
  transform: scaleY(0.8);
}

.slide-up-leave-to {
  opacity: 0;
  transform: scaleY(0.8);
}

/* 滚动条样式 */
.a-select-dropdown-content::-webkit-scrollbar {
  width: 6px;
}

.a-select-dropdown-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.a-select-dropdown-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.a-select-dropdown-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>