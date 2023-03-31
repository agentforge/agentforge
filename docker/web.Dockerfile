# Base image
FROM ruby:3.2.1

# Set environment variables
ENV APP_HOME /app
ENV RAILS_ENV development
ENV RAILS_SERVE_STATIC_FILES true
ENV RAILS_LOG_TO_STDOUT true
ARG REPO_URL
ARG SSH_PRIVATE_KEY

ENV REPO_URL=$REPO_URL
ENV SSH_PRIVATE_KEY=$SSH_PRIVATE_KEY

# Set the working directory to /app
WORKDIR /app

# Copy over git repos
RUN mkdir -p /root/.ssh && \
    echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

RUN  apt-get -yq update && \
     apt-get -yqq install ssh

RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Set the working directory
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# agent_n API
RUN git clone "$REPO_URL"

# Install nodejs and yarn (for webpacker)
RUN apt-get update -qq && \
    apt-get install -y nodejs npm && \
    npm install --global yarn

WORKDIR $APP_HOME/agent_n/web

# Install bundler and gems
RUN gem install bundler && \
    bundle install --jobs 4 --retry 3

# Precompile assets
# RUN RAILS_ENV=production SECRET_KEY_BASE=placeholder_key_base bin/rails assets:precompile

# Expose port 3000
EXPOSE 3000

# Start the server
CMD ["bundle", "exec", "rails", "server", "-b", "0.0.0.0", "-p", "3000"]
