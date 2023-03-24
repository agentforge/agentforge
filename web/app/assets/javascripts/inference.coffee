class App
  constructor: ->
    @playMp4({file_type: "mp4", filename: "/videos/#{@getAvatar()}.mp4"})
    @updateMaxTokensValue()
    # Set change events
    $("#avatar-dropdown").change -> 
      selectedAvatar = @getAvatar()
      $("#hero-video").attr("src", "/videos/" + selectedAvatar + ".mp4")

    $('#send-message').on 'click', (event) ->
      @sendMessage(event)
      event.preventDefault()

    $("textarea").keydown (e) ->
      if (e.keyCode == 13 && e.shiftKey)
        $(this).val($(this).val() + "\n");
        e.preventDefault()
      if (e.keyCode == 13 && !e.shiftKey)
        sendMessage()
        e.preventDefault()

    $("#max_new_tokens").on "input change", () =>
      @updateMaxTokensValue()

  updateMaxTokensValue: () ->
    slider = document.getElementById("max_new_tokens")
    document.getElementById("max_new_tokens_value").textContent = slider.value

  getAvatar: () ->
    avatar = $("#avatar-dropdown").val()
    avatar = "loop" if avatar ==  "default"
    avatar

  getConfigValues: () ->
    configs = {}
    configs.tts = $("#tts").prop("checked")
    configs.lipsync = $("#lipsync").prop("checked")
    configs.streaming = $("#streaming").prop("checked")
    configs.max_new_tokens = parseInt($("#max_new_tokens").val(), 128)
    configs.avatar = @getAvatar()
    configs.model_config = $("#model-config").val()
    configs.model = $("#model").val()
    configs.context = $("#context-input").val()
    configs

  sendTTSRequest: (url, text, avatar) ->
    $.ajax
      url: url
      type: 'POST'
      data:
        text: text
        authenticity_token: window._token
        avatar: avatar
      success: (response) =>
        if response["file_type"] == "wav"
          @playAudio(response)
        else
          @playMp4(response)

  playAudio: (response) ->
    filename = response["filename"]
    audio = new Audio('/wav/' + filename)
    audio.play()

  playMp4: (response) ->
    filename = response["filename"]
    video = document.getElementById("hero-video")
    video.addEventListener 'ended', (event) =>
      video.src = "/videos/#{@getAvatar()}.mp4"
      video.loop = true
      video.load()
      video.play()
      video.removeEventListener 'ended', arguments.callee
    video.src = if filename == "/videos/#{@getAvatar()}.mp4" then "/videos/#{@getAvatar()}.mp4" else '/mp4/' + filename
    video.loop = false
    video.load()
    video.play()

  getTTS: (text, avatar) ->
    host = window.Settings["rails"]["host"]
    port = window.Settings["rails"]["port"]
    @sendTTSRequest("http://#{host}:#{port}/v1/tts", text, avatar)

  sendInferenceRequest: (url, text) ->
    $.ajax
      url: url
      type: 'POST'
      data:
        text: text
        config: getConfigValues()
        authenticity_token: window._token
      success: (response) =>
        md = markdownit()
        formattedOutput = response["text"]
        @getTTS(response["text"], @getAvatar())
        $('.chat-history').append "<li class='ai'><div>#{$("#robot-name-input").val()}: #{formattedOutput}</div></li>"
        $('pre code').each ->
          hljs.highlightElement(this)
        $("#spinner").remove()
        $('.chat-history').scrollTop($('.chat-history')[0].scrollHeight);
      error: () ->
        $("#spinner").remove()

  sendMessage: () ->
    host = window.Settings["rails"]["host"]
    port = window.Settings["rails"]["port"]
    text = $("#user-input").val()
    $("#user-input").val("")
    $('.chat-history').append "<li class='human'><p>#{$("#name-input").val()}: #{text} </p></li>"
    $('.chat-history').append '<li id="spinner"><p><i class="fas fa-spinner fa-pulse"></p></i>'
    $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
    @sendInferenceRequest("http://#{host}:#{port}/v1/completions", text)


