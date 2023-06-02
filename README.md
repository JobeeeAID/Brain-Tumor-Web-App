# Brain-Tumor-Web-App

A brain tumor detection web app using and training the VGG19 model on a dataset found on kaggle here : https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection?resource=download.

The app is made using Flask Framework and containerized on docker.

To run the app locally just clone the repo and run :

    > docker build --tag brain-tumor-image
    > docker run -d -p 5000:5000 brain-tumor-image

You can also see the project live deploiyed on web using Render.

Follow this link :

https://brain-tumor-app.onrender.com/
