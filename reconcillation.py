import chardet
import os


class Reconcilation:
    def __init__(self):
        self.Answer = []
        self.m_Answer = []
        self.m_m_Answer = [ ]
        self.error_code = "###ERROR: SET DISPENSE NOTES FAIL"
        self.error_codes = "###ERROR: DISPENSE FAILURE, STATUS:"
        self.withdrawal = "WITHDRAW         "
        self.failed_stans = [ ]
        self.first = [ ]
        self.double = [ ]

    def check_failed(self, filename):
        count = 0
        amount_sum = 0
        compiled = [ ]
        data = ""
        failed_stan = {}
        most_possibly_failed = {}
        more_most_possibly_failed = {}
        found_date = False
        while line := filename.readline():
            # terminal = ""
            # date = ""
            if not found_date and "TRANSACTION RECEIPT DATA" in line:
                terminal_date = filename.readline().strip().split("     ")[ 0:3:2 ]
                date = terminal_date[ 0 ].replace("\\", "-")
                terminal = terminal_date[1]
                found_date = True
            if self.withdrawal in line:
                amount_sum += int(line.split("NGN")[ 1 ].split(".")[ 0 ])
                count += 1
                wrong_stan = prev.split("    ")[0].split("   ")[ 1 ]
                data += terminal + "\t\t" + date + "\n" + wrong_stan + "\n" + "+" + prev + "+" + line

                while doc_1 := filename.readline():
                    data += doc_1
                    if "TRANSACTION SERIAL NUMBER" in doc_1:
                        compiled.append(data)
                        data = ""
                        found_date = False
                        break
            prev = line
        for failed in compiled:
            key = failed[ -5: ].strip()
            checker_key = failed.split("+")[ 1 ].strip().split("   ")[ 1 ]
            if "MONEY TAKEN=======" not in failed:
                if checker_key != key:
                    self.double.append(checker_key)
                    more_most_possibly_failed[ checker_key ] = failed
                    key = checker_key + "_0"
                failed_stan[ key ] = failed
            if "l_iSum" in failed:
                key = failed[ -5: ].strip()
                self.first.append(key)
                most_possibly_failed[ key ] = failed

        failed_stan = {int(failed[-5:].strip()): failed for failed in compiled if "MONEY TAKEN=======" not in failed }
        print(f"No of Failed / Withdrawals for File: {len(failed_stan)}: {len(more_most_possibly_failed)}/{count}"
              f" ==> {list(more_most_possibly_failed.keys())}  amount_sum : {'#{:,}'.format(amount_sum)}")
        self.Answer.append(failed_stan)
        self.m_Answer.append(most_possibly_failed)
        self.m_m_Answer.append(more_most_possibly_failed)

    def create_failed(self, dict_failed, file_name):
        collate = ""
        for files in dict_failed:
            collate += f"{[ f"{a}" for a in files ]} \n"
            for stan in files:
                self.failed_stans.append(stan)
                # collate += str(stan) + "\n"
                collate += files[ stan ]
                collate += "\n"
            collate += ("==================================================================================="
                        "===========================\n")
        with open(file_name, "wt", encoding="utf-8") as f:
            f.write(collate)

    def run_file(self, Cleaned_files):
        # Raw_files = [ raw_names for raw_names in os.listdir() if ".txt" in raw_names or ".log" in raw_names ]
        # print(Raw_files)
        # if input("Convert") != "":
        #     for raw_file in Raw_files:
        #         convert_to_utf_8(raw_file)
        #
        # os.chdir("updated")
        # Cleaned_files = [ raw_names for raw_names in os.listdir() if ".txt" in raw_names ]
        # print(Cleaned_files)
        self.check_failed(Cleaned_files)
        self.create_failed(self.Answer, "./found/Failed_stan.txt")
        self.create_failed(self.m_Answer, "./found/Most_Failed_stan.txt")
        self.create_failed(self.m_m_Answer, "./found/Output.txt")
        # print(self.failed_stans)
        print(self.double)

# Answer = []
# m_Answer = []
# m_m_Answer = []
# error_code = "###ERROR: SET DISPENSE NOTES FAIL"
# error_codes = "###ERROR: DISPENSE FAILURE, STATUS:"
# withdrawal = "WITHDRAW         "
# failed_stans = []
# first = []
# double = []


def convert_to_utf_8(filename):
    # with open(filename, 'rb') as f:
    #     content_bytes = f.read()
    content_bytes =filename
    detected = chardet.detect(content_bytes)
    # print(detected)
    encoding = detected['encoding']
    # print(encoding)
    content_text = content_bytes.decode(encoding)
    return content_text.replace("\n", "")


    # filenamee = filename.split(".")[0] + ".txt"
    # updated_file = open("./updated/"+filenamee, 'w', encoding="utf-8")
    # updated_file.write(content_text)
    # updated_file.close()
    # practice(filenamee)


