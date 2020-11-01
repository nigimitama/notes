'''

- modulesフォルダを移動する
- assetsフォルダがネストされていたら第一層に移動する
- madkrownファイルのpathを取得
- htmlファイルの生成
'''
import os
import shutil


class Build:

    def __init__(self, work_dir='docs'):
        self.work_dir = work_dir

    def main(self):
        self._reset_wd()
        self._copy_modules()
        self._copy_files()
        self._change_dir_if_its_wrong()
        file_paths = self._get_file_paths()
        file_dirs = self._get_file_dirs()
        assets_dirs = [f for f in file_dirs if '.assets' in f]
        return self

    def _reset_wd(self):
        if os.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        os.mkdir(self.work_dir)
        return self

    def _copy_modules(self):
        dir_path = f'{self.work_dir}/modules'
        os.mkdir(dir_path)
        shutil.copytree('pandoc/modules', dir_path)
        return self

    def _copy_files(self):
        '''markdownファイルや添付画像をコピーする'''
        shutil.copytree('pandoc/modules', dir_path)

    def _change_dir_if_its_wrong(self):
        pwd = os.getcwd()
        pwd_dir = os.path.split(pwd)[-1]
        if pwd_dir == 'scripts':
            os.chdir('..')
        return self

    def _get_file_paths(self):
        path = self.work_dir
        paths = []
        for current_dir, dirs, files in os.walk(path):
            for dir in dirs:
                for file in files:
                    path = os.path.join(current_dir, dir, file)
                    paths.append(path)
        return paths

    def _get_file_dirs(self):
        path = self.work_dir
        paths = []
        for current_dir, dirs, _ in os.walk(path):
            for dir in dirs:
                path = os.path.join(current_dir, dir)
                paths.append(path)
        return paths


if __name__ == '__main__':
    # Build().main()
    b = Build()
    b._change_dir_if_its_wrong()
    b._copy_modules()
