class WhisperController < ApplicationController

  def text_to_speech
    text = params[:text]
    
    host = Settings.inference_api.host
    port = Settings.inference_api.port
    uri = URI("http://#{host}:#{port}/chat")
    http = Net::HTTP.new(uri.host, uri.port)

    http.read_timeout = 600
  
    request = Net::HTTP::Post.new(uri)
    request["Content-Type"] = "application/json"
    request.body = JSON.dump(text: text)
  
    # response should be a raw wav file
    response = http.request(request)
    save_path = Rails.root.join("public/out.wav")
    File.open(save_path, 'wb') do |f|
      f.write response
    end
    # parse the response wave file and send it back to the client
    render json: { response: response }
  end

  def speech_to_text
    # Your code here
  end

end
