FROM node:22-alpine

WORKDIR /app

# install exactly what package-lock.json pins
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build
