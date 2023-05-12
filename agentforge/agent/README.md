# How to Create an Avatar

This describes the current process of how to create and integrate a new avatar. 

1. Pick a historical or fictional character, find a high quality illustration or generate one with a diffusion model.
2. Find biographical information about the character or make one up, wikipedia is usually a good source. Replace all references in the 3rd person to the personal pronoun "you" so the instruct-tuned model takes this as instruction and assumes the personality.
3. Find a short high quality voice clip (> 2min) with very little noise. If this is a youtube video there is a helper script in the scripts folder to download and chunk it. Otherwise save the voice clip as a wav file. We can use a zero-shot TTS like YouTTS with this as the source. In the future we can create an automated fine-tuning pipeline but dataset generation for this is not as trivial as YouTTS.

```
cd scripts/
python youtub2wav.py
```
4. Go to [exh.ai](exh.ai) and create an account. You can create a "Talking Head" which will generate an idle animation. Oftentimes this will not work with some images and you will need to find a new image. Right click to open the video in a new tab and download it.
5. Take this information and create a JSON file in the `config/configs/avatars` folder like the following:

```
{
  "avatar": "fdr",
  "prompt_context": {
    "context": "You are Franklin Delano Roosevelt born on January 30, 1882 and died on April 12, 1945, commonly known as FDR. You were American statesman...",
    "name": "Franlkin D. Roosevelt"
  },
  "speaker_wav": "/audio/fdr/fdr.wav",
  "mp4": "fdr.mp4"
}
```
6. There are 2 places where the avatars are currently hard-coded that needs to access the API/database alternatively. To implement an avatar currently we must alter these files:

-  /home/fragro/Development/agent_n/personaforge/app/(forge)/forge/app.tsx
- /home/fragro/Development/agent_n/agentforge/wav2lip/app.py