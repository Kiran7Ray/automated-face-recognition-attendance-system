import cv2
import numpy as np
import os
import torch
from facenet_pytorch import InceptionResnetV1
from mtcnn import MTCNN

# Initialize
detector = MTCNN()
model = InceptionResnetV1(pretrained='vggface2').eval()

def get_embedding(face):
    face = cv2.resize(face, (160, 160))
    face = face.astype('float32') / 255.0
    face = np.transpose(face, (2, 0, 1))
    face = torch.tensor(face, dtype=torch.float32).unsqueeze(0)

    embedding = model(face).detach().numpy()[0]
    embedding = embedding / np.linalg.norm(embedding)  # Normalize
    return embedding

def generate_embedding(image_path, save_path):
    img = cv2.imread(image_path)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = detector.detect_faces(rgb)
    if len(results) == 0:
        print(" No face detected")
        return

    # Take largest face
    results = sorted(results, key=lambda x: x['box'][2]*x['box'][3], reverse=True)
    x, y, w, h = results[0]['box']
    face = rgb[y:y+h, x:x+w]

    embedding = get_embedding(face)

    # Save embedding
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    np.save(save_path, embedding)

    # Show detected face
    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
    cv2.imshow("Detected Face", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(f" Saved: {save_path}")

# Run
if __name__ == "__main__":
    generate_embedding("Data/kshitiz.jpg", "embeddings/kshy.npy")
