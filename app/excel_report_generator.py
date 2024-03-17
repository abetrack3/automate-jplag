import os
import re
import json
import pandas as pd
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Optional, Tuple
from app.unzip_files import extract_zip_file


EXCEL_FILE_NAME: str = 'result.xlsx'


def __extract_student_id_from_file_name(file_name: str) -> Optional[str]:

    pattern: str = r'(\d{4,8})'

    matches = re.findall(pattern, file_name)

    if matches:

        return matches[0]

    else:

        return None


def __custom_sort_key_function(element: Tuple[str, str, str, str, float,]) -> Tuple[str, float, str, str, str,]:

    return (
        element[0] if element[0] is not None else 'z',
        1.0 - (element[4] if element[4] is not None else 0.0),
        element[1] if element[1] is not None else 'z',
        element[2] if element[2] is not None else 'z',
        element[3] if element[3] is not None else 'z',
    )


def __wrap_cells(worksheet: Worksheet) -> None:

    for row in worksheet.iter_rows():

        for cell in row:

            cell.alignment = Alignment(wrap_text=True)


def __write_to_excel_file(data: pd.DataFrame) -> None:

    print('Generating report excel...')

    with pd.ExcelWriter(EXCEL_FILE_NAME) as writer:

        data.to_excel(writer, index=True)

        # adjusting the column widths based on column names
        worksheet: Worksheet = writer.sheets['Sheet1']

        for column_index, column_name in enumerate(data.columns, start=2):

            column_width: int = len(column_name)

            column_letter: str = get_column_letter(column_index)

            worksheet.column_dimensions[column_letter].width = column_width * 1.2

        # Freeze the first row
        worksheet.freeze_panes = 'A2'

        __wrap_cells(worksheet)

    print(F'Generated: "{EXCEL_FILE_NAME}"')


def generate_excel_report() -> None:

    # Extract result zip file
    extract_zip_file('./result.zip', 'result')

    _, _, json_file_names = next(os.walk('result'))

    file_comparisons: List[Tuple[str, str]] = list(map(lambda file_name: file_name.replace('.py.json', '').split('.py-'), json_file_names))

    result_set: List[Tuple[str, str, str, str, float]] = []

    for each_comparison in file_comparisons:

        if each_comparison[0] == 'overview.json':

            continue

        first_student_id: str = __extract_student_id_from_file_name(each_comparison[0])

        second_student_id: str = __extract_student_id_from_file_name(each_comparison[1])

        file_name: str = '-'.join(list(map(lambda x: f'{x}.py', each_comparison))) + '.json'

        with open(f'./result/{file_name}', 'r', encoding='utf-8') as json_file_object:

            json_data = json.load(json_file_object)

            similarity: float = float(json_data['similarity'])

            if similarity == 0.0:

                continue

            similarity_in_percentage: float = round(similarity * 100.0, 2)

            if first_student_id != second_student_id:

                result_set.append((first_student_id,
                                   second_student_id,
                                   each_comparison[0],
                                   each_comparison[1],
                                   similarity_in_percentage))

    result_set.sort(key = __custom_sort_key_function)

    source_student_ids, target_student_ids, source_student_file_name, target_student_file_name, similarities = zip(*result_set)

    data_frame = pd.DataFrame({
        'Student A ID': source_student_ids,
        'Student B ID': target_student_ids,
        'Similarity Percentage': similarities,
        'Student A File Name': source_student_file_name,
        'Student B File Name': target_student_file_name,
    })

    __write_to_excel_file(data_frame)


