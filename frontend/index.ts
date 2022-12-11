import axios from "axios";

// Define the URL of the API
const API_URL = "http://localhost:3000";

// Define the TTS function
async function tts(text: string, filename: string): Promise<void> {
  try {
    // Make a POST request to the /tts endpoint
    const response = await axios.post(`${API_URL}/tts`, {
      text,
      filename
    });

    // Check if the response is successful
    if (response.status === 200) {
      // Get the wav file from the response
      const wavFile = response.data;

      // Play the wav file
      // TODO: Add code to play the wav file here

      // Display the text on screen
      // TODO: Add code to display the text on screen here
    } else {
      // Handle error
      // TODO: Add code to handle error here
    }
  } catch (error) {
    // Handle error
    // TODO: Add code to handle error here
  }
}

// Define the chat function
async function chat(message: string): Promise<string> {
  try {
    // Make a POST request to the /chat endpoint
    const response = await axios.post(`${API_URL}/chat`, {
      message
    });

    // Check if the response is successful
    if (response.status === 200) {
      // Return the response from the chatbot
      return response.data.response;
    } else {
      // Handle error
      // TODO: Add code to handle error here
    }
  } catch (error) {
    // Handle error
    // TODO: Add code to handle error here
  }
}

// Define the interpret function
async function interpret(): Promise<string> {
  try {
    //
    // Record the voice of the user
    // TODO: Add code to record the voice of the user here

    // Make a POST request to the /interpret endpoint
    const response = await axios.post(`${API_URL}/interpret`, {
      // TODO: Add code to send the recorded voice as a file in the request here
    });

    // Check if the response is successful
    if (response.status === 200) {
      // Return the interpreted text from the voice
      return response.data.text;
    } else {
      // Handle error
      // TODO: Add code to handle error here
    }
  } catch (error) {
    // Handle error
    // TODO: Add code to handle error here
    }
}
    
// Use the TTS function
tts("Hello, I am a text-to-speech system.", "hello.wav");

// Use the chat function
chat("Hello, I am a human.").then(response => {
  console.log(response);
});

// Use the interpret function
interpret().then(text => {
  console.log(text);
});