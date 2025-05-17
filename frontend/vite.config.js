import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: '/app',
  server: {
    port: 3000,
    host: true
  },
  esbuild: {
    target: 'esnext'
  }
})