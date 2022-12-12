Rails.application.routes.draw do
  root 'home#index'
  get 'home/index'
  get 'home/show'

  post 'whisper/text_to_speech' => 'whisper#text_to_speech'
  post 'whisper/speech_to_text' => 'whisper#speech_to_text'

  post 'inference/interpret' => 'inference#interpret'

  post 'inference/reset_history' => 'inference#reset_history'

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
