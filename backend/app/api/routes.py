from fastapi import APIRouter, UploadFile, Form, Request
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
from utils.image_utils import extract_metadata

router = APIRouter()

INPUT_DIR = Path("images/input")
OUTPUT_DIR = Path("images/output")


@router.post("/edit")
async def edit_image(request: Request, image: UploadFile, prompt: str = Form(...)):
    # Save input file
    input_id = f"{uuid.uuid4()}_{image.filename}"
    input_path = INPUT_DIR / input_id

    with input_path.open("wb") as f:
        f.write(await image.read())

    # Get image metadata
    image_metadata = extract_metadata(input_path)
    # Run agent
    agent = request.app.state.agent
    print("Prompt:", prompt)
    result = agent.invoke(
        {
            "user_request": prompt,
            "input_path": str(input_path),
            "image_metadata": image_metadata,
        }
    )

    print("Result:", result)

    # Delete input file
    # input_path.unlink()

    # if result.get("error"):
    #     return {"error": result["error"]}

    # output_path = result["result_path"]

    # return FileResponse(path=output_path, media_type="image/png", filename="result.png")


@router.get("/health")
def health():
    return {"status": "ok"}
