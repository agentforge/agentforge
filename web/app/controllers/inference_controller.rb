class InferenceController < ApplicationController
  require 'net/http'

  def interpret
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    text = params[:text]
    context = params[:context]
    name = params[:name]
    robot_name = params[:robot_name]
    host = Settings.inference_api.host
    port = Settings.inference_api.port
    uri = URI("http://#{host}:#{port}/agent/prompt")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(prompt: text, context: context, name: name, robot_name: robot_name)
  
    response = http.request(request)
    puts response
    text = JSON.parse(response.body)["output"]
    # thoughts = JSON.parse(response.body)["thoughts"]
    # full_phrase = JSON.parse(response.body)["full_phrase"]
    text.gsub("\\n", "<br/>")
    render json: { text: text }
  end

  def reset_history
    host = Settings.inference_api.host
    port = Settings.inference_api.port
    uri = URI("http://#{host}:#{port}/reset_history")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
  
    response = http.request(request)

    render json: { success: true }    
  end
end
