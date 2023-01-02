class InferenceController < ApplicationController
  require 'net/http'
  include Settings

  def interpret
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    text = params[:text]
    context = params[:context]
    name = params[:name]
    host = Settings.config(['inference_api', 'host'])
    port = Settings.config(['inference_api', 'port'])
    uri = URI("http://#{host}:#{port}/chat")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(message: text, context: context, name: name)
  
    response = http.request(request)

    render json: { text: ActionController::Base.helpers.strip_tags(JSON.parse(response.body)["response"]) }
  end

  def reset_history
    uri = URI("http://#{host}:#{port}/reset_history")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
  
    response = http.request(request)

    render json: { success: true }    
  end
end
