import tkinter as tk
from tkinter import filedialog, messagebox
from openai import OpenAI, OpenAIError  # OpenAI Python library to make API calls
import requests                         # used to download images
import os                               # used to access filepaths
import datetime                         # used to name the filename of the image
from PIL import Image                   # used to print and edit images

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "paste_the_API_key_that_you_obtained_from_the_OpenAI_website"))

# Set a default directory to save DALL·E images
default_image_dir = "specify_the_directory_path_where_the_generated_images_will_be_stored"
os.makedirs(default_image_dir, exist_ok=True) #Ensures the directory exists; if not, it is created

# Type of saved image
suffix = '.png'
MODEL = "dall-e-2"  # Supported sizes for 256x256, 512x512, or 1024x1024

# Custom exception class for OpenAI image errors
class OpenAIImageError(Exception):
    pass


# Function to generate image using OpenAI API
def generate_image(prompt, num_images, size, format, m):
    
    # Parameters Explanation
    # prompt: Text description for the image.
    # num_images: Number of images to generate.
    # size: Size of the image (1024x1024, 512x512, or 256x256).
    # format: Response format (set to "url" for the API to return image URLs).
    # m: Model name (dall-e-2).
    
    try:
        generation_response = client.images.generate(
            model=m,
            prompt=prompt,
            n=num_images,
            size=size,
            response_format=format,
        )
        return generation_response  # Returns the response from the OpenAI API, which includes image URLs.
    except OpenAIError as e:
        raise OpenAIImageError("OpenAI API Error: " + str(e))
    except Exception as e:
        raise OpenAIImageError("An unexpected error occurred: " + str(e))


# Function to save image data to files
def save_image(res, size, prefix, suffix):
    
    # Parameters Explanation
    # res: Response object from the API containing image URLs.
    # size: Size of the image.
    # prefix: Directory path to save images.
    # suffix: File format extension (e.g., .png).

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    for i, image in enumerate(res.data):
        generated_image_name = f'image_{size}_{timestamp}_{i}{suffix}'  # Generate Unique Filename: Combines size, timestamp, and an index to name each image.
        generated_image_filepath = os.path.join(prefix, generated_image_name)
        generated_image_url = image.url
        generated_image = requests.get(generated_image_url).content     # Download Images: Fetches image data using the requests library.
        
        with open(generated_image_filepath, "wb") as image_file:
            image_file.write(generated_image)                           # Save Images: Writes the image content to a file on disk.
        print('Saved:', generated_image_filepath)

# GUI Application
class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DALL-E Image Generator")
        self.root.geometry("500x400")
        
        # Variables
        self.prompt_var = tk.StringVar()                # Stores the user’s image description.
        self.size_var = tk.StringVar(value="1024x1024") # Tracks the selected image size.
        self.num_images_var = tk.IntVar(value=1)        # Tracks the number of images to generate.
        self.save_dir = default_image_dir               # Holds the directory where images will be saved.
        
        # Layout: Adds a label and a text box for the user to input their prompt.
        tk.Label(root, text="Prompt:", font=("Arial", 12)).pack(pady=10)
        self.prompt_entry = tk.Entry(root, textvariable=self.prompt_var, width=50)
        self.prompt_entry.pack(pady=5)
        
        # Image Size Dropdown: Adds a dropdown menu for the user to select image size.
        tk.Label(root, text="Image Size:", font=("Arial", 12)).pack(pady=10)
        tk.OptionMenu(root, self.size_var, "1024x1024", "512x512", "256x256").pack(pady=5)
        
        # Number of Images: Adds a spinbox to select the number of images (between 1 and 10).
        tk.Label(root, text="Number of Images:", font=("Arial", 12)).pack(pady=10)
        tk.Spinbox(root, from_=1, to=10, textvariable=self.num_images_var, width=10).pack(pady=5)
        
        #Save Directory Button: Adds a button to open a file dialog for selecting the directory to save images.
        tk.Button(root, text="Choose Save Directory", command=self.choose_save_directory).pack(pady=10)
        
        # Generate Images Button: Adds a button to trigger image generation.
        tk.Button(root, text="Generate Images", command=self.generate_images).pack(pady=10)
    
    # Choose Save Directory: Opens a dialog for the user to select a directory.
    def choose_save_directory(self):
        directory = filedialog.askdirectory(initialdir=default_image_dir, title="Select Save Directory")
        if directory:
            self.save_dir = directory
    
    #Generate Images: Fetches user input from the GUI (prompt, size, num_images).
    def generate_images(self):
        prompt = self.prompt_var.get()
        size = self.size_var.get()
        num_images = self.num_images_var.get()
        
        # Validates the prompt.
        if not prompt:
            messagebox.showerror("Error", "Prompt cannot be empty!")
            return
        
        try:
            response = generate_image(prompt, num_images, size, "url", MODEL)   #Calls generate_image to create images and save_image to save them.
            save_image(response, size, self.save_dir, suffix)
            messagebox.showinfo("Success", f"Images saved to {self.save_dir}")  # Displays success or error messages using messagebox.
        except OpenAIImageError as e:
            messagebox.showerror("Error", str(e))

# Main Function
def main():
    root = tk.Tk()                  # Initializes the Tkinter root window.
    app = ImageGeneratorApp(root)   # Instantiates the ImageGeneratorApp to populate the window with GUI components.
    root.mainloop()                 # Starts the Tkinter event loop to keep the window responsive. 
    
# Entry point of the script
if __name__ == "__main__":
    main()
