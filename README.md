# Image-Gen-AI-Generator

In today’s world, generative AI models like DALL·E 2 have become indispensable for creating high-quality, custom images from text prompts. Leveraging OpenAI’s API, you can seamlessly integrate this powerful model into your Python projects to generate images based on your ideas.

This article showcases a Python script that utilizes the OpenAI API to interact with the DALL·E 2 model. Moreover, the script includes a simple yet functional graphical user interface (GUI) built using Tkinter. This GUI allows you to input various parameters for the API call, making the process more intuitive and user-friendly.

## Key Features of the Script:

1. Prompt Input: Specify the text prompt to guide the image generation.
2. Image Size Selection: Choose from three supported sizes: 1024x1024, 512x512, or 256x256.
3. Number of Images: Generate between 1 and 10 images in a single API call.
4. Save Directory: Select the directory where the generated images will be saved.

With this setup, you can easily create a standalone application for generating and saving images, bypassing the need to work directly in the command line. This approach is perfect for those seeking a user-friendly solution to experiment with generative AI capabilities.

> [!IMPORTANT]
> Two modifications are required in the Python script for proper execution:

```python
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "paste_the_API_key_that_you_obtained_from_the_OpenAI_website"))
default_image_dir = "specify_the_directory_path_where_the_generated_images_will_be_stored"
```

## Graphical User Interface (GUI) of Python Application

You need to provide input to the program through the GUI as follows:

1. Prompt: Enter the text description that will be used to generate a relevant image.
2. Image Size: Choose from three supported sizes: 1024x1024, 512x512, or 256x256.
3. Number of Images: Select the number of images to generate, ranging from 1 to 10, in a single API call.
4. Choose Save Directory: Select the directory where you would like to save the generated images.
5. Generate Images: Click the button to begin generating the images


![App_Gui](https://github.com/EMazarakis/Image-Gen-AI-Generator/blob/main/Images/000.GUI_for_app.PNG)


## Make Python script executable
After you create your python script you can make it executable following the step-by-step guide. 
1. First, you need to install PyInstaller.
   > pip install pyinstaller
2. Then you have to run the following command in the cmd:
  > pyinstaller --noconsole --onefile  path_to_your_script_name.py
   noconsole: Suppresses the command prompt window.
   onefile: Packages everything into a single executable file.
