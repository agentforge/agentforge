class InferenceController < ApplicationController
  require 'net/http'

  def completions
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    text = params[:text]
    context = params[:context]
    name = params[:name]
    robot_name = params[:robot_name]

    host = Settings.inference_api.host
    port = Settings.inference_api.port
    
    uri = URI("http://#{host}:#{port}/v1/completions")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(prompt: text, context: context, name: name, robot_name: robot_name)
  
    response = http.request(request)
    puts JSON.parse(response.body)
    text = JSON.parse(response.body)["response"]
    output = JSON.parse(response.body)["output"]
    thought = JSON.parse(response.body)["thought"]

    text.gsub("\n", "<br/>")
    render json: { text: text, output: output, thought: thought }
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
