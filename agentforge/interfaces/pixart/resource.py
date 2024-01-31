import gc, os

### Manages Base Image Generation ###
class PixArtGenerator():
  def __init__(self,  config: dict = None) -> None:
    self.config = {} if config == None else config
    
  def load_model(self, config: dict) -> None:
    pass

  async def generate(self, text: str, **kwargs) -> str:
    pass