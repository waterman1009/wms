<template>
  <div class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-content">
      <h3 style="color: #667eea; margin-bottom: 20px;">
        <span style="font-size: 24px;">⚠️</span> 发货确认
      </h3>
      
      <div class="confirm-details">
        <div class="detail-item">
          <strong>客户名称：</strong>
          <span style="color: #667eea; font-size: 16px; font-weight: bold;">{{ customerName }}</span>
        </div>
        
        <div class="detail-item">
          <strong>发货产品：</strong>
        </div>
        
        <table>
          <thead>
            <tr>
              <th style="width: 60px;">序号</th>
              <th>产品名称</th>
              <th style="width: 100px;">数量</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in shipments" :key="index">
              <td style="text-align: center;">{{ index + 1 }}</td>
              <td>{{ item.product_name }}</td>
              <td style="text-align: center;">{{ item.quantity }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr style="background: #e9ecef; font-weight: bold;">
              <td colspan="2" style="text-align: right;">合计：</td>
              <td style="text-align: center; color: #667eea; font-size: 16px;">{{ totalQuantity }}</td>
            </tr>
          </tfoot>
        </table>
        
        <div v-if="note" class="detail-item">
          <strong>备注：</strong>
          <div class="note-box">{{ note }}</div>
        </div>
      </div>
      
      <div class="warning-box">
        <strong>⚠️ 请仔细核对以上信息</strong>
        <p>确认后将扣减库存并生成发货记录，此操作不可撤销！</p>
      </div>
      
      <div class="button-group">
        <button type="button" class="btn-secondary" @click="$emit('cancel')">取消</button>
        <button type="button" class="btn-success" @click="$emit('confirm')">确认发货</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  shipments: Array,
  customerName: String,
  note: String
})

defineEmits(['confirm', 'cancel'])

const totalQuantity = computed(() => {
  return props.shipments.reduce((sum, item) => sum + (item.quantity || 0), 0)
})
</script>

<style scoped>
.confirm-details {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.detail-item {
  margin-bottom: 15px;
}

.note-box {
  background: white;
  padding: 10px;
  border-radius: 5px;
  margin-top: 5px;
  color: #6c757d;
}

.warning-box {
  background: #fff3cd;
  border: 1px solid #ffc107;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
  color: #856404;
}

.warning-box p {
  margin: 10px 0 0 0;
  font-size: 14px;
}

.button-group {
  text-align: right;
}

.btn-secondary {
  background: #6c757d;
  margin-right: 10px;
}

.btn-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}
</style>