def practice(filename):
    with (open("./updated/"+filename, "r", encoding="utf-8") as f):
        reader = f.read()
    with open("./updated/"+filename, "w", encoding="utf-8") as f:
        f.write(reader.replace("\n\n", "\n"))


# def check_failed(filename):
#     for name in filename:
#         count = 0
#         amount_sum = 0
#         compiled = []
#         data = ""
#         failed_stan = {}
#         most_possibly_failed = {}
#         more_most_possibly_failed = {}
#         with open(name, encoding="utf-8") as file:
#             found_date = False
#             while line := file.readline():
#                 if not found_date and "TRANSACTION RECEIPT DATA" in line:
#                     terminal_date = file.readline().strip().split("     ")[0:3:2]
#                     date = terminal_date[0].replace("\\", "-")
#                     terminal = terminal_date[1]
#                     found_date = True
#                 if withdrawal in line:
#                     amount_sum += int(line.split("NGN")[1].split(".")[0])
#                     count += 1
#                     wrong_stan = prev.split("    ")[0].split("   ")[1]
#                     data += terminal + "\t\t" + date + "\n" + wrong_stan + "\n" + "+" + prev + "+" + line
#
#                     while doc_1 := file.readline():
#                         data += doc_1
#                         if "TRANSACTION SERIAL NUMBER" in doc_1:
#                             compiled.append(data)
#                             data = ""
#                             found_date = False
#                             break
#                 prev = line
#         for failed in compiled:
#             key = failed[-5:].strip()
#             checker_key = failed.split("+")[1].strip().split("   ")[1]
#             if "MONEY TAKEN=======" not in failed:
#                 if checker_key != key:
#                     double.append(checker_key)
#                     more_most_possibly_failed[checker_key] = failed
#                     key = checker_key + "_0"
#                 failed_stan[key] = failed
#             if "l_iSum" in failed:
#                 key = failed[-5:].strip()
#                 first.append(key)
#                 most_possibly_failed[key] = failed
#
#         # failed_stan = {int(failed[-5:].strip()): failed for failed in compiled if "MONEY TAKEN=======" not in failed }
#         print(f"No of Failed / Withdrawals for {name}: {len(failed_stan)}: {len(more_most_possibly_failed)}/{count}"
#               f" ==> {more_most_possibly_failed.keys()}  amount_sum : {'#{:,}'.format(amount_sum)}")
#         Answer.append(failed_stan)
#         m_Answer.append(most_possibly_failed)
#         m_m_Answer.append(more_most_possibly_failed)


# def create_failed(dict_failed, file_name):
#     collate = ""
#     for files in dict_failed:
#         collate += f"{[f"{a}" for a in files]} \n"
#         for stan in files:
#             failed_stans.append(stan)
#             # collate += str(stan) + "\n"
#             collate += files[stan]
#             collate += "\n"
#         collate += ("==================================================================================="
#                     "===========================\n")
#     with open(file_name, "wt", encoding="utf-8") as f:
#         f.write(collate)


# def run_file():
#     Raw_files = [raw_names for raw_names in os.listdir() if ".txt" in raw_names or ".log" in raw_names]
#     print(Raw_files)
#     if input("Convert") != "":
#         for raw_file in Raw_files:
#             convert_to_utf_8(raw_file)
#
#     os.chdir("updated")
#     Cleaned_files = [raw_names for raw_names in os.listdir() if ".txt" in raw_names]
#     print(Cleaned_files)
#     check_failed(Cleaned_files)
#     create_failed(Answer, "./found/Failed_stan.txt")
#     create_failed(m_Answer, "./found/Most_Failed_stan.txt")
#     create_failed(m_m_Answer, "./found/Output.txt")
#     # print(failed_stans)
#     # print(double)

# Raw_files = [raw_names for raw_names in os.listdir() if ".txt" in raw_names or ".log" in raw_names]
# print(Raw_files)
# if input("Convert") != "":
#     for raw_file in Raw_files:
#         convert_to_utf_8(raw_file)
# os.chdir("updated")
# Cleaned_files = [raw_names for raw_names in os.listdir() if ".txt" in raw_names]
#
# print(Cleaned_files)
# check_failed(Cleaned_files)
# create_failed(Answer, "./found/Failed_stan.txt")
# create_failed(m_Answer, "./found/Most_Failed_stan.txt")
# create_failed(m_m_Answer, "./found/Output.txt")
# print(failed_stans)
# print(double)

# play = Reconcilation()
# play.run_file()
