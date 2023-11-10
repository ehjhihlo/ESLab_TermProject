from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import os
from PIL import Image
from datetime import datetime

workers = 0 if os.name == 'nt' else 4

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))


# 160 is the image size after cropped
mtcnn = MTCNN(
    image_size=160, margin=0, min_face_size=20,
    thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
    device=device
)


resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


def collate_fn(x):
    return x[0]

# assume that the database is in the folder ./data/test_images
dataset = datasets.ImageFolder('./test_images')
dataset.idx_to_class = {i:c for c, i in dataset.class_to_idx.items()}
database_loader = DataLoader(dataset, collate_fn=collate_fn, num_workers=workers)
# print(dataset)


# assume that the test image is in the folder ./unknown
test_img = Image.open('./unknown/1.jpg')
test_img_cropped = mtcnn(test_img, save_path='./unknown/1_corpped.jpg')
test_img_embedding = resnet(test_img_cropped.unsqueeze(0)).detach().cpu()


database_aligned = []
database_names = []
for x, y in database_loader:
    # print(x)
    # print(y)
    x_aligned, prob = mtcnn(x, return_prob=True)
    if x_aligned is not None:
        # print('Face detected with probability: {:8f}'.format(prob))
        database_aligned.append(x_aligned)
        database_names.append(dataset.idx_to_class[y])


database_aligned = torch.stack(database_aligned).to(device)
database_embeddings = resnet(database_aligned).detach().cpu()

# print(database_embeddings.shape)
# print(test_img_embedding.shape)
alert = True
for idx, e1 in enumerate(database_embeddings):
    for e2 in test_img_embedding:
        dist = (e1 - e2).norm().item()
        # print(dist)
        if dist < 0.9:
            # print('face matched')
            alert = False 
            print('matched: ', database_names[idx]) # name
            current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S") # time
            print(current_time)
            img_save_name = f'{database_names[idx]}-{current_time}' + '.jpg'
            print(img_save_name)
            break #TODO: save time, name & picture in database
        else:
            # print('face not matched')
            continue

# TODO: send alert to server
print("alert: ", alert)


# dists = [[(e1 - e2).norm().item() for e2 in embeddings] for e1 in embeddings]
# print(pd.DataFrame(dists, columns=names, index=names))