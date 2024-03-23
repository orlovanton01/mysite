import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },

  server:{
    proxy: {
       "^/api": {
         "target": "http://127.0.0.1:8000",
         "ws": true,
         "changeOrigin": true
       },
       "^/admin": {
         "target": "http://127.0.0.1:8000",
         "ws": true,
         "changeOrigin": true
       },
 
       "^/media": {
        "target": "http://127.0.0.1:8000",
        "ws": true,
        "changeOrigin": true
      },


      "^/login": {
        "target": "http://127.0.0.1:8000",
        "ws": true,
        "changeOrigin": true
      },
      "^/register": {
        "target": "http://127.0.0.1:8000",
        "ws": true,
        "changeOrigin": true
      },
      "^/session": {
        "target": "http://127.0.0.1:8000",
        "ws": true,
        "changeOrigin": true
      },
      "^/whoami": {
        "target": "http://127.0.0.1:8000",
        "ws": true,
        "changeOrigin": true
      },
    }
  }
})
