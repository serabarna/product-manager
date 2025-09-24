# Product Management Design

## Project setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start development server:
   ```bash
   npm run dev
   ```

## Troubleshooting
- If you see ESM/CJS errors, ensure Node.js version is >= 20.19.0 or >= 22.12.0.
- If you see Tailwind errors, ensure you have run `npx tailwindcss init -p` and that your `postcss.config.js` and `tailwind.config.js` exist.

## Stack
- Vue 3
- Vite 5
- Tailwind CSS 3
- Axios

## Structure
- `src/views/` contains ProductList, ProductDetail, ProductForm
- `src/router.js` for routing
- `src/assets/styles.css` for Tailwind

## Figma
[Product Management Mockup](https://www.figma.com/design/Cep7R0EjWIdbO4GEzcAkti/Product-Management-Mockup---Codespring-LLM-Training?node-id=6-9&t=yMRsu7x09eXuU0Cu-4)
