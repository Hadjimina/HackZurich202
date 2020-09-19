from torchvision import models
import torchvision.transforms as T
import os
from PIL import Image
import matplotlib.pyplot as plt
import torch
import numpy as np
import cv2

# Define the helper function
def decode_segmap(image, nc=21):
  label_colors = np.array([(150, 150, 150),  # 0=background
               # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
               (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
               # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
               (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
               # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
               (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (0, 0, 0), #(192, 128, 128),
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
  return rgb

def segment(net, path, show_orig=True, dev='cpu'):
  img = Image.open(path)
  #if show_orig: plt.imshow(img); plt.axis('off'); plt.show()
  # Comment the Resize and CenterCrop for better inference results
  trf = T.Compose([#T.Resize(640),
                   #T.CenterCrop(224),
                   T.ToTensor(),
                   T.Normalize(mean = [0.485, 0.456, 0.406],
                               std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0).to(dev)
  out = net.to(dev)(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  rgb = decode_segmap(om)

  ## create fg/bg mask
  seg_gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
  _,fg_mask = cv2.threshold(seg_gray, 0, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
  _,bg_mask = cv2.threshold(seg_gray, 0, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

  ## convert mask to 3-channels
  fg_mask = cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)
  bg_mask = cv2.cvtColor(bg_mask, cv2.COLOR_GRAY2BGR)

  ## cv2.bitwise_and to extract the region
  img = cv2.imread(path)
  bg = cv2.bitwise_and(img, fg_mask)
  fg = cv2.bitwise_and(img, bg_mask)

  #plt.imshow(fg); plt.axis('off'); plt.show()
  return(fg, bg)

def checkBackgroundEdges(path):
  dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
  img = segment(dlab, os.path.abspath(path))[1]
  edges = cv2.Canny(img,100,200)
  #plt.imshow(edges); plt.axis('off'); plt.show()
  #plt.hist(edges.ravel(), bins=256, range=(0, 255), fc='k', ec='k'); plt.show() #calculating histogram

  nr_white_pixels = np.sum(edges == 255)
  nr_black_pixels = np.sum(edges == 0)
  edge_coef = nr_white_pixels / nr_black_pixels
  #print(edge_coef)
  return 1 if(edge_coef > 0.1) else 0

#checkBackgroundEdges("pictures\\bad\\b4.png")
#dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()
#print(checkBackgroundEdges(segment(dlab, os.path.abspath("pictures\\bad\\b1.png"))[1]))
