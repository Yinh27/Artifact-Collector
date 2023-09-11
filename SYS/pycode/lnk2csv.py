import os
import csv
import pylnk3
import argparse

def parse_lnk(lnk_path):
    lnk = pylnk3.Lnk(lnk_path)
    target_size = get_actual_file_size(lnk.path)
    
    data = {
        "Lnk Filename": os.path.basename(lnk_path),
        "Creation Time": lnk.creation_time.strftime('%Y-%m-%d %H:%M:%S'),
        "Modification Time": lnk.modification_time.strftime('%Y-%m-%d %H:%M:%S'),
        "Access Time": lnk.access_time.strftime('%Y-%m-%d %H:%M:%S'),
        "File Size": str(target_size),
        "Commandline Arguments": lnk.arguments,
        "Working_directory": lnk.working_dir,
        "Used Path": lnk.path
    }
    return data

def get_actual_file_size(target_path):
    try:
        return os.path.getsize(target_path)
    except:
        return 0

def save_to_csv(data, csv_filename):
    fieldnames = [
        "Lnk Filename",
        "Creation Time", 
        "Modification Time", 
        "Access Time", 
        "File Size",
        "Commandline Arguments",
        "Working_directory",
        "Used Path"
    ]
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            for field in fieldnames:
                entry.setdefault(field, "")
            writer.writerow(entry)

def recursive_search(folder_path):
    data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.lnk'):
                full_path = os.path.join(root, file)
                info = parse_lnk(full_path)
                data.append(info)
    return data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process .lnk files and save information to a CSV file.")
    parser.add_argument("-f", "--folder_path", required=True, type=str, help="The folder path containing the .lnk files.")
    parser.add_argument("-o", "--csv_filename", required=True, type=str, help="The destination CSV filename to save parsed information.")
    
    args = parser.parse_args()

    data = recursive_search(args.folder_path)
    save_to_csv(data, args.csv_filename)
