# Import libraries
from PIL import Image
from pdf2image import convert_from_path
import os
import random




def covert_pdffile_to_image(pdf_name, start, end, pdffullpath):
# def covert_pdffile_to_image(pdf_name, start, end):
    randomnumber = random.randint(1,1000)

    # Path of the pdf
    PDF_file = pdf_name
    imagepath = pdffullpath + 'image\\'
    os.mkdir(imagepath)

    '''
    Part #1 : Converting PDF to images
    '''

  
    # Store all the pages of the PDF in a variable
    pages = convert_from_path(PDF_file, 500, first_page=start, last_page=end)

    # Counter to store images of each page of PDF to image
    image_counter = 1

    imagespath = []

    # Iterate through all the pages stored above
    for page in pages:

        # Declaring filename for each page of PDF as JPG
        # For each page, filename will be:
        # PDF page 1 -> page_1.jpg
        # PDF page 2 -> page_2.jpg
        # PDF page 3 -> page_3.jpg
        
        filename = "page_"+str(image_counter)+".jpg"
       
        imagespath.append(str(filename))

        # Save the image of the page in system
        page.save(imagepath + filename, 'JPEG')

        image_counter = image_counter + 1




    return imagespath