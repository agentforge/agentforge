sendTTSRequest = (url, text) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
      authenticity_token: window._token
    success: (response) ->
      snd = new Audio('/out.wav');
      snd.play()

getTTS = (text) ->
  host = window.Settings["rails"]["host"]
  port = window.Settings["rails"]["port"]
  console.log("#send-message #{text}")
  sendTTSRequest("http://#{host}:#{port}/whisper/text_to_speech", text)

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
      getTTS(response["text"])
      $('.chat-history').append "<li class='ai'><md-block>#{$("#robot-name-input").val()}: #{response["text"]}</li>"
      $('.thought-history').append "<li><p>Thought: #{response["thoughts"]} </p></li>" if response["thoughts"] != null
      $("#spinner").remove()
    error: () ->
      $("#spinner").remove()

sendMessage = () ->
  host = window.Settings["rails"]["host"]
  port = window.Settings["rails"]["port"]
  text = $("#user-input").val()
  $("#user-input").val("")
  $('.chat-history').append "<li class='human'><p>#{$("#name-input").val()}: #{text} </p></li>"
  $('.chat-history').append '<li id="spinner"><p><i class="fas fa-spinner fa-pulse"></p></i>'
  $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
  console.log("#send-message #{text}")
  sendInferenceRequest("http://#{host}:#{port}/inference/interpret", text)

$(document).on('turbolinks:load', ->
  $('#send-message').on 'click', (event) ->
    sendMessage(event)
    event.preventDefault()

  $("textarea").keydown (e) ->
    if (e.keyCode == 13 && e.shiftKey)
      $(this).val($(this).val() + "\n");
      e.preventDefault()
    if (e.keyCode == 13 && !e.shiftKey)
      sendMessage()
      e.preventDefault()
)
