from typing import Any, Dict
from agentforge.interfaces import interface_interactor
import base64
import asyncio
import re, os, json

### Handles conversion of text to speech
class Speak:
    def __init__(self):
        self.tts = interface_interactor.get_interface("tts")
        self.w2l = interface_interactor.get_interface("w2l")
        self.redis_store = interface_interactor.create_redis_connection()
        self.pubsub = self.redis_store.pubsub()
        self.pubsub.subscribe('channel')
        self.buffer = ""

    async def event_generator(self, context: Dict[str, Any], av_type: str):
        while True:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                data = message["data"].decode("utf-8")
                should_break = self.parse_av_stream(data, context, av_type)
                if should_break:
                    break

    ### This function should take a text chunk from a stream
    ### and maintain previous text chunks by aggregating them together.
    ### When the text aggregation represents a complete sentence, execute the self.service.call
    ### parse the filename into b64 like this b64encode(fh.read()).decode()
    def parse_av_stream(self, text: str, context: Dict[str, Any], av_type: str='audio'):
        if text != '<|endoftext|>':
            self.buffer += text
        if re.search(r'[.!?]\s*$', self.buffer) or text == '<|endoftext|>':
            print(self.buffer)
            wav_response = self.tts.call({'response': self.buffer, 'avatar_config': context['model_profile']['avatar_config']})
            
            if os.path.isfile(wav_response['filename']):
                if av_type == 'video':
                    lip_sync_file = self.w2l.call({'avatar_config': context['model_profile']['avatar_config'], 'audio_response': wav_response['filename']})
                    with open(lip_sync_file['filename'], 'rb') as fh:
                        encoded_string = base64.b64encode(fh.read()).decode()
                        self.redis_store.publish('video', encoded_string)
                else:
                    with open(wav_response['filename'], 'rb') as fh:
                        encoded_string = base64.b64encode(fh.read()).decode()
                        self.redis_store.publish('audio', encoded_string)
                self.sequence_number += 1
            self.buffer = ""
        
        return True if text == '<|endoftext|>' else False

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.sequence_number = 0
        ### Synchronous example 
        if context['model_profile']['model_config']['speech'] and 'response' in context:
            wav_response = self.service.call({'response': context['response'], 'avatar_config': context['model_profile']['avatar_config']})
            if wav_response is not None:
                context['audio'] = {"audio_response": wav_response["filename"], "type": "audio/wav"}
        # Async example
        elif context['model_profile']['model_config']['video'] and context['model_profile']['model_config']['streaming']:
            asyncio.run(self.event_generator(context, 'video'))
            self.redis_store.publish('video', '<|endofvideo|>')

        elif context['model_profile']['model_config']['speech'] and context['model_profile']['model_config']['streaming']:
            asyncio.run(self.event_generator(context, 'audio'))

        return context
