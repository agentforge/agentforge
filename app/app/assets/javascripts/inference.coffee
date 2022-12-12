# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/


sendInferenceRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
      context: $("#context-input").val()
      authenticity_token: window._token
    success: (response) ->
      $('.chat-history').append "<li><p>Link: #{response["text"]} </p></li>"
      $("#spinner").remove()

sendMessage = () ->
  text = $("#user-input").val()
  $("#user-input").val("")
  $('.chat-history').append "<li><p>You: #{text} </p></li>"
  $('.chat-history').append '<li id="spinner"><p><i class="fas fa-spinner fa-pulse"></p></i>'
  $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
  console.log("#send-message #{text}")
  sendInferenceRequest("http://localhost:3001/inference/interpret", text)
  event.preventDefault()

$(document).on('turbolinks:load', ->
  $('#send-message').on 'click', (event) ->
    sendMessage()

  # Capture the enter key press event
  $(document).on 'keypress', (event) ->
    # Check if the enter key was pressed
    if event.which is 13
      # Trigger the someFunction function
      sendMessage()
)
