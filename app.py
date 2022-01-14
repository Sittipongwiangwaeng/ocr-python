from flask import Flask, render_template, request, jsonify
import cv2
import pytesseract
from pytesseract import Output

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/readcard", methods=["POST"])
def readcard():

    raw_file = request.get_json().raw_file
    print('raw_file, ' , raw_file)
    
    corpus = []
    str = ""
    strData = str
    idCard = str
    nameTh = str
    lastnameTh = str
    nameEng = str
    lastnameEng = str
    dateOfBirth = str
    dateOfBirthTh = str
    religion = str
    address = str
    custom_config = r'-l tha+eng --oem 3 --psm 6 -c language_model_ngram_space_delimited_language=1'
    img = cv2.imread(raw_file)

    gray = get_grayscale(img)
    thresh = thresholding(gray)
    img = thresh
    text = pytesseract.image_to_string(img, config=custom_config)
    strData = text
    data = pytesseract.image_to_data(img, config=custom_config, output_type=Output.DICT)
    keys = list(data.keys())

    totalBox = len(data['text'])
    for i in range(totalBox):
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    str = ''.join(data['text'])

    list(corpus)
    strData = clean(strData)
    findBD = strData.find("เกิดวันที่")
    findReligion = strData.find("ศาสนา")
    findAddress = strData.find("ที่อยู่")
    findID = strData.find("Identification Number")
    findIDv2 = strData.find("เลขประจําตัวประชาชน")
    findIDv3 = strData.find("เลขประจ่าตัวประชาชน")
    if findID != -1:
        thisFindID = findID
        checkID = 0
        for x in range(thisFindID+22, thisFindID+39):
            if checkID >= 2:
                break
            if strData[x].isspace() == True:
                checkID = checkID+1
            else:
                checkID = 0
                idCard = idCard + strData[x]
    elif findIDv2 != -1:
        thisFindID = findIDv2
        checkID = 0
        for x in range(thisFindID+20, thisFindID+39):
            if checkID >= 2:
                break
            if strData[x].isspace() == True:
                checkID = checkID+1
            else:
                checkID = 0
                idCard = idCard + strData[x]
    elif findIDv3 != -1:
        thisFindID = findIDv3
        checkID = 0
        for x in range(thisFindID+20, thisFindID+39):
            if checkID >= 2:
                break
            if strData[x].isspace() == True:
                checkID = checkID+1
            else:
                checkID = 0
                idCard = idCard + strData[x]

    findNameTh = strData.find("ชื่อตัวและชื่อสกุล")
    findNameThv2 = strData.find("ชื่อตัวและชื่อสกล")
    if findNameTh != -1:
        thisFindNameTh = findNameTh
        checkNameTh = 0
        keepName = 0
        for x in range(thisFindNameTh+19, thisFindNameTh+60):
            if checkNameTh >= 2:
                break
            if strData[x].isspace() == True:
                checkNameTh = checkNameTh+1
                keepName += 1
            else:
                checkNameTh = 0
            if keepName == 1:
                nameTh = nameTh + strData[x]
            elif keepName == 2:
                lastnameTh = lastnameTh + strData[x]

    elif findNameThv2 != -1:
        thisFindNameTh = findNameThv2
        checkNameTh = 0
        keepName = 0
        for x in range(thisFindNameTh+19, thisFindNameTh+60):
            if checkNameTh >= 2:
                break
            if strData[x].isspace() == True:
                checkNameTh = checkNameTh+1
                keepName += 1
            else:
                checkNameTh = 0
            if keepName == 1:
                nameTh = nameTh + strData[x]
            elif keepName == 2:
                lastnameTh = lastnameTh + strData[x]

    findNameEng = strData.find("Name")
    findNameEngv2 = strData.find("Nem")
    if findNameEng != -1:
        thisFindNameEng = findNameEng
        checkNameEng = 0
        for x in range(thisFindNameEng+4, thisFindNameEng+25):
            if checkNameEng >= 3:
                break
            if strData[x].isspace() == True:
                checkNameEng = checkNameEng+1
            else:
                checkNameEng = 0
                nameEng = nameEng + strData[x]
    elif findNameEngv2 != -1:
        thisFindNameEng = findNameEngv2
        checkNameEng = 0
        for x in range(thisFindNameEng+3, thisFindNameEng+25):
            if checkNameEng >= 3:
                break
            if strData[x].isspace() == True:
                checkNameEng = checkNameEng+1
            else:
                checkNameEng = 0
                nameEng = nameEng + strData[x]

    findLastname = strData.find("Lastname")
    findLastnamev2 = strData.find("Last name")
    findLastnamev3 = strData.find("lastname")
    if findLastname != -1:
        thisFindLastname = findLastname
        checkLastnameEng = 0
        for x in range(thisFindLastname+8, thisFindLastname+25):
            if checkLastnameEng >= 2:
                break
            if strData[x].isalpha() == False:
                checkLastnameEng = checkLastnameEng+1
            else:
                checkLastnameEng = 0
                lastnameEng = lastnameEng + strData[x]
    elif findLastnamev2 != -1:
        thisFindLastname = findLastnamev2
        checkLastnameEng = 0
        for x in range(thisFindLastname+9, thisFindLastname+26):
            if checkLastnameEng >= 2:
                break
            if strData[x].isalpha() == False:
                checkLastnameEng = checkLastnameEng+1
            else:
                checkLastnameEng = 0
                lastnameEng = lastnameEng + strData[x]
    elif findLastnamev3 != -1:
        thisFindLastname = findLastnamev3
        checkLastnameEng = 0
        for x in range(thisFindLastname+8, thisFindLastname+25):
            if checkLastnameEng >= 2:
                break
            if strData[x].isalpha() == False:
                checkLastnameEng = checkLastnameEng+1
            else:
                checkLastnameEng = 0
                lastnameEng = lastnameEng + strData[x]

    findDoB = strData.find("Date of Birth")
    findDoBv2 = strData.find("Dets of Birth")
    findDoBv3 = strData.find("Date of Buth")
    if findDoB != -1:
        thisFindDoB = findDoB
        checkDoB = 0
        for x in range(thisFindDoB+14, thisFindDoB+27):
            # if checkDoB >= 2:
            #     break
            # if strData[x].isspace() == True:
            #     checkDoB = checkDoB+1
            # else:
            #     checkDoB = 0
            dateOfBirth = dateOfBirth + strData[x]

    elif findDoBv2 != -1:
        thisFindDoB = findDoBv2
        checkDoB = 0
        for x in range(thisFindDoB+14, thisFindDoB+27):
            dateOfBirth = dateOfBirth + strData[x]
    elif findDoBv3 != -1:
        thisFindDoB = findDoBv3
        checkDoB = 0
        for x in range(thisFindDoB+13, thisFindDoB+27):
            dateOfBirth = dateOfBirth + strData[x]

    checkDoBth = 0
    for x in range(findBD+10, findBD+30):
        if checkDoBth >= 2:
            break
        if strData[x].isspace() == True:
            checkDoBth = checkDoBth+1
        else:
            checkDoBth = 0
            dateOfBirthTh = dateOfBirthTh + strData[x]

    checkReligion = 0
    for x in range(findReligion+5, findReligion+30):
        if strData[x].isspace() == True:
            checkReligion = checkReligion+1
        else:
            checkReligion = 0
            religion = religion + strData[x]

    response = {
        "idcard": "idCard",
        "nameth": "nameTh",
        "lastnameth": "lastnameTh",
        "nameeng": "nameEng",
        "lastnameeng": "lastnameEng",
        "dateofbirth": "dateOfBirth"
    }
    return jsonify(response)

    # print("ID Card:", idCard)
    # print("ชื่อตัว:", nameTh)
    # print("ชื่อสกุล:", lastnameTh)
    # print("เกิดวันที่:", dateOfBirthTh)
    # print("Name:", nameEng)
    # print("Last name:", lastnameEng)
    # print("Date Of Birth:", dateOfBirth)


def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def clean(text):
        cleanText = ""
        cleanText = text.translate({ord(c): None for c in "_—?!=+-()[]*&%#|«»:;'‘“,"})
        return cleanText


def is_ascii(s):
        return all(ord(c) < 128 for c in s)