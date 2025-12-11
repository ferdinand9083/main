import os
import argparse
import re
import yaml

# Парсер для входных данных
def parse_input(text):
    number_pattern = r'[1-9][0-9]*'
    array_pattern = r'\[([^\]]+)\]'  # Считаем, что внутри массива могут быть значения, разделенные точкой с запятой
    name_pattern = r'[a-z][a-z0-9_]*'
    string_pattern = r'\'[^\']*\''

    lines = text.splitlines()
    config = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if '->' in line:
            key, value = line.split('->')
            key = key.strip()
            value = value.strip()

            if re.match(name_pattern, key):
                if re.match(number_pattern, value):
                    config[key] = int(value)
                elif re.match(string_pattern, value):
                    config[key] = value[1:-1]  # Убираем кавычки
                elif re.match(array_pattern, value):
                    values = [v.strip().strip("'") for v in value[1:-1].split(';')]
                    config[key] = values
                else:
                    raise ValueError(f"Invalid value for {key}: {value}")
            else:
                raise ValueError(f"Invalid name {key}")
        else:
            raise ValueError(f"Syntax error in line: {line}")
    
    return config

# Преобразование в YAML
def convert_to_yaml(config):
    return yaml.dump(config, default_flow_style=False, allow_unicode=True)

# Основная функция программы
def main():
    files = ['test_1.conf', 'test_2.conf', 'test_3.conf']
    output_dir = 'config_results'  # Папка, в которой будут сохранены файлы

    # Создаем папку для результатов, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for input_file in files:
        try:
            # Чтение входного текста
            with open(input_file, 'r') as file:
                input_text = file.read()

            # Парсим входной текст
            config = parse_input(input_text)

            # Преобразуем в YAML
            yaml_output = convert_to_yaml(config)

            # Формируем имя выходного файла, основанное на имени входного файла
            output_file = os.path.join(output_dir, f"{os.path.splitext(input_file)[0]}.yaml")

            # Записываем в файл
            with open(output_file, 'w') as file:
                file.write(f"# From {input_file}\n{yaml_output}")

            print(f"Configuration from {input_file} successfully written to {output_file}")

        except Exception as e:
            print(f"Error processing {input_file}: {e}")

if __name__ == "__main__":
    main()
