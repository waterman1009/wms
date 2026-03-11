<template>
  <div class="a-spin" :class="spinClass">
    <div class="a-spin-dot">
      <span class="a-spin-dot-item"></span>
      <span class="a-spin-dot-item"></span>
      <span class="a-spin-dot-item"></span>
      <span class="a-spin-dot-item"></span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'default',
    validator: (value) => ['small', 'default', 'large'].includes(value)
  }
})

const spinClass = computed(() => ({
  [`a-spin-${props.size}`]: props.size !== 'default'
}))
</script>

<style scoped>
.a-spin {
  display: inline-block;
  color: #1890ff;
}

.a-spin-dot {
  position: relative;
  display: inline-block;
  font-size: 20px;
  width: 1em;
  height: 1em;
}

.a-spin-dot-item {
  position: absolute;
  display: block;
  width: 9px;
  height: 9px;
  background-color: #1890ff;
  border-radius: 100%;
  transform: scale(0.75);
  transform-origin: 50% 50%;
  opacity: 0.3;
  animation: antSpinMove 1s infinite linear alternate;
}

.a-spin-dot-item:nth-child(1) {
  top: 0;
  left: 0;
}

.a-spin-dot-item:nth-child(2) {
  top: 0;
  right: 0;
  animation-delay: 0.4s;
}

.a-spin-dot-item:nth-child(3) {
  right: 0;
  bottom: 0;
  animation-delay: 0.8s;
}

.a-spin-dot-item:nth-child(4) {
  bottom: 0;
  left: 0;
  animation-delay: 1.2s;
}

.a-spin-small .a-spin-dot {
  font-size: 14px;
}

.a-spin-large .a-spin-dot {
  font-size: 32px;
}

@keyframes antSpinMove {
  to {
    opacity: 1;
  }
}
</style>