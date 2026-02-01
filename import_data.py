import sqlite3
import re

def import_data_to_sqlite():
    # Подключаемся к базе данных
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Открываем файл дампа
    with open(r'C:\Users\Fablab\Downloads\iamthaichef.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все секции COPY и извлекаем данные
    copy_sections = re.findall(r'COPY ([^ ]+) \((.+?)\) FROM stdin([\s\S]*?)\\\.', content)
    
    imported_count = 0
    
    for table_name, columns_str, data_section in copy_sections:
        table_name = table_name.replace('public.', '').strip('"')
        columns = [col.strip().strip('"') for col in columns_str.split(',')]
        
        # Разбиваем данные на строки
        data_lines = data_section.strip().split('\n')[1:]  # Пропускаем первую пустую строку
        
        for line in data_lines:
            if line.strip() == '' or line.strip() == '\\N':
                continue
                
            # Разбиваем строку по табуляции
            values = []
            current_val = ""
            i = 0
            while i < len(line):
                char = line[i]
                if char == '\\' and i + 1 < len(line) and line[i + 1] == '\\':
                    current_val += '\\'
                    i += 2
                    continue
                elif char == '\t':
                    values.append(current_val if current_val != '\\N' else None)
                    current_val = ""
                else:
                    current_val += char
                i += 1
            values.append(current_val if current_val != '\\N' else None)
            
            # Подготавливаем SQL-запрос
            placeholders = ', '.join(['?' for _ in values])
            columns_formatted = ', '.join(columns)
            sql = f"INSERT OR IGNORE INTO {table_name} ({columns_formatted}) VALUES ({placeholders})"
            
            try:
                cursor.execute(sql, values)
                imported_count += 1
            except sqlite3.Error as e:
                print(f"Ошибка при вставке в таблицу {table_name}: {e}")
                print(f"Значения: {values}")
    
    conn.commit()
    conn.close()
    
    print(f"Импортировано {imported_count} записей")

if __name__ == "__main__":
    import_data_to_sqlite()