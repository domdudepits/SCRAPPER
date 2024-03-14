from fastai.vision.all import *


foodpath = untar_data(URLs.FOOD)
print(get_image_files(foodpath))