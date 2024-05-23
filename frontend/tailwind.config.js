/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}', './formkit.theme.ts'],
  theme: {
    extend: {
      colors: {
        light: '#FBF7F4',
        textLight: '#1F2041',
        dark: '#2D2D2A',
        textDark: '#FFFFFF',
        primaryLight: '#4C4C9D',
        primaryDark: '#059669',
      },
    },
  },
  darkMode: 'class',
  plugins: [],
};
