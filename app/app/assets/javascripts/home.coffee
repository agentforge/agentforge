# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

sendResetRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      authenticity_token: window._token
    success: (response) ->
      $('.chat-history').append "<li><p>Link: #{response["text"]} </p></li>"
      $("#spinner").remove()

sendMessage = () ->
  # text = $("#user-input").val()
  # $("#user-input").val("")
  # $('.chat-history').append "<li><p>You: #{text} </p></li>"
  # $('.chat-history').append '<li id="spinner"><p><i class="fas fa-spinner fa-pulse"></p></i>'
  # $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
  # console.log("#send-message #{text}")
  sendInferenceRequest("http://localhost:3001/inference/reset_history", text)
  event.preventDefault()


$(document).on('turbolinks:load', ->
  window._token = $("#authenticity_token").val()
  $('#reset-history').on 'click', (event) ->
    sendMessage()
)