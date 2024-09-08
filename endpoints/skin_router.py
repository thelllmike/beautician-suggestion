from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from inference_sdk import InferenceHTTPClient
import io
from PIL import Image

# Initialize the APIRouter
router = APIRouter()

# Initialize the InferenceHTTPClient
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="PEYGzgogxcECrVaSiZhE"
)

@router.post("/infer/skin-type/")
async def infer_skin_type(image: UploadFile = File(...)):
    try:
        # Read the image file
        image_data = await image.read()
        image_file = io.BytesIO(image_data)
        pil_image = Image.open(image_file)

        # Perform inference using the model
        result = CLIENT.infer(pil_image, model_id="skin-detection-uvj1f/3")
# skin-detection-uvj1f/3
#skin-type-detection/2
        # Return the result as a JSON response
        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
