# pull official base image
ARG NODE_VERSION=current-alpine
FROM node:${NODE_VERSION}
# set working directory
WORKDIR /usr/src/app/react

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
 
COPY package.json ./
COPY package-lock.json ./
COPY . .

RUN npm install --force
RUN npm install react-scripts@3.4.1 -g


# add app
COPY . ./

# start app
CMD ["npm", "start"]
