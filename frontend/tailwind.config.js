/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        ink: {
          950: '#0a0a0f',
          900: '#12121a',
          800: '#1c1c28',
          700: '#2a2a3d',
          600: '#3d3d5c',
        },
        accent: {
          DEFAULT: '#6c63ff',
          hover:   '#7c74ff',
          muted:   '#6c63ff33',
        },
        risk: {
          low:    '#22c55e',
          medium: '#f59e0b',
          high:   '#ef4444',
          vhigh:  '#dc2626',
        },
      },
    },
  },
  plugins: [],
}
