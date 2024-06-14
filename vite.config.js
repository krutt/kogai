/* ~~/vite.config.js */
import autoprefixer from 'autoprefixer'
import { defineConfig } from 'vite'
import path from 'path'
import svgLoader from 'vite-svg-loader'
import vue from '@vitejs/plugin-vue'
import tailwind from 'tailwindcss'

// https://vitejs.dev/config/
export default defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()],
    },
  },
  plugins: [svgLoader(), vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './pages'),
    },
  }
})
