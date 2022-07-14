# FaceMask-Detector-ViAC
  The coronavirus epidemic has given rise to an extraordinary degree of worldwide scientific cooperation. Artificial Intelligence (AI) based on Machine learning and Deep Learning can help to fight Covid-19 in many ways.
  
We are developing a system that will detect or measure the following factors:
1. Face-Mask Detection.
2. Human Body Temperature.
3. Oxygen Percentage in Body.
4. Visitor Identification(Face Recognition over Mask). 

Technology holds the key here. We introduce as ystem that can detect instances where face masks are not used. We are proposing a system that is capable of detecting masked and unmasked faces and can be integrated with pre-installed CCTV cameras. This will help track safety violations, promote the use of face masks, and ensure a safe working environment.

## 🚀&nbsp; Installation
1. Clone the repo
```
$ git clone https://github.com/frosty1011/FaceMask-Detector-ViAC.git
```

2. Change your directory to the cloned repo 
```
$ cd FaceMask-Detector-ViAC
```

3. Create a Python virtual environment named 'test' and activate it
```
$ virtualenv test
```
```
$ .\test/bin/activate
```

4. Now, run the following command in your Terminal/Command Prompt to install the libraries required
```
$ pip install -r requirements.txt
```
```
$ pip install tensorflow
```

5. Create a folder named f1, and add images of employees with their respective names as the image name.

7. In app.py file, 
Assign employees names and phone numbers in dictionary format to condir variable.
Eg : condir={"nehul":"99999999","rohit":"9888888"}

8. Now, run the following command in your Terminal/Command Prompt to create a database for records.
```
$ python createdb.py
```

## :bulb: Working

1. Open terminal. Go into the cloned project directory and type the following command:
```
$ python train_mask_detector.py --dataset dataset
```

2. To start ViAC :
```
$ python3 app.py 
```

3. Go to http://127.0.0.1:5000/ on any web browser to access the UI
