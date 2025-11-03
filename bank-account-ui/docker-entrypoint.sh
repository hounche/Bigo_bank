#!/bin/sh
set -e

echo "Vérification de Rollup..."
if ! npm ls @rollup/rollup-linux-x64-gnu >/dev/null 2>&1; then
  echo "Installation manquante de @rollup/rollup-linux-x64-gnu..."
  npm install @rollup/rollup-linux-x64-gnu --save-dev --force || true
fi

echo "Lancement de Vite..."
exec npm run dev -- --host
