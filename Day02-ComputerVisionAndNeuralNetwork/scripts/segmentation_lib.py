import torchvision
import numpy as np
from PIL import Image

PREPROCESSING_ROUTINE = torchvision.transforms.Compose([
    torchvision.transforms.ToTensor(),
    torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def ottieni_output_rete(immagine, rete, preprocessamento=PREPROCESSING_ROUTINE):
    rete.eval()
    immagine_preprocessata = preprocessamento(immagine)
    immagine_preprocessata = immagine_preprocessata.unsqueeze(0)
    return rete(immagine_preprocessata)

def decode_segmap(image, nc=21):
    label_colors = np.array([(0, 0, 0),  # 0=background
                   # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                   (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                   # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                   (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                   # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                   (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                   # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                   (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)
    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
    rgb = np.stack([r, g, b], axis=2)

    return Image.fromarray(rgb)