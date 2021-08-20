# image 3D rotation

## Image

Use ```image_rotation.py``` to rotate your image!

Before | After
------------ | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_demo.jpg?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_rotate.jpg?raw=true" width="217" height="272">


Example:

```
image_rotation.py ${IMPUT_IMAGE} ${OUTPUT_PATH} [--theta] [--phi] [--gamma]
```

- theta : rotation around the x axis

- phi   : rotation around the y axis

- gamma : rotation around the z axis

```
python image_rotation.py demo/image_demo.jpg demo/img_rotate.jpg --theta 26 --phi 43 --gamma -66
```

## Mask

You can specify ```[--mask]``` to export the mask:

<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_mask.jpg?raw=true" width="217" height="272">

## Labels

Transform your labels

Before | After
------------ | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_demo_labels.jpg?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_rotate_labels.jpg?raw=true" width="217" height="272">


Example:

```
python image_rotation.py \
    ${IMPUT_IMAGE} \
    ${OUTPUT_PATH} \
    [--theta ${THETA}] \
    [--phi ${PHI}] \
    [--gamma ${GAMMA}] \
    [--labels ${TXT_FILE}] \
    [--labels-out ${OUTPTU_TXT_PATH}]
```

```
python image_rotation.py demo/image_demo.jpg demo/img_rotate.jpg --theta 26 --phi 43 --gamma -66 --mask demo/img_mask.jpg --labels demo/image_demo_labels.txt --labels-out demo/img_rotate_labels.txt
```

# Other Image transformations

image foreground | mask | image background
------------ | ------------- | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/graff.png?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/graff_mask.jpg?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/graffeur.jpg?raw=true" width="341" height="218">


Example:
```
from transformers import (rotate_layer, blend_layers, scale_layer, 
                          resize_poly, rotate_poly, translate_poly)
                          
scale = 0.8
image_fg = scale_layer(image_fg, scale)
image_fg_mask = scale_layer(image_fg_mask, scale)
poly = data["polygon"]
poly = resize_poly(poly, scale)


dicRotation = {'theta':-5, 'phi':-40, 'gamma':-10}
images_rotated = rotate_layer([image_fg, image_fg_mask], dicRotation)
image_fg, image_fg_mask = images_rotated
poly = rotate_poly(poly)


result = blend_layers(image_fg, image_bg, image_fg_mask, position=(275,70), opacity=0.85)
poly = translate_poly(poly, y=70, x=275)
```

Result:
image | polygones
------------ | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_blend01.png?raw=true" width="381" height="248"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_blend.png?raw=true" width="381" height="248">
