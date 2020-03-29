import cv2
from PIL import Image
import torchvision.transforms as transforms
import torch
import module_loader

preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def get_frame_images():
    # Read the video from specified path
    cam = cv2.VideoCapture("static/demo.mp4")

    # frame
    imgs = []
    while (True):
        # reading from frame
        ret, frame = cam.read()
        if not ret:
            break
        imgs.append(Image.fromarray(frame))

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    return imgs


def run():
    imgs = get_frame_images()

    inputs = []
    for img in imgs:
        input_tensor = preprocess(img)
        inputs.append(input_tensor)

    pre_model, model = module_loader.load_module()

    result = []
    split = 0
    with torch.no_grad():
        while split < len(inputs):
            batch = torch.stack(inputs[split:split + 32])
            if torch.cuda.is_available():
                batch = batch.cuda()
            output = pre_model(batch)
            output = model(output)
            _, predict = output.max(axis=-1)
            result.append(predict)
            split += 32

    return torch.cat(result).cpu().numpy()
