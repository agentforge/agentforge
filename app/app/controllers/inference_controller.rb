class InferenceController < ApplicationController
  require 'net/http'

  def interpret
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    text = params[:text]
    context = params[:context]
    name = params[:name]

    uri = URI("http://localhost:3000/chat")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(message: text, context: context, name: name)
  
    response = http.request(request)

    render json: { text: ActionController::Base.helpers.strip_tags(JSON.parse(response.body)["response"]) }
  end

  def reset_history
    text = params[:text]
    context = params[:context]

    uri = URI("http://localhost:3000/reset_history")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
  
    response = http.request(request)

    render json: { success: true }    
  end
end
