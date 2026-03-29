import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  // Use relative paths for assets - works both locally and on GitHub Pages
  base: './',
  build: {
    outDir: 'dist',
    sourcemap: false,
    assetsDir: 'assets',
  },
  publicDir: 'public',
})
