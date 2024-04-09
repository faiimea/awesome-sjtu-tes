import os
import time
import shutil
import gradio as gr
from detect import detect
import pygmtools as pygm


# Define file address constant
FD_IMG_DEFAULT_PATH = "media/fake_detect_default.png"
FD_SOLUTION_PATH = "media/fake_detect_pie.png"
PRETRAINED_PATH = "fc_weights.pth"


def _handle_fd_solve(img_path: str):
    # Check file upload status
    if img_path is None:
        raise gr.Error("Please upload file completely!")
    
    # gzip
    os.system("gzip clip/bpe_simple_vocab_16e6.txt")
    
    # Begin solve and record the solving time
    start_time = time.time()
    detect(
        img_path=img_path,
        save_path=FD_SOLUTION_PATH,
        pretrained_path=PRETRAINED_PATH
    )
    solved_time = time.time() - start_time
    
    # Message
    message = "Successfully detect the image, using time ({:.3f}s).".format(solved_time)
    
    return message, FD_SOLUTION_PATH
    

def handle_fd_solve(img_path: str):
    try:
        message = _handle_fd_solve(img_path)
        return message
    except Exception as e:
        message = str(e)
        return message, FD_SOLUTION_PATH


def handle_ged_clear():
    # Replace the original image with the default image
    shutil.copy(
        src=FD_IMG_DEFAULT_PATH,
        dst=FD_SOLUTION_PATH
    )

    message = "successfully clear the files!"
    return message, FD_SOLUTION_PATH


with gr.Blocks() as ged_page:
    
    gr.Markdown(
        '''
        This space displays that how to detect the images generated by AI.
        ## How to use this Space?
        - Upload a '.png' or '.jpg' image.
        - The detection result will be shown after you click the detect button.
        - Click the 'clear' button to clear all the files.
        ## Examples
        - You can get the test examples from our [FakeDetect Dataset Repo.](https://huggingface.co/datasets/SJTU-TES/FakeDetect) 
        '''
    )

    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            with gr.Row():
                fd_img = gr.Image(
                    type="filepath"
                )
            info = gr.Textbox(
                value="",
                label="Log",
                scale=4,
            )
            with gr.Row():
                with gr.Column(scale=1, min_width=100):
                    solve_button = gr.Button(
                        value="Detect", 
                        variant="primary", 
                        scale=1
                    )
                with gr.Column(scale=1, min_width=100):
                    clear_button = gr.Button(
                        "Clear", 
                        variant="secondary", 
                        scale=1
                    )
                with gr.Column(scale=8):
                    pass    
        with gr.Row(variant="panel"):
            fd_solution = gr.Image(
                value=FD_SOLUTION_PATH, 
                type="filepath",
                label="Detection Result"
            )

     
    
    solve_button.click(
        handle_fd_solve,
        [fd_img],
        outputs=[info, fd_solution]
    )
    
    clear_button.click(
        handle_ged_clear,
        inputs=None,
        outputs=[info, fd_solution]
    )


if __name__ == "__main__":
    ged_page.launch(debug = True)