import path from 'path';
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import { VITE_DEFAULT_PORT } from './src/constants/dev';

let base: string = '';
// 1. if NOTEBOOK_ID is set, use /notebook-sessions/${NOTEBOOK_ID}/ports/5173/ for dev server
if (process.env.NOTEBOOK_ID && process.env.NODE_ENV === 'development') {
    const notebookId = process.env.NOTEBOOK_ID;
    base = `/notebook-sessions/${notebookId}/ports/${VITE_DEFAULT_PORT}/`;
}
const proxyBase: string = base === '' ? '/' : base;


// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    {
        name: 'strip-base',
        apply: 'serve',
        configureServer({ middlewares }) {
          middlewares.use((req, _res, next) => {
            if (base !== '' && !req.url?.startsWith(base)) {
              req.url = base.slice(0, -1) + req.url;
            }
            next();
          });
        },
      },
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  base: base,
  build: {
    outDir: '../web/static/',
    manifest: true,
  },
  server: {
    host: true,
    allowedHosts: ["localhost", "127.0.0.1", ".datarobot.com"],
    proxy: {
      [`${proxyBase}api/`]: {
        target: 'http://localhost:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(new RegExp(`^${proxyBase}`), ''),
      }
    }
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './tests/setupTests.ts',
    typecheck: {
      tsconfig: './tsconfig.test.json',
    }
  },
})
