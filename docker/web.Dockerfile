# Use the official Node.js v14 image as the base image
FROM node:20-slim

# Set the working directory in the container
WORKDIR /app

# Replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Set debconf to run non-interactively
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN mkdir /app/agentforge

COPY . /app/agentforge/

WORKDIR /app/agentforge/web/

ENV NODE_VERSION 16.8.0
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR
RUN apt update && apt install -y curl

# Install the app's dependencies

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default \
    && npm install \
    && npm install -g webpack webpack-cli webpack-dev-server \
    && npm install next@latest react@latest react-dom@latest

RUN apt-get update
RUN apt-get install -y tig libvips libvips-dev libvips-tools

# Expose the port used by the app (if any)
EXPOSE 8080

# Start the app
# CMD [ "npm", "start" ]
CMD tail -f /dev/null

