# Real Time Detection of Facial Expression
 A tool that can auto-send an instant alert to specific person via telegram whenever negative facial expression (eg. pain) is detected in the live camera. It is helpful in knowing any emergency needs for an elderly living alone.

### Working Principle
 The camera will periodically capture images. For each image, human face will be detected by Haar Cascade Classifier and the face image will be cropped out. The face image will be passed to a simple Convolutional Neural Network (CNN) and classify the facial expression. When pain emotion is detected in consecutive images, an alert message together with a captured image will be sent to a specific person through telegram chatbot. 
![](images\workflow.jpg)

### Data source for CNN training
 For 'Neutral' and 'Happy' emotion images, they come from [FER2013 in kaggle](https://www.kaggle.com/nicolejyt/facialexpressionrecognition).
 
 For 'Pain' emotion images, they come from [2D face sets](http://pics.stir.ac.uk/2D_face_sets.htm). Since the number of 'pain' images is far lower than that of 'Neutral' and 'Happy', selfies of our 'pain' expression are also used. 
 
 ![](images\dataset.jpg)
