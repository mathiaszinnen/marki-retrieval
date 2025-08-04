import os
from fastapi.testclient import TestClient
from webservice.main import app

client = TestClient(app)

def test_retrieve_similar_images():
    # Path to a test image (must exist!)
    test_image_path = "tests/test_data/BZ0152a.jpg"
    
    with open(test_image_path, "rb") as img_file:
        response = client.post(
            "/retrieve/3",
            files={"file": ("BZ0152a.jpg", img_file, "image/jpeg")}
        )

    assert response.status_code == 200
    json_data = response.json()

    # Basic checks
    print(f"Retrieved {len(json_data['similar_images'])} similar images.")
    print("Retrieved image names: ", json_data.get('similar_images'))
    assert "filename" in json_data
    assert json_data["filename"] == "BZ0152a.jpg"
    assert "similar_images" in json_data
    assert isinstance(json_data["similar_images"], list)
    assert len(json_data["similar_images"]) <= 3
