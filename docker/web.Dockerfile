# Use the official Node.js v14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

RUN mkdir /app/agent_n

COPY . /app/agent_n/

WORKDIR /app/agent_n/personaforge

# Install the app's dependencies
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
RUN nvm install 16.8.0
RUN nvm use 16.8.0
RUN npm install

# Install Webpacker globally
RUN npm install -g webpack webpack-cli webpack-dev-server

RUN apt-get update
RUN apt-get install -y tig

# Expose the port used by the app (if any)
EXPOSE 3005

# Start the app
# CMD [ "npm", "start" ]
CMD tail -f /dev/null

