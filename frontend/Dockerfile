FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm install
COPY . /app
ENV CHOKIDAR_USEPOLLING=true
CMD ["npm", "start"]