# # Max New Tokens Slider
# updateMaxTokensValue = () ->
#   slider = document.getElementById("max_new_tokens")
#   document.getElementById("max_new_tokens_value").textContent = slider.value

# getAvatar = () ->
#   avatar = $("#avatar-dropdown").val()
#   if avatar ==  "default"
#     avatar = "loop"
#   return avatar

# getConfigValues = ->
#   configs = {}
  
#   configs.tts = $("#tts").prop("checked")
#   configs.lipsync = $("#lipsync").prop("checked")
#   configs.streaming = $("#streaming").prop("checked")
  
#   configs.max_new_tokens = parseInt($("#max_new_tokens").val(), 128)
  
#   configs.avatar = getAvatar()
#   configs.model_config = $("#model-config").val()
#   configs.model = $("#model").val()
  
#   return configs

# sendTTSRequest = (url, text, avatar) ->
#   $.ajax
#     url: url
#     type: 'POST'
#     data: 
#       text: text
#       authenticity_token: window._token
#       avatar: avatar
#     success: (response) ->
#       file_type = response["file_type"]
#       if file_type == "wav"
#         playAudio(response)
#       else
#         playMp4(response)

# # playAudio uses Audio object to play wav file
# playAudio = (response) ->
#   file_type = response["file_type"]
#   filename = response["filename"]
#   audio = new Audio('/wav/' + filename)
#   audio.play()

# # playMp4 uses video object to play mp4 file
# # by replacing the source of the video object
# # and loading and playing the video
# playMp4 = (response) ->
#   file_type = response["file_type"]
#   filename = response["filename"]
#   video = document.getElementById("hero-video")
  
#   # Event listener for when the video ends
#   video.addEventListener 'ended', (event) ->
#     video.src = "/videos/#{getAvatar()}.mp4"
#     video.loop = true
#     video.load()
#     video.play()
#     # Remove the event listener once the looping video is loaded
#     video.removeEventListener 'ended', arguments.callee
  
#   if filename == "/videos/#{getAvatar()}.mp4"
#     video.src = "/videos/#{getAvatar()}.mp4"
#   else
#     video.src = '/mp4/' + filename
#     video.loop = false
#   video.load()
#   video.play()

# getTTS = (text, avatar) ->
#   host = window.Settings["rails"]["host"]
#   port = window.Settings["rails"]["port"]
#   sendTTSRequest("http://#{host}:#{port}/v1/tts", text, avatar)

# sendInferenceRequest = (url, text) ->
#   $.ajax
#     url: url
#     type: 'POST'
#     data: 
#       text: text
#       context: $("#context-input").val()
#       avatar: getAvatar()
#       model_config: $("#model-config").val()
#       authenticity_token: window._token
#     success: (response) =>
#       md = markdownit()
#       # formattedOutput = md.render(response["text"])
#       formattedOutput = response["text"]
#       getTTS(response["text"], getAvatar())
#       $('.chat-history').append "<li class='ai'><div>#{$("#robot-name-input").val()}: #{formattedOutput}</div></li>"
#       $('pre code').each ->
#         hljs.highlightElement(this)
#       # $('.thought-history').append "<li><p>Thought: #{response["thoughts"]} </p></li>" if response["thoughts"] != null
#       $("#spinner").remove()
#       $('.chat-history').scrollTop($('.chat-history')[0].scrollHeight);
#     error: () ->
#       $("#spinner").remove()

# sendMessage = () ->
#   host = window.Settings["rails"]["host"]
#   port = window.Settings["rails"]["port"]
#   text = $("#user-input").val()
#   $("#user-input").val("")
#   $('.chat-history').append "<li class='human'><p>#{$("#name-input").val()}: #{text} </p></li>"
#   $('.chat-history').append '<li id="spinner"><p><i class="fas fa-spinner fa-pulse"></p></i>'
#   $(".chat-history").scrollTop($(".chat-history")[0].scrollHeight);
#   sendInferenceRequest("http://#{host}:#{port}/v1/completions", text)

# Events!
$(document).on('turbolinks:load', ->
  App()
)
