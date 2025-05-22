 
import os
from tkinter import filedialog
import customtkinter as ctk
from PIL import ImageTk, Image
from predictions import predict

project_folder = os.path.dirname(os.path.abspath(__file__))
filename = ""

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Bone Fracture Detection")
        self.geometry("400x500")
        
        ctk.CTkLabel(self, text="Bone Fracture Detection", font=("Roboto", 24)).pack(pady=10)
        ctk.CTkLabel(self, text="Upload an X-Ray image to detect fractures.", wraplength=400).pack(pady=5)
        
        self.upload_btn = ctk.CTkButton(self, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=5)
        
        self.image_label = ctk.CTkLabel(self, text="No Image Uploaded")
        self.image_label.pack(pady=10)
        
        self.predict_btn = ctk.CTkButton(self, text="Predict", command=self.predict_gui)
        self.predict_btn.pack(pady=5)
        
        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)
        
    def upload_image(self):
        global filename
        filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filename:
            img = Image.open(filename)
            img_resized = img.resize((200, 200))
            img = ImageTk.PhotoImage(img_resized)
            self.image_label.configure(image=img, text="")
            self.image_label.image = img

    def predict_gui(self):
        if filename:
            bone_type_result = predict(filename)
            result = predict(filename, bone_type_result)
            color = "RED" if result == 'fractured' else "GREEN"
            self.result_label.configure(text=f"Result: {result.capitalize()}\nType: {bone_type_result}", text_color=color, font=("Roboto", 18))

if __name__ == "__main__":
    app = App()
    app.mainloop()
