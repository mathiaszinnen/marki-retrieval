import os
import numpy as np
import faiss
from PIL import Image
from tqdm import tqdm
from feature_extractor import ResNetFeatureExtractor

def build_faiss_index(image_dir, output_dir):
    image_paths = []
    feature_list = []
    extractor = ResNetFeatureExtractor()

    for filename in tqdm(os.listdir(image_dir)):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            path = os.path.join(image_dir, filename)
            image = Image.open(path).convert('RGB')
            features = extractor.extract(image)  # shape (D,)
            feature_list.append(features)
            image_paths.append(filename)

    features_np = np.stack(feature_list).astype('float32')  # shape (N, D)

    # Create FAISS index (L2 similarity, D = feature dim)
    dim = features_np.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(features_np)

    # Save index and mapping
    faiss.write_index(index, os.path.join(output_dir, 'faiss.index'))
    np.save(os.path.join(output_dir, 'filenames.npy'), np.array(image_paths))

    print(f"Saved FAISS index and filenames to {output_dir}")

if __name__ == "__main__":
    image_dir = os.path.expanduser("~/data/marki/images")
    output_dir = "webservice/data"
    build_faiss_index(image_dir, output_dir)
