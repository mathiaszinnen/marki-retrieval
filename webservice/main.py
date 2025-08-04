from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

from preparation.feature_extractor import ResNetFeatureExtractor
# from preparation.classifier import predict_class  # TODO
from webservice.faiss_backend import load_faiss_index, query_index

app = FastAPI()

# Load feature index at startup (dictionary: {filename: feature_vector})
INDEX, FILENAMES = load_faiss_index("webservice/data/faiss.index", "webservice/data/filenames.npy")
extractor = ResNetFeatureExtractor()


@app.get("/")
def root():
    return {"status": "ok"}
    
def read_imagefile(file: UploadFile) -> Image.Image:
    return Image.open(io.BytesIO(file.file.read())).convert("RGB")


@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    image = read_imagefile(file)
    raise NotImplementedError


@app.post("/retrieve/{top_k}")
async def retrieve_similar_images(top_k: int, file: UploadFile = File(...)) -> JSONResponse:
    image = read_imagefile(file)
    query_features = extractor.extract(image)

    # Return top K similar filenames
    similar_files = query_index(INDEX, FILENAMES, query_features, top_k=top_k)

    return JSONResponse(content={"filename": file.filename, "similar_images": similar_files})
