import cv2
import pandas as pd

# Load colors CSV
csv_path = 'colors.csv'
colors = pd.read_csv(csv_path)

# Function to get color name
def get_color_name(R, G, B):
    minimum = 10000
    cname = ""
    for i in range(len(colors)):
        d = abs(R - int(colors.loc[i, "R"])) + abs(G - int(colors.loc[i, "G"])) + abs(B - int(colors.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = colors.loc[i, "color_name"]
    return cname

# Mouse click event
clicked = False
r = g = b = xpos = ypos = 0

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

# Load image
img = cv2.imread('sample_image.jpg')
img = cv2.resize(img, (800, 600))
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', draw_function)

while True:
    cv2.imshow("Image", img)
    if clicked:
        # Create color rectangle
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = f"{get_color_name(r, g, b)}  (R={r}, G={g}, B={b})"
        # Set text color (white/black based on brightness)
        text_color = (255, 255, 255) if r+g+b < 400 else (0, 0, 0)
        cv2.putText(img, text, (50, 50), 2, 0.8, text_color, 2, cv2.LINE_AA)
        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:  # press ESC to exit
        break

cv2.destroyAllWindows()
