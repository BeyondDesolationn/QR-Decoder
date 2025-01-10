import tkinter
from PIL import ImageGrab, Image, ImageTk
import cv2
import numpy

# ------ QR code decoding function ------ #
def decode_QR(pil_image):
    opencv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR) # Converting to numpy array for cv2, and converting colors to BGR
    detector = cv2.QRCodeDetector()   # Creates a QR code detector object
    qr_text, bbox, _ = detector.detectAndDecode(opencv_image) # Use detector on image. (Detector return tuple with 3 indexes, therefore 3 variables)
    return qr_text if qr_text else None

# ------ Scaling image to appropriate size ------ #
def scale_image(pil_image, max_size): # pil_image is a PIL object, max_size is a tuple
    width, height = pil_image.size
    scale = min(max_size[0] / width, max_size[1] / height)
    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        return pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return pil_image

# ------ Grab the image and process it ------ #
def paste_image():
    image = ImageGrab.grabclipboard() # Capture image from clipboard (PIL IMAGE OBJECT)

    if image: # If there is an image
        image = image.convert("RGB") # Make sure coloring scheme is RGB
        scaled_image = scale_image(image, (300,300)) # Scale image to max 300x300, save it in a new variable
        image_tk = ImageTk.PhotoImage(scaled_image) # Convert image to ImageTk object

        # Display image in Label widget
        image_label.config(image=image_tk) # Assign Tkinter object to label
        image_label.image = image_tk # Keep a reference to prevent garbage collection

        # Decode the QR code
        qr_data = decode_QR(image) # Decode QR code from original image
        if qr_data:
            result_message.config(text=f"QR Code: {qr_data}")
        else:
            result_message.config(text="No QR code detected")


# Tkinter GUI window setup
window = tkinter.Tk()
window.title('QR Decode')

# Colors
bg_dark = '#2B2B2B'
fg_dark = '#FFFFFF'
button_bg = '#404040'
frame_bg = '#333333'

# Configure window
window.configure(bg=bg_dark)

# Main container
main_frame = tkinter.Frame(window, bg=frame_bg, padx=20, pady=20)
main_frame.pack(expand=True, fill='both', padx=15, pady=15)

# Buttons at the top
terminate_button = tkinter.Button(
    main_frame,
    text='Terminate',
    command=window.destroy,
    bg=button_bg,
    fg=fg_dark
)
terminate_button.pack(fill='x', pady=(0, 5))

paste_button = tkinter.Button(
    main_frame,
    text='Paste QR',
    command=paste_image,
    bg=button_bg,
    fg=fg_dark
)
paste_button.pack(fill='x', pady=(0, 20))

# Image display area
image_label = tkinter.Label(
    main_frame,
    bg=frame_bg,
    fg=fg_dark
)
image_label.pack(pady=10)

# Text display area
result_frame = tkinter.Frame(main_frame, bg=frame_bg)
result_frame.pack(fill='x', pady=10)

result_message = tkinter.Label(
    result_frame,
    text='QR code will appear here',
    bg=frame_bg,
    fg=fg_dark,
    font=('Segoe UI', 11),
    wraplength=350
)
result_message.pack(pady=10)

window.mainloop()