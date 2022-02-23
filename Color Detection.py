# Color Detection
# This code allows you to choose a color from an image and to filter that image for that color.
    # Accepts an image as an input.
    # Outputs the RGB values and name of the color selected.
    # Outputs a black and white image with the color selected shown in white.

# Load the libraries.
import cv2
import numpy as np
import pandas as pd
from skimage import io

# Load the image twice, once to read from and once to filter.
image = "image1.jpg"
img = cv2.imread(image)
img_filter = io.imread(image)

# Initiate variables.
clicked = False
r = g =b = xpos = ypos = 0

# Load color name CSV
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv("colors.csv", names=index, header=None)

# Gets the name of a color.
    # Accepts the RGB values of a color as an input.
    # Outputs the name of the color that is its closeest match.
def get_color_name(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G-int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# Allows user to interact with the image and pull values from point clicked.
# Inputs the state of the mouse and keyboard.
# Selects the RGB values of the point clicked on the image.
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos,clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

# Display image in window.
def choose_color():
    # Create window and display image.
    cv2.namedWindow("choose color")
    cv2.setMouseCallback("choose color", draw_function)

    global b,g,r,xpos,ypos,clicked

    while(1):
        cv2.imshow("choose color",img)

        if (clicked):
            # Display color name and RGB values on window while user interacts with it.
            cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)
            text = get_color_name(r,g,b)+': R: '+str(r)+' G: '+ str(g)+' B: '+ str(b)
            cv2.putText(img, text,(50,50),2,0.8, (255,255,255),2,cv2.LINE_AA)
            if(r+g+b>=600):
                cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            clicked=False

        if cv2.waitKey(20) & 0xFF == 27:
            cv2.destroyAllWindows()
            break
    return

# Initiate the program and walk user through interface.
while(1):
    print("Choose the color you'd like to detect on the image. Click the esc key to continue.")
    choose_color()
    print(get_color_name(r,g,b)+': R: '+str(r)+' G: '+ str(g)+' B: '+ str(b))

    cont = input("Continue with current selection (Y/N): ")

    if cont == "Y":
        # Convert the color to the correct values and format.
        lower_range = np.array([r-50, g-50, b-25])
        upper_range = np.array([r+50, g+50, b+50])

        # Apply that range over the original image. Call the newly filtered image "mask".
        mask = cv2.inRange(img_filter, lower_range, upper_range)

        # Convert the original image back to a format we can display.
        img_filter = cv2.cvtColor(img_filter, cv2.COLOR_BGR2RGB)

        # Display the images, both original and filtered.
        cv2.imshow('filtered image', mask)
        cv2.imshow('original image', img_filter)
        cv2.waitKey(0)   #wait for a keyboard input
        cv2.destroyAllWindows()
        break