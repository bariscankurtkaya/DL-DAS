# Deep Learning based Driver Assistance System (DL-DAS)


## Paper Abstract:

Nowadays, vehicles have become an integral part of our lives due to mobility advantages. However, traffic accidents continue to occur worldwide. This study aims to develop a pure image-based solution using a combination of "deep learning" and "image processing" techniques to minimize the occurrence of traffic accidents. While the You Only Look Once (YOLO) algorithm is one of the fastest object detection algorithms, it faces slight accuracy and robustness problems. Afterward, the YOLO algorithm with Darknet-53 architecture, which is pre-trained with COCO Dataset, has faced reliability issues to detect objects in "Night" images while getting high results on "Day" images. Therefore, we suspect that the COCO Dataset is inclined toward brighter images rather than low-light ones. To support this idea with scientific evidence, we analyzed the COCO Dataset. Besides, to overcome this issue, finetuning and classifier filter design have been proposed. Additionally, lane detection systems were developed to improve the reliability of the feedback system. As a result, the classifier filter system achieved 99.92% accuracy in distinguishing between "Night" and "Day" images. After evaluation processes, the proposed system achieved ~0.92 IOU with YOLOV3 fine-tuned model and ~0.95 IOU with YOLOV4 fine-tuned model. Furthermore, the lane detection algorithm achieved 88.00% accuracy.


## Algorithm Procedure:

<div align="center">

|Filter creation algorithm|
|------|

<img width="425" height="300" alt="filterCreationAlgorithm" src="https://user-images.githubusercontent.com/33360380/197346926-fb2197c8-2cf6-4475-9f18-e45e0b6c3e6c.png"> 

|Filter algorithm|
|-------|
<img width="425" height="300" alt="filterAlgorithm" src="https://user-images.githubusercontent.com/33360380/197347263-a598d1ae-bbfb-4a82-aaf8-fc3f64510761.png">

|Flowchart|
|----|

```mermaid
flowchart TD
    A[Start] --> B[Taking Image]
    B --> C[Filter Algorithm]
    C --> D{Is image from night?}
    D --> |YES| E[Use Model Tuned with Oxford Robotcar Dataset]
    D --> |NO| F[Use Pretrained Yolo Model with COCO]
    E --> G[Object and Lane Detection]
    F --> G
    G --> H{Are there any object between lanes?}
    H --> |YES| I[Distance Calculation]
    H --> |NO| L{Is our car inside between lanes?}
    I --> J{Are there enough distance?}
    J --> |Yes| L
    J --> |NO| K[Warn the driver!]
    L --> |YES| B
    L --> |NO| K
    K --> B
```
</div>

## Results:
###### Day and night image matrice values:

<div align="center">

|Before filter|After filter|
|---------|---------------|

|<img width="350" height="300" alt="beforeFilter" src="https://user-images.githubusercontent.com/33360380/197346797-6d2a9d74-6754-426b-9bcf-afcec6933243.png"><img width="350" height="300" alt="afterFilter" src="https://user-images.githubusercontent.com/33360380/197346805-dc0b8409-6808-41d8-99e1-157f22ed7118.png">|
</div>
