from roboflow import Roboflow
rf = Roboflow(api_key="coanWLXOg08ty4ufts0H")
project = rf.workspace().project("leonberger-kkm3f")
dataset = project.version(1).download("yolov5")
for d in dataset:
    print(d)