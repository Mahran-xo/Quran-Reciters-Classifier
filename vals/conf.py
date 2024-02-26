from tqdm import tqdm
import os

RECITERS = ['ابراهيم عبد المنعم ',
            'احمد الشلبي',
            'اسماعيل القاضي  ',
            'اوريانتو',
            'ايوب مصعب  ',
            'حسين عبد الضاهر  ',
            'خالد طوالبة  ',
            'زين ابو الكوثر  ',
            'طارق محمد  ',
            'علاء عقل  ',
            'علاء ياسر  ',
            'محمد حجازي  ',
            'مختار الحاج  ']


def rename_folders(base_path, string_to_strip):
    try:
        # Iterate over each folder in the base path
        for folder_name in os.listdir(base_path):
            folder_path = os.path.join(base_path, folder_name)

            # Check if it is a directory
            if os.path.isdir(folder_path):
                # Strip away the specified string from the folder name
                new_folder_name = folder_name.replace(string_to_strip, '')

                # Construct the new path
                new_folder_path = os.path.join(base_path, new_folder_name)

                # Rename the folder
                os.rename(folder_path, new_folder_path)
                gprint(f"Renamed: {folder_name} to {new_folder_name}")

    except Exception as e:
        rprint(f"An error occurred: {str(e)}")

def gprint(text):
    """
    green colored `print()`
    """
    print("\033[92m{}\033[0m".format(text))

def rprint(text):
    """
       red colored `print()`
    """
    print("\033[91m{}\033[0m".format(text))

def colored_tqdm(iterable, color_code, **kwargs):
    """
    colored `tqdm()` prog bar
    """
    return tqdm(iterable, bar_format=f"{color_code}{{bar}}{{r_bar}}\033[0m", **kwargs)


    #   "https://www.youtube.com/watch?v=0Zle6xIhOYY&t=774s",
    #   "https://www.youtube.com/watch?v=VZ-W8pLuCDU&t=863s",
    #   "https://www.youtube.com/watch?v=NvxafyffaRY&t=119s",
    #   "https://www.youtube.com/watch?v=ZLNC3ZFnX2E&t=424s",
    #   "https://www.youtube.com/watch?v=fyBCRqmO6gA&t=175s",
    #   "https://www.youtube.com/watch?v=3psUPFdSn7k&t=342s",
    #   "https://www.youtube.com/watch?v=7yBtIa7S6v0",
    #   "https://www.youtube.com/watch?v=9oqMrq0FR1Q",
    #   "https://www.youtube.com/watch?v=-FMWBZ7LN28"                   
    # above links for ismail al kady

        # "https://www.youtube.com/watch?v=XJwllTT2p0E",
        # "https://www.youtube.com/watch?v=Uy5ShxuJ8Es",
        # "https://www.youtube.com/watch?v=x-LLk5pjycs",
        # "https://www.youtube.com/watch?v=FMkwZICQIxU",
        # "https://www.youtube.com/watch?v=u-ezI4qKHb4",
        # "https://www.youtube.com/watch?v=NTtDIxPyWHM",
        # "https://www.youtube.com/watch?v=RygxXl4ufYc",
        # "https://www.youtube.com/watch?v=B0hioKeVco8",
        # "https://www.youtube.com/watch?v=5BnkgVJf5mU"
#ahmed el shalaby


    # "https://www.youtube.com/watch?v=Su87wxVD9u0",
    # "https://www.youtube.com/watch?v=Y5YOkrC2x8E",
    # "https://www.youtube.com/watch?v=pB-cGMFicBU&t=301s",
    # "https://www.youtube.com/watch?v=0dFMfvdPWWs",
    # "https://www.youtube.com/watch?v=hWd9xp8MKWM",
    # "https://www.youtube.com/watch?v=_VcMmy03cIk",
    # "https://www.youtube.com/watch?v=I5B6XQ0VNgk",
    # "https://www.youtube.com/watch?v=hT9M8gLhaZU",
#el menshwy

    # "https://www.youtube.com/watch?v=GuTiZBE6Ito",
    # "https://www.youtube.com/watch?v=Bp7HFU-RAaY",
    # "https://www.youtube.com/watch?v=YM_KX56_M3I",
    # "https://www.youtube.com/watch?v=RDgSSEvrZm4",
    # "https://www.youtube.com/watch?v=LCiSMPsZLEA",
    # "https://www.youtube.com/watch?v=Hh2dL3-O778",
    # "https://www.youtube.com/watch?v=kLMQ51H0r48",
#abd el baset

    # "https://www.youtube.com/watch?v=84gRTTfMQB4",
    # "https://www.youtube.com/watch?v=66jVdPDZXCY",
    # "https://www.youtube.com/watch?v=BHQEa0Uxz-0",
    # "https://www.youtube.com/watch?v=EoT7K2Uj-9g",
    # "https://www.youtube.com/watch?v=PslL8AkLW3c",
    # "https://www.youtube.com/watch?v=w02pq01df8U",
    # "https://www.youtube.com/watch?v=3H084daUwlA",
#Tarek mohamed

    # "https://www.youtube.com/watch?v=Th-KP48CFEI",
    # "https://www.youtube.com/watch?v=6-j84t2dtBU",
    # "https://www.youtube.com/watch?v=ea2ud0Pzxto",
    # "https://www.youtube.com/watch?v=iS4nkKYQ6BQ",
    # "https://www.youtube.com/watch?v=eNaOecVLIuI",
    # "https://www.youtube.com/watch?v=3rnSyz7iDdw",
    # "https://www.youtube.com/watch?v=vnE7bFCYPrI",
    # "https://www.youtube.com/watch?v=c7Wwn03QBro",
# alaa akl

