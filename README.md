# marki-retrieval
This project provides a simple web service for retrieving visually similar goldsmith marks of the MarKI project of the GNM. It's built using **FastAPI** and uses **ResNet-50** (from `torchvision`) for feature extraction and **FAISS** for fast similarity search. It is currently work in progress.


## Project Structure
```
marki-retrieval/
├── preparation/ 
│ ├── build_index.py # prepare the feature index for the webservice
│ ├── collect_images.py # download images from gnm wisski instance
│ ├── analysis.py 
│ └── feature_extractor.py
├── webservice/ # FastAPI service
│ ├── main.py # API endpoints
│ ├── faiss_backend.py # FAISS index utilities
│ └── data/ # Index and filenames
├── notebooks/ 
│ └── retrieval_demo.ipynb # test the query API of the running service
└── tests/ 
```


---

## Running the Service Locally

1. **Install requirements:**

```bash
pip install -e .
```
2. **Prepare data**

- download images using `collect_images.py`
- build feature index using `build_index.py`

3. **Webservice**

- Start the FastAPI service using uvicorn webservice.main:app --reload
- The service will be available at: http://localhost:8000

4. **Try it out**

- To try the webservice, refer to the demo [notebook](notebooks/retrieval_demo.ipynb) 

## API Endpoints
`POST /retrieve/{top_k}`

Find the top k most similar images.

    Path parameter: top_k: number of similar images to return

    Body: Upload image file (multipart/form-data)

Example (with curl):

```
curl -X POST http://localhost:8000/retrieve/5 \
  -F "file=@path/to/query_image.jpg"
```
