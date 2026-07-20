import easyocr
import numpy as np
from PIL import Image

# Create reader once
reader = easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(uploaded_file):

    image = Image.open(uploaded_file).convert("RGB")

    image = np.array(image)

    results = reader.readtext(image)

    text = "\n".join([r[1] for r in results])

    return text