# Use the official Node.js v14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN mkdir /app/agentforge

COPY . /app/agentforge/

WORKDIR /app/agentforge/personaforge

ENV NODE_VERSION 16.8.0
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR

# Install the app's dependencies

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default

# Install Webpacker globally
RUN npm install
RUN npm install -g webpack webpack-cli webpack-dev-server
RUN npm install next@latest react@latest react-dom@latest

RUN apt-get update
RUN apt-get install -y tig

# Expose the port used by the app (if any)
EXPOSE 3005

# Start the app
# CMD [ "npm", "start" ]
CMD tail -f /dev/null

