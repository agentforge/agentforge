require 'base64'
require 'securerandom'

class WhisperController < ApplicationController

  def text_to_speech
    prompt = params[:text]
    
    host = Settings.inference_api.host
    port = Settings.inference_api.port
    uri = URI("http://#{host}:#{port}/v1/tts")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(prompt: prompt, generate_lip_sync: "true")
    
    # response should be a raw wav file
    response = http.request(request)

    content_type = response.content_type
    file_type = content_type.split('/').last

    # base64_dtata = Base64.encode64(response.body)
    # send_data response.body, :type => 'audio/wav'

    # puts response
    uuid = SecureRandom.uuid
    filename = "#{uuid}.#{file_type}"
    save_path = Rails.root.join("public/#{file_type}/#{filename}")

    File.open(save_path, 'wb') do |f|
      f.write response.body
    end
    response_data = {
      filename: filename,
      file_type: file_type
    }
    # # parse the response wave file and send it back to the client
    render json: response_data
  end

  def speech_to_text
    # Your code here
  end

end
