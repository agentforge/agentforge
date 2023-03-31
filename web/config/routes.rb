Rails.application.routes.draw do
  root 'home#index'
  get 'home/index'
  get 'home/show'

  # API
  post 'v1/tts' => 'whisper#text_to_speech'
  post 'v1/completions' => 'inference#completions'
  
  post 'whisper/speech_to_text' => 'whisper#speech_to_text'
  post 'inference/reset_history' => 'inference#reset_history'

  # Streaming
  post 'inference/publish'
  get 'inference/stream'

end
