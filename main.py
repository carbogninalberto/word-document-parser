import os
import json
import docx2txt

# GLOBAL SCRIPT VARS
output = "outputs"
keyword_list = []
json_entities_list = []
json_db_path = os.path.join(output, "database.json")

# Functions
def get_list_of_files(dirname='documents'):
    file_list = []

    if os.path.exists(os.path.join(dirname)):
        for root, dir, files in os.walk(dirname, topdown=False):
            for name in files:
                filepath = os.path.join(root, name)
                file_list.append(filepath)
    return file_list

# Classes
class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    file_list = get_list_of_files()

    # print list of files
    print("Found {} files.".format(len(file_list)))
    for file in file_list:
        print(file)

    # opening files
    for file in file_list:
        print("#######################################################################################################")
        print("Parsing file: '{}'.".format(file.split("/")[1]))
        print("#######################################################################################################")

        doc_name = file.split(".")[0].split("/")[1]

        img_store_path = os.path.join(output, file.split(".")[0].split("/")[1], 'images')
        raw_file_path = os.path.join(output, file.split(".")[0].split("/")[1], file.split(".")[0].split("/")[1]+'.txt')
        json_path = os.path.join(output, file.split(".")[0].split("/")[1], file.split(".")[0].split("/")[1] + '.json')

        print("{}{}1) Extracting and saving raw data from file.{}".format(Color.BOLD, Color.YELLOW, Color.END))
        print("\t- Checking if '{}' path exists.".format(img_store_path))
        if not os.path.exists(img_store_path):
            os.makedirs(img_store_path)

        # processing file and storing images in img_store_path
        file_to_process = docx2txt.process(file, img_store_path).replace("\n\n", "\n").replace("-\n", "-\n\n")

        # writing text to raw_file
        print("\t- Saving raw text to '{}'.".format(raw_file_path))
        raw_file = open(raw_file_path, 'w')
        raw_file.write(file_to_process)
        raw_file.close()

        # output parsed text
        #print(file_to_process)

        # elaborate parsed text
        print("{}{}2) Elaboration of raw data to extract required text.{}".format(Color.BOLD, Color.YELLOW, Color.END))
        description_list = []
        with open(raw_file_path, 'r+') as open_file:
            print("\t- file opened. Scanning for keywords...")
            for line in open_file:
                for keyword in keyword_list:
                    if keyword in line:
                        print("\t\t {}(!) found keyword: {}{}{}".format(Color.RED, Color.BLUE, keyword, Color.END,))
                        tmp_open_file = open_file
                        description_text = ""
                        for text_line in tmp_open_file:
                            if "APL26" in doc_name:
                                print(description_text)
                            if text_line == "\n":
                                break
                            description_text += text_line.replace("\n", " ")
                        description_list.append(description_text)
                        break
        print("\t- Converting extracted data to dictionary.")
        zip_of_doc = zip(keyword_list, description_list)
        dict_of_doc = dict(zip_of_doc)
        dict_of_doc = {doc_name: dict_of_doc}

        json_entities_list.append(dict_of_doc)

        print("\t- dump dictionary to a json.")
        with open(json_path, 'w') as json_file:
            json.dump(dict_of_doc, json_file, indent=4)

    print("\n{}{}Dumping all extracted data to {}.{}".format(Color.BOLD, Color.YELLOW, json_db_path, Color.END))
    json_db = {"database": json_entities_list}

    with open(json_db_path, 'w') as database:
        json.dump(json_db, database, indent=4)
