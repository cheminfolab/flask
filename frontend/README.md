```
npm create vite@latest my-project
cd my-project
```
```
npm install tailwindcss @tailwindcss/vite
```
vite.config.ts:
```
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
})
```
index.css:
```
@import "tailwindcss"
```
