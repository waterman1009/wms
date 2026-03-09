<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <h3>{{ customer ? '编辑客户' : '添加客户' }}</h3>
      <MessageAlert :message="message" :type="messageType" />
      
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>客户名称 *</label>
          <input v-model="form.name" type="text" required>
        </div>
        <div class="form-group">
          <label>联系人</label>
          <input v-model="form.contact_person" type="text">
        </div>
        <div class="form-group">
          <label>电话</label>
          <input v-model="form.phone" type="text">
        </div>
        <div class="form-group">
          <label>地址</label>
          <input v-model="form.address" type="text">
        </div>
        <div class="form-group">
          <label>备注</label>
          <textarea v-model="form.note" rows="3"></textarea>
        </div>
        
        <div class="button-group">
          <button type="submit">保存</button>
          <button type="button" @click="$emit('close')">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import api from '../api'
import MessageAlert from './MessageAlert.vue'

const props = defineProps({
  customer: Object
})

const emit = defineEmits(['close', 'saved'])

const form = reactive({
  name: props.customer?.name || '',
  contact_person: props.customer?.contact_person || '',
  phone: props.customer?.phone || '',
  address: props.customer?.address || '',
  note: props.customer?.note || ''
})

const message = ref('')
const messageType = ref('success')

const handleSubmit = async () => {
  try {
    const { data } = props.customer
      ? await api.updateCustomer(props.customer.customer_id, form)
      : await api.addCustomer(form)
    
    message.value = data.message
    messageType.value = data.success ? 'success' : 'error'
    
    if (data.success) {
      setTimeout(() => emit('saved'), 1000)
    }
  } catch (error) {
    message.value = '操作失败: ' + error.message
    messageType.value = 'error'
  }
}
</script>

<style scoped>
.button-group {
  margin-top: 20px;
}
</style>
