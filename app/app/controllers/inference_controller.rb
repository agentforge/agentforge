class InferenceController < ApplicationController
  require 'net/http'

  def interpret
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    text = params[:text]

    uri = URI("http://localhost:3000/chat")
    http = Net::HTTP.new(uri.host, uri.port)
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(message: text, context: "")
  
    response = http.request(request)

    render json: { text: ActionController::Base.helpers.strip_tags(JSON.parse(response.body)["response"]) }
  end
end
