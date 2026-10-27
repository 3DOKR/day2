FROM node:22-alpine
ENV NODE_ENV=production
WORKDIR /usr/src/app
COPY package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    if [ -f package-lock.json ]; then npm ci --omit=dev; else npm install --omit=dev; fi
USER node
COPY --chown=node:node ./src/ ./src/
EXPOSE 3000
CMD ["node", "src/index.js"]
