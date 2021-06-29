from gui import Message
import os
import zipfile
import shutil


def files_in_folder(dir_path, filter_extend=None):
    """根据文件件位置,返回对应的所有文件"""
    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if filter_extend:
                file_extend = file.split('.')[-1].lower()
                if file_extend in filter_extend:
                    file_path_list.append(os.path.join(root, file))
            else:
                file_path_list.append(os.path.join(root, file))
    Message.info('获取<{}>文件夹下所有的文件'.format(dir_path))
    return file_path_list


def create_folder(path):
    """创建文件夹,如果地址的父文件不存在也会一同创建"""
    os.makedirs(path)
    Message.info('创建文件夹:{}'.format(path))


def file_extension(path):
    """文件完整路径->文件的扩展名"""
    return os.path.splitext(path)[1]


def raw_file_name(path):
    """文件完整路径->文件名(含扩展名)"""
    return os.path.split(path)[1]


def pure_file_name(path):
    """文件完整路径->纯文件名(不含扩展名)"""
    file_name = os.path.basename(path)
    pure_name = os.path.splitext(file_name)[0]
    return pure_name


def unzip_file(zipfilepath, result_path):
    """将zip文件解压到指定文件夹"""
    f = zipfile.ZipFile(zipfilepath, 'r')
    for file in f.namelist():
        f.extract(file, result_path)
    Message.info('解压文件:<{}>到:<{}>'.format(zipfilepath, result_path))


def copy_file(file_path, folder):
    """将文件拷贝到指定目录"""
    shutil.copy(file_path, folder)
    Message.info('复制文件:<{}>到:<{}>'.format(file_path, folder))


def delete_folder(folder):
    """删除文件夹及其子件"""
    shutil.rmtree(folder)
    Message.info('删除文件夹:<{}>'.format(folder))
