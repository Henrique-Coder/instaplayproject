### Premade by @Henrique-Coder (https://github.com/Henrique-Coder) ###



filename = 'instaplayproject-gui.py'
name = 'Instaplay-Project-GUI'
working_os = 'win'
version = '1.0.0'
icon = 'imgs/icon.ico'
upx_dir = 'upx'
data = 'dependencies/*;.'

from os import system as cmd
cmd(f'pyinstaller --noconsole --onefile --upx-dir={upx_dir} --icon={icon} --add-data={data} --name={name}-{working_os}-v{version} {filename}')



### Premade by @Henrique-Coder (https://github.com/Henrique-Coder) ###
