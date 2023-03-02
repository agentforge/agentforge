sendInferenceRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
      context: $("#context-input").val()
      name: $("#name-input").val()
      robot_name: $("#robot-name-input").val()
      authenticity_token: window._token
    success: (response) ->
      $('.chat-history').append "<li><p>#{$("#robot-name-input").val()}: #{response["text"]} </p></li>"
      $('.thought-history').append "<li><p>Thought: #{response["thoughts"]} </p></li>" if response["thoughts"] != ""
      $("#spinner").remove()
    error: () ->
      $("#spinner").remove()

sendMessage = () ->
  host = window.Settings["rails"]["host"]
  port = window.Settings["rails"]["port"]
  text = $("#user-input").val()
  $("#user-input").val("")
  $('.chat-history').append "<li><p>#{$("#name-input").val()}: #{text} </p></li>"
  $('.chat-history').append '<li id="spinner"><md-block><i class="fas fa-spinner fa-pulse"></md-block></i>'
  $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
  console.log("#send-message #{text}")
  sendInferenceRequest("http://#{host}:#{port}/inference/interpret", text)
  event.preventDefault()

$(document).on('turbolinks:load', ->
  $('#send-message').on 'click', (event) ->
    sendMessage()

  $("textarea").keydown (e) ->
  if (e.keyCode == 13 && !e.shiftKey)
    e.preventDefault()

  # Capture the enter key press event
  $(document).on 'keypress', (event) ->
    # Check if the enter key was pressed
    if event.which is 13
      # Trigger the someFunction function
      sendMessage()
)
