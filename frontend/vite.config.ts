import { defineConfig } from 'vite';
import { mergeConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { defineConfig as defineVitestConfig } from 'vitest/config';

export default defineConfig(
  mergeConfig(
    {
      plugins: [react()],
    },
    defineVitestConfig({
      test: {
        environment: "jsdom",
        setupFiles: ["./src/test/setup.ts"],
        globals: false,
      },
    })
  )
);