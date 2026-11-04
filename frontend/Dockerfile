# --- build stage: compile the SPA -------------------------------------------
FROM node:22-alpine AS build

WORKDIR /app

# install exactly what package-lock.json pins
COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# --- runtime stage: nginx serving the built files and proxying the API ------
# The SPA is baked into the image, so every `docker compose up --build` ships
# the current build (a shared volume would keep serving the first build).
FROM nginx:1.30-alpine

COPY --from=build /app/dist /var/www/frontend
# site configuration is mounted from ../nginx/conf.d (see docker-compose.yml)
