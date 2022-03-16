import requests
import base64
import io
from PIL import Image
import json

class DetectInRoboflow:
    def detectRoboflow(imagePath):
        MY_KEY = "2Wsz5yUEGz8rNFAIyCyw"
        image = Image.open(imagePath).convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, quality=90, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        img_str = img_str.decode("ascii")

        upload_url = "".join([
            "https://detect.roboflow.com/leonberger/2",
            "?api_key="+MY_KEY,
            "&name="+imagePath
        ])
        r = requests.post(upload_url, data=img_str, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })

        y = json.loads(str(r.json()).replace("'",'"'))
        y = y["predictions"]

        if not y:
            return "",0
            
        return y[0]["class"], y[0]["confidence"]
