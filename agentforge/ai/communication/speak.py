from typing import Any, Dict
from agentforge.interfaces import interface_interactor
import base64
import asyncio
import re, os, json, time, threading

### COMMUNICATION: Handles conversion of text to speech
class Speak:
    def __init__(self):
        self.tts = interface_interactor.get_interface("tts")
        self.w2l = interface_interactor.get_interface("w2l")
        self.redis_store = interface_interactor.create_redis_connection()
        self.pubsub = self.redis_store.pubsub()

    def event_generator(self, context: Dict[str, Any], av_type: str):
        self.pubsub.subscribe('channel') # TODO: Make user specific for multi-user
        while True:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = message["data"].decode("utf-8")
                should_break = self.parse_av_stream(data, context, av_type)
                if should_break:
                    self.redis_store.publish('video', '<|endofvideo|>')
                    self.pubsub.unsubscribe('channel')
                    break
            else:
                time.sleep(0.1) # TODO: make this backoff

    ### This function should take a text chunk from a stream
    ### and maintain previous text chunks by aggregating them together.
    ### When the text aggregation represents a complete sentence, execute the self.service.call
    ### parse the filename into b64 like this b64encode(fh.read()).decode()
    def parse_av_stream(self, text: str, context: Dict[str, Any], av_type: str='audio'):
        if text != '<|endoftext|>':
            self.buffer += text
        if re.search(r'[.!?]\s*$', self.buffer) or text == '<|endoftext|>' and self.buffer != '':
            print("buffer", self.buffer)
            wav_response = self.tts.call({'response': self.buffer, 'avatar_config': context.get('model.avatar_config')})

            if os.path.isfile(wav_response['filename']):
                if av_type == 'video':
                    lip_sync_file = self.w2l.call({'avatar_config': context.get('model.avatar_config'), 'audio_response': wav_response['filename']})
                    with open(lip_sync_file['filename'], 'rb') as fh:
                        encoded_string = base64.b64encode(fh.read()).decode()
                        data = {'data': encoded_string, "id": str(context._id)}
                        self.redis_store.publish('video', json.dumps(data))
                else:
                    with open(wav_response['filename'], 'rb') as fh:
                        encoded_string = base64.b64encode(fh.read()).decode()
                        self.redis_store.publish('audio', encoded_string)
                self.sequence_number += 1
            self.buffer = ""
            print(f"{self.buffer=}")

        return True if text == '<|endoftext|>' else False

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.buffer = ""
        self.sequence_number = 0
        ### Synchronous example
        print("EXECUTING SPEAK!")

        if context.get('model.model_config.speech') and context.has_key('response'):
            wav_response = self.tts.call({'response': context['response'], 'avatar_config': context['model_profile']['avatar_config']})
            if wav_response is not None:
                context['audio'] = {"audio_response": wav_response["filename"], "type": "audio/wav"}

        if context.get('model.model_config.video') and context.get('model.model_config.streaming'):
            threading.Thread(target=self.event_generator, args=(context, 'video')).start()
        elif context.get('model.model_config.speech') and context.get('model.model_config.streaming'):
            threading.Thread(target=self.event_generator, args=(context, 'audio')).start()

        return context

