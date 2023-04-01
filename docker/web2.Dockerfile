# Use the official Node.js v14 image as the base image
FROM node:14

# Copy over git repos
RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

RUN  apt-get -yq update && \
     apt-get -yqq install ssh

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Set the working directory in the container
WORKDIR /app

RUN git clone "$REPO_URL"

WORKDIR /app/agent_n

# Install the app's dependencies
RUN npm install

# Install Webpacker globally
RUN npm install -g webpack webpack-cli webpack-dev-server

RUN apt-get update
RUN apt-get install -y tig

# Copy the app's source code to the container

# Expose the port used by the app (if any)
EXPOSE 3005

# Start the app
# CMD [ "npm", "start" ]
CMD tail -f /dev/null

