class InferenceController < ApplicationController

  def interpret
    # Calls interpret API and takes request data and called inference engine to produce
    # an automated response
    
    
    render json: { text: "hello" }
  end
end
