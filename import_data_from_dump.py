import sqlite3
import re
import os

def import_data_from_dump(dump_file_path, db_path):
    """
    Импортирует данные из PostgreSQL дампа в SQLite базу данных
    """
    # Подключаемся к базе данных
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Читаем дамп
    with open(dump_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Разбиваем на строки
    lines = content.split('\n')
    
    # Обрабатываем COPY секции
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('COPY'):
            # Извлекаем информацию о таблице и колонках
            copy_match = re.match(r'COPY public\.(\w+) \((.+)\) FROM stdin', line)
            if copy_match:
                table_name = copy_match.group(1)
                columns = [col.strip().strip('"') for col in copy_match.group(2).split(',')]
                
                # Читаем данные до '\\.'
                i += 1
                data_lines = []
                while i < len(lines) and lines[i].strip() != '\\.':
                    data_lines.append(lines[i])
                    i += 1
                
                # Подготавливаем SQL для вставки
                placeholders = ','.join(['?' for _ in columns])
                insert_sql = f"INSERT OR IGNORE INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
                
                # Вставляем данные
                for data_line in data_lines:
                    if data_line.strip() and data_line != '\\N':
                        # Разбираем значения, учитывая табы и экранирование
                        values = []
                        current_val = ""
                        i_pos = 0
                        while i_pos < len(data_line):
                            char = data_line[i_pos]
                            
                            # Проверяем, не является ли это началом экранированного символа
                            if char == '\\' and i_pos + 1 < len(data_line):
                                next_char = data_line[i_pos + 1]
                                if next_char == 't':
                                    current_val += '\t'
                                    i_pos += 2
                                    continue
                                elif next_char == 'n':
                                    current_val += '\n'
                                    i_pos += 2
                                    continue
                                elif next_char == 'r':
                                    current_val += '\r'
                                    i_pos += 2
                                    continue
                                elif next_char == '\\':
                                    current_val += '\\'
                                    i_pos += 2
                                    continue
                                else:
                                    # Это одиночный обратный слеш
                                    current_val += char
                                    i_pos += 1
                            elif char == '\t':
                                # Это разделитель полей
                                values.append(current_val if current_val != '\\N' else None)
                                current_val = ""
                                i_pos += 1
                            else:
                                current_val += char
                                i_pos += 1
                        
                        # Добавляем последнее значение
                        values.append(current_val if current_val != '\\N' else None)
                        
                        try:
                            cursor.execute(insert_sql, values)
                        except sqlite3.Error as e:
                            print(f"Ошибка при вставке в таблицу {table_name}: {e}")
                            print(f"Значения: {values}")
        
        i += 1
    
    # Сохраняем изменения
    conn.commit()
    conn.close()
    
    print("Импорт данных завершен")

if __name__ == "__main__":
    dump_file_path = r"C:\Users\Fablab\Downloads\iamthaichef.sql"
    db_path = r"C:\Users\Fablab\iamthaichef\db.sqlite3"
    
    if os.path.exists(dump_file_path):
        import_data_from_dump(dump_file_path, db_path)
    else:
        print(f"Файл дампа не найден: {dump_file_path}")