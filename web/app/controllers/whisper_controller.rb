require 'base64'
require 'securerandom'

class WhisperController < ApplicationController

  def text_to_speech
    prompt = params[:text]
    
    host = Settings.inference_api.host
    port = Settings.inference_api.port
    uri = URI("http://#{host}:#{port}/tts")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(prompt: prompt)
    
    # response should be a raw wav file
    response = http.request(request)
    # base64_data = Base64.encode64(response.body)
    # send_data response.body, :type => 'audio/wav'

    # puts response
    uuid = SecureRandom.uuid
    filename = "#{uuid}.wav"
    save_path = Rails.root.join("public/#{filename}")

    File.open(save_path, 'wb') do |f|
      f.write response.body
    end
    response_data = {
      filename: filename,
      # file_data: base64_data
    }
    # # parse the response wave file and send it back to the client
    render json: response_data
  end

  def speech_to_text
    # Your code here
  end

end
