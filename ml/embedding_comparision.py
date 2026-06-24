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
    face = torch.tensor(face).unsqueeze(0)

    embedding = model(face).detach().numpy()[0]
    embedding = embedding / np.linalg.norm(embedding)  # Normalize
    return embedding

def load_database(path="embeddings"):
    database = {}
    for file in os.listdir(path):
        if file.endswith(".npy"):
            name = file.split(".")[0]
            database[name] = np.load(os.path.join(path, file))
    print("Loaded:", database.keys())
    return database

def recognize_video(video_path):
    database = load_database()
    cap = cv2.VideoCapture(video_path)

    THRESHOLD = 1.2   # Adjust as needed

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = detector.detect_faces(rgb)

        for r in results:
            x, y, w, h = r['box']
            x, y = max(0, x), max(0, y)
            face = rgb[y:y+h, x:x+w]

            if face.size == 0:
                continue

            embedding = get_embedding(face)

            min_dist = float("inf")
            identity = "Unknown"

            for name, db_emb in database.items():
                dist = np.linalg.norm(embedding - db_emb)
                print(f"{name}: {dist:.2f}")
                if dist < min_dist:
                    min_dist = dist
                    identity = name

            print("BEST:", identity, min_dist)

            if min_dist < THRESHOLD:
                label = identity
                color = (0,255,0)
            else:
                label = "Unknown"
                color = (0,0,255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame,
                        f"{label} {min_dist:.2f}",
                        (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        color,
                        2)

        cv2.imshow("Recognition", frame)
        if cv2.waitKey(1) == 27:  # ESC to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# Run
if __name__ == "__main__":
    recognize_video("Data/vdo1.mp4")