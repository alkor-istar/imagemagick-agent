# ImageMagick LLM Agent

ImageMagick LLM Agent is a full-stack application that lets you edit images using natural language.  
You upload an image, describe what you want (“resize to 256x256”, “crop the center”, “convert to PNG”), 
and an LLM-powered agent plans and executes the correct ImageMagick commands for you.

ImageMagick is a free, open-source software suite, used for editing and manipulating digital images. 
Check their webpage here https://imagemagick.org/ or give it a try in any linux distro. 

It looks like this:
https://github.com/alkor-istar/imagemagick-agent/releases/download/untagged-ea653583244bacd27188/Screencast.mp4

Live app:  
https://imagemagick-agent.vercel.app/
The backend on this deployment is not always online, please send me a message if you want to have try.

---

## Features

- Natural language image editing
- ImageMagick execution via a safe, structured command layer
- Multi-step plans (resize → crop → convert, etc.)
- LLM-powered planning and command generation
- Typed commands using Pydantic schemas
- LangGraph state machine for agent control flow
- FastAPI backend
- React + Vite + Tailwind frontend
- Dockerized backend
- Deployed backend on Railway, frontend on Vercel

---

## Todo
 - Frontend / backend authentication
 - More LLM backends.
 - Find which is the simplest and cheapest LLM I can get this running with
 - Better logging
 - Better user feedback
