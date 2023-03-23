class HomeController < ApplicationController
  def index
    @model_configs = ["llm/creative", "llm/logical", "llm/moderate"]
    @models = ["alpaca-lora-7b"]
    @avatars = ["default", "makhno"]  
    render 'home/index'
  end
end
