import urllib.request
import csv
import qrcode
import webbrowser
import requests
import sys
import pandas as pd

# Member verification and download the images from google drive
def verifyMember(p_link):
    """
    :param p_link: the link of the student profile
    :return: true if the page is valid and contains student
    otherwise no
    """
    try:
        f = urllib.request.urlopen(p_link)
        web_page = f.read()

        if b'student' in web_page:
            return True
        else:
            return False
    except:
        print ("http request failed. Member is not verified")
    return False

def generateQR(link):
    # Create qr code instance
    # QR code links to the generated link for each member
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    # Add data
    qr.add_data(link)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image()
    img.show()
    img.save("image.jpg")



confirmations = []

# download the profile imgs and
# name them in a specific format

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

# if __name__ == "__main__":
#     var = raw_input("Please enter public file id : ")
#     file_id = str(var)
#     name = raw_input("Please enter name with extension : ")
#     destination = str(name)
#     download_file_from_google_drive(file_id, destination)

#file_id = '1ZdR3L3qP4Bkq8noWLJHSr_iBau0DNT4Kli4SxNc2YEo'
#destination = 'test.png'
#download_file_from_google_drive(file_id, destination)



# generateQR('han')


def process_info(info_path, photo_path):
    # f = open(info_path)
    # csv_f = csv.reader(f)
    #
    # status_id = 1
    # member_page_id = 4
    # conStatus_id = 6
    # for row in csv_f:
    #     # column 1 as the member status
    #     row[1] = verifyMember(row[4])
    #     # colum 5 as the profile url
    #
    #     # column 6 is the generated
    #     print(row)
    df = pd.read_csv(info_path)
    print(df[['Email Address', 'Status']])
    # saved_column = df.column_name
    # print(saved_column)

# specify the excel to process and the member photo path
# 1. verify if the member status is valid
# 2. download the member photo to photo_path
# 3. store the QR code
if __name__ == "__main__":
    info_path = sys.argv[1]
    photo_path = sys.argv[2]
    process_info(info_path, photo_path)
