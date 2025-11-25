# Tezak Lab - Cell Counter

## Contributors:
alenachen2 - Alena Chen  
schalla1201 - Saakshi Challa  
acurielwes - Allegra Curiel  

## Style Guide 
https://github.com/alenachen2/COMP333-Tezak/blob/1e1ebc1eb064cbe47c49140c17cb7d6f46f0f8f3/StyleGuide.md

## User Instructions
1. Download Python version 3.11.x if it is not already downloaded by following the instructions from this link: https://www.python.org/downloads/. To check your Python version, type 'python --version' into the terminal. 
2. Clone our Github repository
   a. Open Terminal on your laptop and type: git clone https://github.com/alenachen2/COMP333-Tezak.git
   b. Change directory into our repository's folder by figuring out where the repository was downloaded and then typing: 'cd COMP333-Tezak'. 
3. Create a virtual environment for this project. 
   a. Type 'python3 -m venv cellpose_env' to create a virtual environment named cellpose_env. 
   b. To activate the virtual environment on macOS/Linux compute, type 'source cellpose_env/bin/activate'. If you are using Windows, type 'cellpose_env\Scripts\activate' 
4. Install required Python Packages
   a. In the terminal, type 'pip3 install opencv-python yaspin 'cellpose[gui] == 4.0.7' numpy matplotlib pytest'
5. Run our code by typing 'python main.py'. 
   a. When prompted to insert a file path, you may use your own cell image, or one of the cell images provided to us by the Tezak Lab. Since our code is tailored to work with specific cell images and still in the works, there is no guarantee of the cell count accuracy with other cell images. 
      i. To use our images, locate the images folder and find an image you would like to test, named x.jpg. The path would be 'images/x.jpg'.
      ii. To use your own image, find where the image is saved on your computer and insert the file's path. 
6. To run our test code, type: pytest
   a. If you are unfamilar with pytest, here is documentation explaining how it works: https://docs.pytest.org/en/stable/.
   
