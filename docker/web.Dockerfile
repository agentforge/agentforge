# Use the official Node.js v14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

RUN mkdir /app/agent_n

COPY . /app/agent_n/

WORKDIR /app/agent_n/web2

# Install the app's dependencies
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

