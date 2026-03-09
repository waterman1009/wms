import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8080',  // 使用 127.0.0.1 而不是 localhost
        changeOrigin: true,
        secure: false
      }
    }
  },
  build: {
    outDir: '../static',
    emptyOutDir: true
  }
})
