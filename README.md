# image 3D rotation

## Image

Use ```image_rotation.py``` to rotate your image!

Before | After
------------ | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_demo.jpg?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_rotate.jpg?raw=true" width="203" height="303">


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

<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_mask.jpg?raw=true" width="203" height="203">

## Labels

Transform your labels

Before | After
------------ | -------------
<img src="https://github.com/DanielHry/imageTransform/blob/main/demo/image_demo_labels.jpg?raw=true" width="200" height="200"> | <img src="https://github.com/DanielHry/imageTransform/blob/main/demo/img_rotate_labels.jpg?raw=true" width="203" height="203">


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
