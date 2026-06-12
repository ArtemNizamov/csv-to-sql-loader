import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text
from pathlib import Path

# Конфигурация подключения
DB_NAME = 'Olist'
CSV_FOLDER = 'C:\\Users\\Артём\\Downloads\\archive (3)'  # папка с CSV файлами


# Создаём connection string для SQLAlchemy
def get_engine():
    connection_string = (
        f'mssql+pyodbc://@.\\SQLEXPRESS/{DB_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    )
    return create_engine(connection_string)


# Проверка подключения
print("Проверка подключения к SQL Server...")
try:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Подключение успешно!")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    exit()


def create_table_if_not_exists(csv_path, table_name, engine):
    """Создаёт таблицу на основе структуры CSV, если её нет"""
    try:
        # Проверяем, существует ли таблица
        with engine.connect() as conn:
            result = conn.execute(text(f"""
                SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = '{table_name}'
            """))
            exists = result.scalar() > 0

        if not exists:
            # Читаем только заголовки CSV
            df_sample = pd.read_csv(csv_path, nrows=0)

            # Создаём таблицу с правильными типами
            # (временно все колонки как NVARCHAR, чтобы избежать ошибок)
            df_sample.to_sql(table_name, engine, if_exists='replace', index=False)

            # Очищаем временную таблицу (оставляем пустую структуру)
            with engine.connect() as conn:
                conn.execute(text(f"DELETE FROM [{table_name}]"))
                conn.commit()

            print(f"    📋 Создана таблица: {table_name}")
    except Exception as e:
        print(f"    ⚠️ Ошибка при создании таблицы {table_name}: {e}")


def load_csv_to_sql(csv_path, table_name, engine):
    try:
        print(f"  Загрузка {csv_path.name}...")

        # Читаем CSV
        df = pd.read_csv(csv_path)

        # Очищаем названия колонок
        df.columns = df.columns.str.replace(' ', '_').str.replace('[^a-zA-Z0-9_]', '')

        # Загружаем порциями для больших файлов
        df.to_sql(table_name, engine, if_exists='append', index=False, chunksize=1000)

        print(f"    ✅ {table_name}: {len(df)} строк")
        return True
    except Exception as e:
        print(f"    ❌ Ошибка: {e}")
        return False


# Основной процесс
csv_folder = Path(CSV_FOLDER)
if not csv_folder.exists():
    print(f"❌ Папка не найдена: {CSV_FOLDER}")
    exit()

csv_files = list(csv_folder.glob('*.csv'))
print(f"\nНайдено CSV файлов: {len(csv_files)}")
print("=" * 50)

engine = get_engine()
success_count = 0

for csv_file in csv_files:
    table_name = csv_file.stem

    # Создаём таблицу, если её нет
    create_table_if_not_exists(csv_file, table_name, engine)

    # Загружаем данные
    if load_csv_to_sql(csv_file, table_name, engine):
        success_count += 1

print("=" * 50)
print(f"Готово! Успешно загружено: {success_count} из {len(csv_files)}")