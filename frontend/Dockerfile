FROM node:23 AS base

WORKDIR /frontend

COPY ./package.json ./
RUN ls -la
RUN npm install

COPY . .

FROM base AS dev
CMD ["npm", "run", "dev", "--", "--host"]

FROM base AS build
CMD ["npm", "run", "build"]

