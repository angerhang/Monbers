import urllib.request
import csv
import qrcode
import webbrowser
import requests
import sys
import pandas as pd
from selenium import webdriver

# Member verification and download the images from google drive
def verifyMember(p_link):
    """
    :param p_link: the link of the student profile
    :return: true if the page is valid and contains student
    otherwise no
    """
    # without doctoral
    # more than 5 student or etudiant
    try:
        # req = urllib.request.Request(
        #     p_link,
        #     data=None,
        #     headers={
        #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        #     }
        # )
        #
        # f = urllib.request.urlopen(req)
        # web_page = f.read()

        browser = webdriver.Firefox()
        browser.get(p_link)
        web_page = browser.page_source

        # print (web_page)
        #f = urllib.request.urlopen(p_link)


        doctoral_c = 0
        student_c = 0
        etudiant_c = 0
        #
        # for word in web_page.split():
        #     if word not in wordcount:
        #         wordcount[word] = 1
        #     else:
        #         wordcount[word] += 1
        #
        # if 'doctoral' in wordcount:
        #     doctoral_c = wordcount['doctoral']
        # if 'student' in wordcount:
        #     student_c = wordcount['student']
        # if 'etudiant' in wordcount:
        #     etudiant_c = wordcount['etudiant_c']

        print(doctoral_c)
        print(student_c)
        print(etudiant_c)
        if '<a href="#">Student	</a>' in web_page:
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
    for index, row in df.iterrows():
        print(row['Email Address'])
        print(row['EPFL personal page link'])
        print(verifyMember(row['EPFL personal page link']))

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
