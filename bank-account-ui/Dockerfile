# ---------- FRONT : bank-account-ui/Dockerfile ----------
FROM node:20

WORKDIR /usr/src/app

ENV NODE_ENV=development
ENV npm_config_update_notifier=false
ENV npm_config_fund=false
ENV npm_config_audit=false

# Copier les fichiers de dépendances
COPY package*.json ./

# Supprimer node_modules / cache
RUN rm -rf node_modules package-lock.json

# Installer les dépendances proprement
RUN npm install --legacy-peer-deps --force

# Copier le reste du projet
COPY . .

# Patch Rollup bug au démarrage (voir script)
COPY ./docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 5173

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
