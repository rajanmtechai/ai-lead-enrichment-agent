import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#0c1220',
        panel: '#11182a',
        panelSoft: '#17213a',
        accent: '#f97316',
        accentSoft: '#fb923c',
        line: 'rgba(255,255,255,0.08)',
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(249,115,22,0.18), 0 24px 60px rgba(0,0,0,0.32)',
      },
      backgroundImage: {
        dashboard: 'radial-gradient(circle at top left, rgba(249,115,22,0.24), transparent 34%), radial-gradient(circle at top right, rgba(56,189,248,0.16), transparent 24%), linear-gradient(180deg, #09111f 0%, #0c1220 100%)',
      },
    },
  },
  plugins: [],
};

export default config;