# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/


sendInferenceRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
      authenticity_token: window._token
    success: (response) ->

      $('.chat-history').append "<li> #{response["text"]} </li>"

$(document).on('turbolinks:load', ->
  $('#send-message').on 'click', (event) ->
    text = $("#user-input").val()
    console.log("#send-message #{text}")
    sendInferenceRequest("http://localhost:3001/inference/interpret", text)
    event.preventDefault()
)