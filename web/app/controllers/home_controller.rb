class HomeController < ApplicationController
  def index
    @model_configs = ["creative", "logical", "moderate"]
    @models = ["alpaca-lora-7b"]
    @avatars = ["default", "makhno"]
    render 'home/index'
  end
end
