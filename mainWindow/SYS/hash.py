import os
import hashlib
import argparse

def calculate_hashes(file_path):
    # 각 해시 알고리즘에 대한 객체 초기화
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    return md5.hexdigest(), sha1.hexdigest(), sha256.hexdigest()

def list_files(startpath, exclude_path=None):
    output = []
    for root, dirs, files in os.walk(startpath):
        # 생성되는 output 파일은 hash.txt에 저장하지 않음
        if root == os.path.dirname(exclude_path):
            if os.path.basename(exclude_path) in files:
                files.remove(os.path.basename(exclude_path))
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output.append('{}Directory: {}'.format(indent, root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_path = os.path.join(root, f)
            md5_hash, sha1_hash, sha256_hash = calculate_hashes(file_path)
            output.append('{}File: {} - MD5: {}, SHA-1: {}, SHA-256: {}'.format(subindent, file_path, md5_hash, sha1_hash, sha256_hash))
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculate MD5, SHA-1, and SHA-256 hashes for files in a directory and save to a text file.")
    parser.add_argument('-f', '--start_directory', type=str, required=True, help='The directory to start scanning from.')
    parser.add_argument('-o', '--output_path', type=str, required=True, help='Path to save the output text file.')

    args = parser.parse_args()

    with open(args.output_path, 'w', encoding='utf-8') as file:
        for line in list_files(args.start_directory, exclude_path=args.output_path):
            file.write(line + '\n')

    print(f"Hashes have been saved to {args.output_path}")
