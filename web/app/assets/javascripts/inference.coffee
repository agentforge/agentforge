getAvatar = () ->
  avatar = $("#avatar-dropdown").val()
  if avatar ==  "default"
    avatar = "loop"
  return avatar

sendTTSRequest = (url, text, avatar) ->
  $.ajax
    url: url
    type: 'POST'
    data: 
      text: text
      authenticity_token: window._token
      avatar: avatar
    success: (response) ->
      console.log(response)
      file_type = response["file_type"]
      if file_type == "wav"
        playAudio(response)
      else
        playMp4(response)

# playAudio uses Audio object to play wav file
playAudio = (response) ->
  file_type = response["file_type"]
  filename = response["filename"]
  audio = new Audio('/wav/' + filename)
  audio.play()

# playMp4 uses video object to play mp4 file
# by replacing the source of the video object
# and loading and playing the video
playMp4 = (response) ->
  file_type = response["file_type"]
  filename = response["filename"]
  video = document.getElementById("hero-video")
  
  # Event listener for when the video ends
  video.addEventListener 'ended', (event) ->
    video.src = "/videos/#{getAvatar()}.mp4"
    video.loop = true
    video.load()
    video.play()
    # Remove the event listener once the looping video is loaded
    video.removeEventListener 'ended', arguments.callee
  
  if filename == "/videos/#{getAvatar()}.mp4"
    video.src = "/videos/#{getAvatar()}.mp4"
  else
    video.src = '/mp4/' + filename
    video.loop = false
  video.load()
  video.play()

getTTS = (text, avatar) ->
  host = window.Settings["rails"]["host"]
  port = window.Settings["rails"]["port"]
  console.log("#send-message #{text}")
  sendTTSRequest("http://#{host}:#{port}/v1/tts", text, avatar)

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
    success: (response) =>
      md = markdownit()
      formattedOutput = md.render(response["text"]);
      getTTS(response["text"], getAvatar())
      $('.chat-history').append "<li class='ai'><div>#{$("#robot-name-input").val()}: #{formattedOutput}</div></li>"
      $('pre code').each ->
        hljs.highlightElement(this)
      # $('.thought-history').append "<li><p>Thought: #{response["thoughts"]} </p></li>" if response["thoughts"] != null
      $("#spinner").remove()
      $('.chat-history').scrollTop($('.chat-history')[0].scrollHeight);
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
  sendInferenceRequest("http://#{host}:#{port}/v1/completions", text)

$(document).on('turbolinks:load', ->
  playMp4({file_type: "mp4", filename: "/videos/#{getAvatar()}.mp4"})

  $("#avatar-dropdown").change -> 
    selectedAvatar = $(this).val()
    $("#hero-video").attr("src", "/videos/" + selectedAvatar + ".mp4")

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
