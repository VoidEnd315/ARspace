import cv2
import tkinter as tk
from tkinter import *
from ultralytics import YOLO
from PIL import Image, ImageTk
import os
import pyttsx3
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from torch.utils.data import Dataset, DataLoader
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import threading

# Load fine-tuned model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("fine_tuned_gpt_model")
model = GPT2LMHeadModel.from_pretrained("fine_tuned_gpt_model")

# Set the model in evaluation mode
model.eval()

root = tk.Tk()

path1="download.jpg"
bg_image = ImageTk.PhotoImage(file=path1)
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
last_clicked_button = None
def turnOnTV(image_path, prompt_text):
    global last_clicked_button  # Declare the variable as global
    last_clicked_button = {"image_path": image_path, "prompt_text": prompt_text} 
    tv_frame = tk.Frame(root, width=400, height=400)
    tv_frame.place(relx=0.52, rely=0.1, anchor='nw')

    image = Image.open(image_path)
    resize_image = image.resize((300, 300))
    img = ImageTk.PhotoImage(resize_image)

    label1 = Label(tv_frame, image=img)
    label1.image = img
    label1.pack()

    input_ids = tokenizer.encode(prompt_text, return_tensors="pt")
    output = model.generate(
        input_ids,
        max_length=50,
        num_return_sequences=1,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        do_sample=True,
        max_new_tokens=30
    )

    for i, sample_output in enumerate(output):
        decoded_output = tokenizer.decode(sample_output, skip_special_tokens=True)
        sentences = decoded_output.split('.')
        if len(sentences) > 1:
            first_sentence = sentences[0] + '.'
            second_sentence = sentences[1] + '.'
            sentence = first_sentence + second_sentence

            text = Text(tv_frame, width=70, height=10)
            text.insert(INSERT, sentence)
            text.pack()

            engine = pyttsx3.init()
            engine.say(sentence)
            threading.Thread(target=engine.runAndWait).start()
def reloadLastButton():
    if last_clicked_button:
        turnOnTV(last_clicked_button["image_path"], last_clicked_button["prompt_text"])
b1 = Button(root, text="ear", command=lambda: turnOnTV("ears.jpg", "The human ear is a"))
b2 = Button(root, text="face", command=lambda: turnOnTV("face.jpg", "The human face is a"))
b3 = Button(root, text="eyes", command=lambda: turnOnTV("eyes.jpg", "The human eyes is a"))
reload_button = Button(root, text="More Facts", command=reloadLastButton)
class YOLODetector:
    def __init__(self, master):
        self.master = master
        master.title("YOLOv8s Object Detection")

        # Create a label to display the video stream
        self.video_label = tk.Label(master)
        self.video_label.pack(side="top",anchor="w", padx=0, pady=0)

        # Load the YOLOv8s model
        self.model = YOLO('best.pt')

        # Start the video capture
        self.cap = cv2.VideoCapture(0)

        # Initialize the set of detected classes
        self.detected_classes_set = set()

        self.detect_objects()

    def detect_objects(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Run the YOLOv8s model on the frame
        results = self.model(frame)[0]

        # Draw bounding boxes and add the detected classes to the set
        for result in results.boxes:
            x1, y1, x2, y2 = result.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            class_id = int(result.cls[0])
            class_name = self.model.names[class_id]

            # Draw the bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Draw the class name on top of the bounding box
            text_size = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
            text_x = x1
            text_y = max(y1 - text_size[1] - 5, 0)
            cv2.putText(frame, class_name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

            # Add the detected class to the set
            self.detected_classes_set.add(class_name)

        reload_button.pack(side=tk.LEFT, padx=40, pady=20)
        if "ear" in self.detected_classes_set:
            b1.pack(side=tk.LEFT, padx=40, pady=20)
        else:
            b1.pack_forget()
        if "eye" in self.detected_classes_set:
            b2.pack(side=tk.LEFT, padx=40, pady=20)
        else:
            b2.pack_forget()
        if "face" in self.detected_classes_set:
            b3.pack(side=tk.LEFT, padx=40, pady=20)
        else:
            b3.pack_forget()

        # Display the frame in the video label
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(img)
        self.video_label.configure(image=photo)
        self.video_label.image = photo

        # Schedule the next detection
        self.master.after(10, self.detect_objects)
root.geometry("1300x600")
detector = YOLODetector(root)
root.mainloop()
