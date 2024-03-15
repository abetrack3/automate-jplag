import os
import re
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from app.unzip_files import extract_zip_file


def __extract_student_id_from_file_name(file_name: str) -> Optional[str]:

    pattern: str = r'(\d{4,8})'

    matches = re.findall(pattern, file_name)

    if matches:

        return matches[0]

    else:

        return None


def generate_excel_report() -> None:

    # Extract result zip file
    extract_zip_file('./result.zip', 'result')

    _, _, json_file_names = next(os.walk('result'))

    file_comparisons: List[Tuple[str, str]] = list(map(lambda file_name: file_name.removesuffix('.py.json').split('.py-'), json_file_names))

    result_set: List[Tuple[str, str, float]] = []

    for each_comparison in file_comparisons:

        if each_comparison[0] == 'overview.json':

            continue

        first_student_id: str = __extract_student_id_from_file_name(each_comparison[0])

        second_student_id: str = __extract_student_id_from_file_name(each_comparison[1])

        file_name: str = '-'.join(list(map(lambda x: f'{x}.py', each_comparison))) + '.json'

        with open(f'./result/{file_name}', 'r', encoding='utf-8') as json_file_object:

            json_data = json.load(json_file_object)

            similarity: float = float(json_data['similarity'])

            if first_student_id != second_student_id:

                result_set.append((first_student_id, second_student_id, similarity))
        
    source_student_ids, target_student_ids, similarities = zip(*result_set)

    data_frame = pd.DataFrame({
        'Source': source_student_ids,
        'Target': target_student_ids,
        'Similarity Percentage': similarities,
    })

    data_frame.to_excel('result.xlsx', index=False)

