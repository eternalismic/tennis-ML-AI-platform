
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { brand: { 600: '#2563eb', 700: '#1d4ed8' } }
    }
  },
  plugins: []
}
