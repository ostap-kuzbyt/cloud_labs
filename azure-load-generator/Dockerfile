FROM node:20-alpine

WORKDIR /app

COPY index.js package*.json ./
RUN npm install express node-fetch

EXPOSE 8080

CMD ["node", "index.js"]
