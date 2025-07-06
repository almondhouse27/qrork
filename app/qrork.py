from turtle import back
import qrcode
import qrcode.image.svg
from io import BytesIO

def generate(url, file_name, file_format, theme):

    """
    Generates a QR code image from the given URL with input data from the `templates/partials/input.html` component.

    Called:
        from the `app.py` file's index ('/') function when the form is submitted ['POST'].

    Args:
        url             (str):    The data or URL to encode in the QR code.
        file_name       (str):    The base name for the output file.
        file_format     (str):    The desired image file format.
        theme           (str):    The color theme to use for the QR code.

    Returns:
        success         (str):    The file name of the saved QR code image.
        otherwise       (None)

    Calls:
        assign_theme(theme):                     Determines the fill and background colors based on the selected theme.
        construct_image(url, fill, back):        Creates a QR code image with the specified URL and colors.
        construct_file(file_name, file_format):  Constructs the output file name with the appropriate extension.

    Notes:
        If an error occurs during QR code generation or saving, the function prints the error and returns None.
    """

    try:
        fill, back = assign_theme(theme)
        file, ext = construct_file(file_name, file_format)
        buf = BytesIO()

        if ext == "svg":
            factory = qrcode.image.svg.SvgImage
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=20,
                border=4,
                image_factory=factory,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image()
            img.save(buf)
        else:
            img = construct_image(url, fill, back)
            img.save(buf, format=ext.upper() if ext != "jpg" else "JPEG")


        buf.seek(0)
        return buf, file, ext
    
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return None, None, None



def assign_theme(theme):

    WHITE = "#FEFDFC"
    BLACK = "#010203"
    YELLOW = "#FFEB0F"
    RED = "#FF0F0F"
    BLUE = "#0404DB"
    GREEN = "#0FFFDB"


    if theme == "invert":
        fill = WHITE
        back = BLACK
    elif theme == "bee":
        fill = YELLOW
        back = BLACK
    elif theme == "qrork":
        fill = RED
        back = YELLOW
    elif theme == "aqua":
        fill = BLUE
        back = GREEN
    else:
        fill = BLACK
        back = WHITE

    return fill, back



def construct_image(url, fill, back):

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill, back_color=back)

    return img



def construct_file(file_name, file_format):

    ext = file_format.lower()

    if ext not in ["png", "bmp", "jpg", "gif", "svg"]:
        ext = "png"

    file = f"{file_name}.{ext}"

    return file, ext