class HomeController < ApplicationController
  before_action :authenticate_user!
  def index
    @model_configs = ["creative", "logical", "moderate"]
    @models = ["alpaca-lora-7b"]
    @avatars = ["default", "makhno", "fdr"]
    render 'home/index'
  end
end
