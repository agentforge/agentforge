# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

sendTTSRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
    success: (response) ->
      console.log(response)

getTTS = (text) ->
  host = window.Settings["rails"]["host"]
  port = window.Settings["rails"]["port"]
  console.log("#send-message #{text}")
  sendTTSRequest("http://#{host}:#{port}/whisper/text_to_speech", text)
  event.preventDefault()