import os
from langchain.memory import MongoDBChatMessageHistory
from agentforge.config import DbConfig
from urllib.parse import quote_plus
from agentforge.utils.time import get_mongo_timestamp

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Literal, TypedDict, Union, cast

from pydantic import BaseModel, PrivateAttr, Field

### THis is a bunch of stuff to deal with the fact that the latest version of langchain
### doesn't work with the latest version of Deeplake

class BaseSerialized(TypedDict):
    """Base class for serialized objects."""

    lc: int
    id: List[str]


class SerializedConstructor(BaseSerialized):
    """Serialized constructor."""

    type: Literal["constructor"]
    kwargs: Dict[str, Any]


class SerializedSecret(BaseSerialized):
    """Serialized secret."""

    type: Literal["secret"]


class SerializedNotImplemented(BaseSerialized):
    """Serialized not implemented."""

    type: Literal["not_implemented"]


class Serializable(BaseModel, ABC):
    """Serializable base class."""

    @property
    def lc_serializable(self) -> bool:
        """
        Return whether or not the class is serializable.
        """
        return False

    @property
    def lc_namespace(self) -> List[str]:
        """
        Return the namespace of the langchain object.
        eg. ["langchain", "llms", "openai"]
        """
        return self.__class__.__module__.split(".")

    @property
    def lc_secrets(self) -> Dict[str, str]:
        """
        Return a map of constructor argument names to secret ids.
        eg. {"openai_api_key": "OPENAI_API_KEY"}
        """
        return dict()

    @property
    def lc_attributes(self) -> Dict:
        """
        Return a list of attribute names that should be included in the
        serialized kwargs. These attributes must be accepted by the
        constructor.
        """
        return {}

    class Config:
        extra = "ignore"

    _lc_kwargs = PrivateAttr(default_factory=dict)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._lc_kwargs = kwargs

    def to_json(self) -> Union[SerializedConstructor, SerializedNotImplemented]:
        if not self.lc_serializable:
            return self.to_json_not_implemented()

        secrets = dict()
        # Get latest values for kwargs if there is an attribute with same name
        lc_kwargs = {
            k: getattr(self, k, v)
            for k, v in self._lc_kwargs.items()
            if not (self.__exclude_fields__ or {}).get(k, False)  # type: ignore
        }

        # Merge the lc_secrets and lc_attributes from every class in the MRO
        for cls in [None, *self.__class__.mro()]:
            # Once we get to Serializable, we're done
            if cls is Serializable:
                break

            # Get a reference to self bound to each class in the MRO
            this = cast(Serializable, self if cls is None else super(cls, self))

            secrets.update(this.lc_secrets)
            lc_kwargs.update(this.lc_attributes)

        # include all secrets, even if not specified in kwargs
        # as these secrets may be passed as an environment variable instead
        for key in secrets.keys():
            secret_value = getattr(self, key, None) or lc_kwargs.get(key)
            if secret_value is not None:
                lc_kwargs.update({key: secret_value})

        return {
            "lc": 1,
            "type": "constructor",
            "id": [*self.lc_namespace, self.__class__.__name__],
            "kwargs": lc_kwargs
            if not secrets
            else _replace_secrets(lc_kwargs, secrets),
        }

    def to_json_not_implemented(self) -> SerializedNotImplemented:
        return to_json_not_implemented(self)


class BaseMessage(Serializable):
    """The base abstract Message class.

    Messages are the inputs and outputs of ChatModels.
    """

    content: str
    """The string contents of the message."""

    additional_kwargs: dict = Field(default_factory=dict)
    """Any additional information."""

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the Message, used for serialization."""

    @property
    def lc_serializable(self) -> bool:
        """Whether this class is LangChain serializable."""
        return True


class HumanMessage(BaseMessage):
    """A Message from a human."""

    example: bool = False
    """Whether this Message is being passed in to the model as part of an example 
        conversation.
    """

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "human"


class AIMessage(BaseMessage):
    """A Message from an AI."""

    example: bool = False
    """Whether this Message is being passed in to the model as part of an example 
        conversation.
    """

    @property
    def type(self) -> str:
        """Type of the message, used for serialization."""
        return "ai"

### Working memory chat store
class MongoMemory:
  def __init__(self, config: DbConfig):
    self.config = config
    self.short_term_memory = None

  def connect(self, user_id, session_id):
    username = quote_plus(self.config.username)
    password = quote_plus(self.config.password)
    host = self.config.host
    port = self.config.port
    connection_string = f"mongodb://{username}:{password}@{host}:{port}"
    session = f"{user_id}-{session_id}"
    self.short_term_memory = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=session, database_name=os.environ.get("DB_NAME")
    )

  # Stores memory for various agent avatars
  def setup_memory(self, human_prefix: str, ai_prefix: str, user_id: str, session_id: str):
    if not self.short_term_memory:
      self.connect(user_id, session_id)
    self.human_prefix = human_prefix
    self.ai_prefix = ai_prefix

  # Saves a response from another individual to short-term memory
  def remember(self, user: str, agent: str, prompt: str, response: str):
    # Do not save empty interactions
    if prompt.strip() == "":
      return
    if self.short_term_memory:
        interaction_time = {"interaction_time": get_mongo_timestamp()}
        self.short_term_memory.add_message(HumanMessage(content=prompt, additional_kwargs=interaction_time))
        self.short_term_memory.add_message(AIMessage(content=response, additional_kwargs=interaction_time))

  # Returns the last 5 interactions from the short term memory
  def recall(self, user: str, agent: str, n: int = 5):
      mem = self.short_term_memory.messages
      def get_content(obj):
          prefix = f"{self.human_prefix}: " if obj.__class__.__name__ == "HumanMessage" else f"{self.ai_prefix}: "
          # postfix = f" {self.human_postfix}" if obj.__class__.__name__ == "HumanMessage" else f" {self.human_postfix}"
          return prefix + obj.content # + postfix
      # TODO: Need a more robust way to ensure we don't hit token limit for prompt
      hist = "\n".join(list(map(lambda obj: get_content(obj), mem[-5:])))
      return hist
