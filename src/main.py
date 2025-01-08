import tkinter
from PIL import ImageGrab, Image, ImageTk
import cv2
import numpy
def paste_image():
    image = ImageGrab.grabclipboard() # Capture image from clipboard (PIL IMAGE OBJECT)

    if image: # If there is an image
        # Make image an ImageTk object
        image = image.convert("RGB") # Make sure coloring scheme is RGB
        image_tk = ImageTk.PhotoImage(image) # Convert image to ImageTk object

        # Display image in Label widget
        image_label.config(image=image_tk)
        image_label.image = image_tk # Keep a reference to prevent garbage collection

        # Decode the QR code
        qr_data = decode_QR(image) # Decode QR code from original image
        if qr_data:
            result_message.config(text=f"QR Code: {qr_data}")
        else:
            result_message.config(text="No QR code detected")

def decode_QR(pil_image):
    opencv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)

    detector = cv2.QRCodeDetector()   # Creates a QR code detector object
    qr_text, bbox, _ = detector.detectAndDecode(opencv_image)
    if qr_text:
        return qr_text
    else:
        return None
    '''

    try:
        qr = qrcode.decode(pil_image)
        return qr.data.decode('utf-8')
    except qrcode.exceptions.Error as e:
        print(f"Error decoding QR code: {e}")
        return None
    '''



window = tkinter.Tk()
window.title('QR Decode')

# Buttons
terminate_button = tkinter.Button(window, text='Terminate', width=40, command=window.destroy)
capture_clipboard_button = tkinter.Button(window, text='Paste QR', width=40, command=paste_image)

image_label = tkinter.Label(window, pady=10)
result_message = tkinter.Message(window, text='QR code will appear here')
# instruction = tkinter.Message(window, width=1000, text='Paste your QR code photo')

terminate_button.pack()
capture_clipboard_button.pack()
image_label.pack()
result_message.pack()
# instruction.pack()
window.mainloop()


