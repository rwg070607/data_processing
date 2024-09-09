import json
import re
import os
import pandas as pd
import numpy as np

folder_path = r'C:\Users\USER\Desktop\json'
result_path = r"C:\Users\user\Desktop\json\result.json"

def preprocessing(file_path):

    with open(file_path, mode='r+', encoding = 'UTF-8') as i: # json 파일 디렉토리로 변환
        data = json.load(i)

        def remove_prth(text):
            pattern = r"\(([^)]+)\)/"
            new_sentence = re.sub(pattern, lambda x: x.group(1), text)
            new_sentence = re.sub(r"\([^)]*\)", "", new_sentence)

            return new_sentence.strip()

        def remove_brace(text):

            return re.sub(r'\{[^{}]*\}', '', text).strip()

        def modify_json_prth(data):

            if isinstance(data, str):
                return remove_prth(data)

            elif isinstance(data, dict):
                return {k: modify_json_prth(v) for k, v in data.items()}

            elif isinstance(data, list):
                return [modify_json_prth(item) for item in data]

            return data

        def modify_json_brace(data):

            if isinstance(data, str):
                return remove_brace(data)

            elif isinstance(data, dict):
                return {k: modify_json_brace(v) for k, v in data.items()}

            elif isinstance(data, list):
                return [modify_json_brace(item) for item in data]

            return data

        modified_data = modify_json_prth(data)
        modified_data = modify_json_brace(modified_data)

        i.seek(0)
        i.truncate()
        json.dump(modified_data, i, ensure_ascii=False, indent=4)

def json_to_dataframe(file_path):
    with open(file_path, mode='r+', encoding='UTF-8') as i:
        js = json.load(i)

    df = pd.json_normalize(js['utterance'], sep='_')

    df = df.fillna(value='')

    print(df)


def json_folder(folder_path):

    for i in os.listdir(folder_path):
        if i.endswith('.json'):
            file_path = os.path.join(folder_path, i)
            preprocessing(file_path)
            json_to_dataframe(file_path)

json_folder(folder_path)

# def mkdir():
#     with open(result_path, mode = 'r+', encoding='UTF-8') as i:
