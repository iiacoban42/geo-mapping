###Overview

This directory contains object-detection model, training data and validation data.

Object-detection algorithm reads a directory of **images coupled with XML files**. XML files denote object names and coordinates in images.

###To add more training data:
1. Find an image with an object of your interest `//Currently only churches are supported`
2. Run labelImg in terminal ([here](https://towardsdatascience.com/build-a-custom-trained-object-detection-model-with-5-lines-of-code-713ba7f6c0fb) you can see how to use it)
3. Draw a box around the object in image and label it. Click save. This labeled image will be saved as .xml file