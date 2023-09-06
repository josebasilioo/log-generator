# # ## DELETE FILES
# # for file_name in files_to_delete:
# #     source_path= os.path.join(current_dir + '/home/valcann/backupsTo', file_name)

# #     if os.path.exists(source_path) and os.path.isfile(source_path):
# #         print(source_path)
# #         os.remove(source_path)
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
    infos = []

    for file in files:
        file_path = os.path.join(source_folder, file)
        file_data = os.stat(file_path)

        current_time = datetime.datetime.now().timestamp()

        if (current_time - file_data.st_ctime) > time_offset:
            files_to_delete.append(get_file_info(file_path))
        else:
            files_to_copy.append(get_file_info(file_path))
        
        infos.append(get_file_info(file_path))

    return files_to_copy, files_to_delete, infos

def format_log(log={}):
    formatted_log = (
        '#####' +
        '\n' + log['name'] +
        '\n' + str(log['file_size']) +
        '\n' + log['created_at'] +
        '\n' + log['updated_at'] +
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

def main():
    source_folder, destination_folder, main_folder = get_paths()
    time_offset = 3 * 24 * 60 * 60

    files_to_copy, files_to_delete, infos = list_files_to_copy_and_delete(source_folder, time_offset)

    create_log(main_folder, 'backupsFrom.log', infos)

    try:
        copy_files(source_folder, destination_folder, files_to_copy)
        create_log(main_folder, 'backupsTo.log', files_to_copy)
    except Exception as e:
        print(f"Some error ocurred while coping files: {str(e)}")

if __name__ == "__main__":
    main()