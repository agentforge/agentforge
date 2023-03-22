class HomeController < ApplicationController
  def index
    @model_configs = ["creative-alpaca-lora-7b"]
    @models = ["alpaca-lora-7b"]
    @avatars = ["default", "makhno"]  
    render 'home/index'
  end
end
