# which node version to use?
FROM node:alpine AS build

# Setting up the work directory
WORKDIR /frontend

# Installing dependencies
COPY ./package.json /frontend
RUN npm install 

# Copying all the files in our project
COPY . .

EXPOSE 3000

# Starting our application
CMD npm start