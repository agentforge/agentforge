# Use the official Node.js v14 image as the base image
FROM node:14

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the app's dependencies
RUN npm install

# Install Webpacker globally
RUN npm install -g webpack webpack-cli webpack-dev-server

# Copy the app's source code to the container
COPY ../../agent_n .

# Expose the port used by the app (if any)
EXPOSE 3000

# Start the app
# CMD [ "npm", "start" ]
CMD tail -f /dev/null

