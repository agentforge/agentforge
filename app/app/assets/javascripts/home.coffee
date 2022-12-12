# Place all the behaviors and hooks related to the matching controller here.
# All this logic will automatically be available in application.js.
# You can use CoffeeScript in this file: http://coffeescript.org/

sendResetRequest = (url) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      authenticity_token: window._token
    success: (response) ->
      $(".chat-history").html("")

sendMessage = () ->
  sendResetRequest("http://localhost:3001/inference/reset_history")
  event.preventDefault()


$(document).on('turbolinks:load', ->
  window._token = $("#authenticity_token").val()
  $('#reset-history').on 'click', (event) ->
    sendMessage()
)