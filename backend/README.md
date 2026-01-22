# ImageMagick LLM Agent

**ImageMagick LLM Agent** is a full-stack application that lets you edit images using natural language instructions.  
It combines a modern React frontend with a FastAPI backend powered by LangGraph,  translating user intent into safe, executable ImageMagick commands.

**Live demo:**  
https://imagemagick-agent.vercel.app/

---

## How it works

1. The user uploads an image and writes a natural-language instruction  
   (for example: *“Resize this image to 128x128 and convert it to grayscale”*).

2. The backend agent:
   - Interprets the request using an LLM 
   - Produces a constrained ImageMagick command
   - Validates and executes the command safely

3. The processed image is returned to the browser.

The system is intentionally split into **planning** and **execution** steps using LangGraph, mirroring real-world agent design patterns.

---

## Tech stack

### Frontend
- Vite
- React
- TypeScript
- Tailwind CSS
- Deployed on Vercel

### Backend
- Python
- FastAPI
- LangChain
- LangGraph
- Google Gemini API (For now, I'm planning to add others in the future)
- ImageMagick (CLI)
- Docker
- Deployed on Railway