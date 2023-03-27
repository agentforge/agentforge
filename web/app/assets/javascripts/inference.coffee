class App
  constructor: ->
    # Set change events
    $("#avatar-dropdown").change => 
      selectedAvatar = @getAvatar()
      $("#hero-video").attr("src", "/videos/" + selectedAvatar + ".mp4")

    $('#send-message').on 'click', (event) =>
      @sendMessage(event)
      event.preventDefault()

    $("textarea").keydown (e) =>
      if (e.keyCode == 13 && e.shiftKey)
        $(this).val($(this).val() + "\n");
        e.preventDefault()
      if (e.keyCode == 13 && !e.shiftKey)
        @sendMessage()
        e.preventDefault()

    $("#max_new_tokens").on "input change", () =>
      @updateMaxTokensValue()

    $('#tts, #streaming').on 'change', (e) =>
      console.log "change"
      e.preventDefault()
      @updateStates()

  updateMaxTokensValue: () ->
    slider = document.getElementById("max_new_tokens")
    document.getElementById("max_new_tokens_value").textContent = slider.value

  getAvatar: () ->
    avatar = $("#avatar-dropdown").val()
    avatar

  getConfigValues: () ->
    configs = {}
    configs.tts = $("#tts").prop("checked")
    configs.lipsync = $("#lipsync").prop("checked")
    configs.streaming = $("#streaming").prop("checked")
    configs.max_new_tokens = parseInt($("#max_new_tokens").val())
    configs.avatar = @getAvatar()
    configs.generation_config = $("#model-config").val()
    configs.model_key = $("#model").val()
    configs.context = $("#context-input").val()
    configs

  sendTTSRequest: (url, text, avatar) =>
    $.ajax
      url: url
      type: 'POST'
      data:
        text: text
        config: @getConfigValues()
        authenticity_token: window._token
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

  updateStates: () ->
    ttsChecked = $('#tts').prop('checked')
    streamingChecked = $('#streaming').prop('checked')

    if ttsChecked
      if streamingChecked
        $('#lipsync').prop('checked', false)
        $('#lipsync').prop('disabled', true)
      else
        $('#lipsync').prop('checked', true)
        $('#lipsync').prop('disabled', false)
    else
      $('#lipsync').prop('checked', false)
      $('#lipsync').prop('disabled', true)

  getTTS: (text, avatar) ->
    host = window.Settings["rails"]["host"]
    port = window.Settings["rails"]["port"]
    @sendTTSRequest("http://#{host}:#{port}/v1/tts", text, avatar)

  sendInferenceRequest: (url, text) =>
    config = @getConfigValues()
    $.ajax
      url: url
      type: 'POST'
      data:
        text: text
        config: config
        authenticity_token: window._token
      success: (response) =>
        md = markdownit()
        formattedOutput = response["text"].replace(/\n/g, '<br>')
        if config["tts"] == true
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

# Events!
$(document).on('turbolinks:load', ->
  app = new App()
  app.playMp4({file_type: "mp4", filename: "/videos/#{app.getAvatar()}.mp4"})
  app.updateMaxTokensValue()
  app.updateStates()
)
