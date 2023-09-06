import os
import datetime
import shutil

def get_current_dir():
    return os.getcwd()

def get_paths():
    current_dir = get_current_dir()
    source_folder = os.path.join(current_dir, 'home/valcann/backupsFrom')
    destination_folder = os.path.join(current_dir, 'home/valcann/backupsTo')
    main_folder = os.path.join(current_dir, 'home/valcann')
    return source_folder, destination_folder, main_folder

def get_file_info(file_path):
    file_data = os.stat(file_path)
    
    return {
        'name': os.path.basename(file_path),
        'file_size': os.path.getsize(file_path),
        'created_at': datetime.datetime.fromtimestamp(file_data.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.datetime.fromtimestamp(file_data.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
    }

def list_files_to_copy_and_delete(source_folder, time_offset):
    source_files = os.listdir(source_folder)

    files = [file for file in source_files if os.path.isfile(os.path.join(source_folder, file))]

    files_to_delete = []
    files_to_copy = []
    all_files = []

    for file in files:
        file_path = os.path.join(source_folder, file)
        file_data = os.stat(file_path)

        current_time = datetime.datetime.now().timestamp()

        if (current_time - file_data.st_ctime) > time_offset:
            files_to_delete.append(get_file_info(file_path))
        else:
            files_to_copy.append(get_file_info(file_path))
        
        all_files.append(get_file_info(file_path))

    return files_to_copy, files_to_delete, all_files

def format_log(log={}):
    formatted_log = (
        '#####' +
        '\n' + 'nome: ' + log['name'] +
        '\n' + 'tamanho: ' + str(log['file_size']) +
        '\n' + 'criado_em: ' + log['created_at'] +
        '\n' + 'modificado_em: ' + log['updated_at'] +
        '\n' + 'log_gerado_em: ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +
        '\n\n')

    return formatted_log

def create_log(path, file_name, log_data):
    log_file_path = os.path.join(path, file_name)

    if len(log_data) != 0:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as file:
                log_content = file.read()

            with open(log_file_path, 'w') as file:
                for info in log_data:
                    file.write(format_log(info))
                file.write(log_content)
        else:
            with open(log_file_path, 'w') as file:
                for info in log_data:
                    file.write(format_log(info))

def copy_files(source_folder, destination_folder, files_to_copy):
    for file in files_to_copy:
        file_name = file['name']

        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)

        try:
            shutil.copy(source_path, destination_path)
            print(f"Successfully copied {file_name} to {destination_folder}")
        except Exception as e:
            print(f"Error copying {file_name}: {str(e)}")

def delete_files(source_folder, files_to_delete):
    for file in files_to_delete:
        file_name = file['name']
        
        source_path = os.path.join(source_folder, file_name)

        if os.path.exists(source_path) and os.path.isfile(source_path):
            print(source_path)
            os.remove(source_path)

def main():
    source_folder, destination_folder, main_folder = get_paths()

    ## recomendation: set to 15 minutes (15 * 60) for testing with local files
    ## 3 days must be: 3 * 24 * 60 * 60
    time_offset = 3 * 24 * 60 * 60

    files_to_copy, files_to_delete, all_files = list_files_to_copy_and_delete(source_folder, time_offset)

    create_log(main_folder, 'backupsFrom.log', all_files)
    delete_files(source_folder, files_to_delete)

    try:
        copy_files(source_folder, destination_folder, files_to_copy)
        create_log(main_folder, 'backupsTo.log', files_to_copy)
    except Exception as e:
        print(f"Some error ocurred while coping files: {str(e)}")

if __name__ == "__main__":
    main()