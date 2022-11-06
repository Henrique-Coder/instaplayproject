from dependencies import imgs
from PyQt5 import QtCore, QtGui, QtWidgets
from os import makedirs, environ, pathsep, getcwd, path, remove
from zstd import ZSTD_uncompress
from pathlib import Path
from requests import get
from multiprocessing.dummy import Process


# Section: Downloading and Uncompressing FFMPEG
def download_ffmpeg():
    userprofile_name = environ['userprofile']
    makedirs(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies', exist_ok=True)
    ffmpeg_exe = Path(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies\ffmpeg.exe')

    if not ffmpeg_exe.is_file():
        ffmpeg_url = 'https://drive.google.com/uc?export=download&id=16Ob9qv7uwLWqcMOwTOKeC9p52accn-wO'
        r = get(ffmpeg_url, allow_redirects=True)
        open(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies\ffmpeg.exe.zst', 'wb').write(r.content)

        with open(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies\ffmpeg.exe.zst', mode='rb') as fi:
            with open(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies\ffmpeg.exe', mode='wb') as fo:
                fo.write(ZSTD_uncompress(fi.read()))

        remove(fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies\ffmpeg.exe.zst')
    environ['PATH'] += pathsep + path.join(getcwd(), fr'{userprofile_name}\AppData\Local\Instaplay Project\dependencies')


# Section: Formating the Title
def format_title(title):
    from re import sub
    new_title = ''
    for ch in title:
        if ch in 'aáàâãäåbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyzAÁÀÂÃÄÅBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ0123456789-_()[]{}# ':
            new_title += ch
    new_title = sub(' +', ' ', new_title)
    new_title = new_title.strip()
    return new_title

# Section: Downloading the Video
def d_video(self, yt, output_path, title, video_quality, wait_processes):
    for p in wait_processes:
        p.join()
    video_title_mp4 = title + '.mp4'
    self.txt_progress_video.setText(' Downloading...')
    self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(233, 77, 78);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')
    yt.streams.filter(res=video_quality).first().download(output_path=output_path, filename=video_title_mp4)
    self.txt_progress_video.setText(' Completed!')
    self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(56, 229, 77);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')

# Section: Downloading the Audio
def d_audio(self, yt, output_path, title, wait_processes):
    for p in wait_processes:
        p.join()
    video_title_mp3 = title + '.mp3'
    self.txt_progress_audio.setText(' Downloading...')
    self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(233, 77, 78);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')
    yt.streams.filter(only_audio=True).first().download(output_path=output_path, filename=video_title_mp3)
    self.txt_progress_audio.setText(' Completed!')
    self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(56, 229, 77);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')

# Section: Merging the Video and Audio
def f_render(self, output_path, title, wait_processes):
    for p in wait_processes:
        p.join()
    from ffmpeg import input as ffinput, output as ffoutput
    makedirs('Videos', exist_ok=True)
    temp_video = fr'{output_path}\{title}.mp4'
    temp_audio = fr'{output_path}\{title}.mp3'
    output = fr'Videos\{title}.mp4'

    input_video = ffinput(temp_video)
    input_audio = ffinput(temp_audio)

    self.txt_progress_rendering.setText(' Merging...')
    self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(233, 77, 78);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')
    ffoutput(input_video, input_audio, output, acodec='copy', vcodec='copy').run(quiet=True, overwrite_output=True)
    self.txt_progress_rendering.setText(' Completed!')
    self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(56, 229, 77);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')

# Section: Deleting the Temp Files
def f_cleanup(self, output_path, wait_processes):
    for p in wait_processes:
        p.join()
    from shutil import rmtree
    self.txt_progress_finishing.setText(' Cleaning up...')
    self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(233, 77, 78);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')
    rmtree(output_path, ignore_errors=True)
    self.txt_progress_finishing.setText(' Completed!')
    self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                          '\n'
                                          'color: rgb(56, 229, 77);\n'
                                          'background-color: rgb(255, 255, 255);\n'
                                          '\n'
                                          'border-style: outset;\n'
                                          'border-width: 0px;\n'
                                          'border-radius: 4px;')

    self.warning_wait.setText('    DONE!')
    self.input_url.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    self.warning_wait.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    self.btn_reset_screen.show()


processes = {
    'download_ffmpeg': Process(target=download_ffmpeg),
    'download_video': None,
    'download_audio': None,
    'render': None,
    'cleanup': None
}
processes['download_ffmpeg'].start()

yt = None


class Ui_main(object):
    def setupUi(self, main):
        main.setObjectName('main')
        main.resize(411, 411)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(':/imgs/imgs/icon.ico'), QtGui.QIcon.Active, QtGui.QIcon.On)
        main.setWindowIcon(icon)
        main.setToolTip('')
        main.setStatusTip('')
        main.setWhatsThis('')
        main.setStyleSheet('background-color: rgb(64, 68, 75);')
        self.centralwidget = QtWidgets.QWidget(main)
        self.centralwidget.setObjectName('centralwidget')
        self.input_url = QtWidgets.QLineEdit(self.centralwidget)
        self.input_url.setGeometry(QtCore.QRect(10, 140, 301, 21))
        self.input_url.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.input_url.setTabletTracking(False)
        self.input_url.setStatusTip('')
        self.input_url.setStyleSheet('font: 12px;\n'
                                     '\n'
                                     'color: rgb(0, 0, 0);\n'
                                     'background-color: rgb(255, 255, 255);\n'
                                     'border-color: rgb(255, 255, 255);\n'
                                     '\n'
                                     'border-style: outset;\n'
                                     'border-width: 2px;\n'
                                     'border-radius: 4px;')

        self.input_url.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.input_url.setDragEnabled(True)
        self.input_url.setReadOnly(False)
        self.input_url.setCursorMoveStyle(QtCore.Qt.VisualMoveStyle)
        self.input_url.setClearButtonEnabled(True)
        self.input_url.setObjectName('input_url')
        self.txt_inputurl = QtWidgets.QLabel(self.centralwidget)
        self.txt_inputurl.setGeometry(QtCore.QRect(80, 110, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_inputurl.setFont(font)
        self.txt_inputurl.setStyleSheet('font: bold 11px;\n'
                                        '\n'
                                        'color: rgb(255, 255, 255);')

        self.txt_inputurl.setObjectName('txt_inputurl')
        self.logo_banner = QtWidgets.QLabel(self.centralwidget)
        self.logo_banner.setGeometry(QtCore.QRect(-10, 0, 431, 111))
        self.logo_banner.setStyleSheet('image: url(:/imgs/imgs/app-banner.png);')
        self.logo_banner.setText('')
        self.logo_banner.setObjectName('logo_banner')
        self.btn_show_resolutions = QtWidgets.QPushButton(self.centralwidget)
        self.btn_show_resolutions.setGeometry(QtCore.QRect(320, 140, 81, 21))
        self.btn_show_resolutions.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_show_resolutions.setStyleSheet('font: bold 12px;\n'
                                                '\n'
                                                'color: rgb(255, 255, 255);\n'
                                                'background-color: rgb(104, 131, 188);\n'
                                                'border-color: rgb(104, 131, 188);\n'
                                                '\n'
                                                'border-style: outset;\n'
                                                'border-width: 2px;\n'
                                                'border-radius: 4px;')

        self.btn_show_resolutions.setObjectName('btn_show_resolutions')
        self.decorative_line = QtWidgets.QLabel(self.centralwidget)
        self.decorative_line.setGeometry(QtCore.QRect(10, 60, 391, 121))
        self.decorative_line.setStyleSheet('image: url(:/imgs/imgs/decorative_line.png);')
        self.decorative_line.setText('')
        self.decorative_line.setObjectName('decorative_line')
        self.btn_quality_144p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_144p.setGeometry(QtCore.QRect(60, 210, 61, 21))
        self.btn_quality_144p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_144p.setStyleSheet('font: bold 11px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(223, 54, 45);\n'
                                            'border-color: rgb(223, 54, 45);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 1px;\n'
                                            'border-radius: 4px;')

        self.btn_quality_144p.setObjectName('btn_quality_144p')
        self.btn_quality_240p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_240p.setGeometry(QtCore.QRect(130, 210, 61, 21))
        self.btn_quality_240p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_240p.setStyleSheet('font: bold 11px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(223, 54, 45);\n'
                                            'border-color: rgb(223, 54, 45);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 1px;\n'
                                            'border-radius: 4px;')

        self.btn_quality_240p.setObjectName('btn_quality_240p')
        self.btn_quality_360p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_360p.setGeometry(QtCore.QRect(200, 210, 61, 21))
        self.btn_quality_360p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_360p.setStyleSheet('font: bold 11px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(223, 54, 45);\n'
                                            'border-color: rgb(223, 54, 45);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 1px;\n'
                                            'border-radius: 4px;')

        self.btn_quality_360p.setObjectName('btn_quality_360p')
        self.btn_quality_480p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_480p.setGeometry(QtCore.QRect(60, 240, 61, 21))
        self.btn_quality_480p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_480p.setStyleSheet('font: bold 11px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(223, 54, 45);\n'
                                            'border-color: rgb(223, 54, 45);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 1px;\n'
                                            'border-radius: 4px;')

        self.btn_quality_480p.setObjectName('btn_quality_480p')
        self.btn_quality_720p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_720p.setGeometry(QtCore.QRect(130, 240, 61, 21))
        self.btn_quality_720p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_720p.setStyleSheet('font: bold 11px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(223, 54, 45);\n'
                                            'border-color: rgb(223, 54, 45);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 1px;\n'
                                            'border-radius: 4px;')

        self.btn_quality_720p.setObjectName('btn_quality_720p')
        self.btn_quality_1080p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_1080p.setGeometry(QtCore.QRect(200, 240, 61, 21))
        self.btn_quality_1080p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_1080p.setStyleSheet('font: bold 11px;\n'
                                             '\n'
                                             'color: rgb(255, 255, 255);\n'
                                             'background-color: rgb(223, 54, 45);\n'
                                             'border-color: rgb(223, 54, 45);\n'
                                             '\n'
                                             'border-style: outset;\n'
                                             'border-width: 1px;\n'
                                             'border-radius: 4px;')

        self.btn_quality_1080p.setObjectName('btn_quality_1080p')
        self.btn_quality_1440p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_1440p.setGeometry(QtCore.QRect(60, 270, 61, 21))
        self.btn_quality_1440p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_1440p.setStyleSheet('font: bold 11px;\n'
                                             '\n'
                                             'color: rgb(255, 255, 255);\n'
                                             'background-color: rgb(223, 54, 45);\n'
                                             'border-color: rgb(223, 54, 45);\n'
                                             '\n'
                                             'border-style: outset;\n'
                                             'border-width: 1px;\n'
                                             'border-radius: 4px;')

        self.btn_quality_1440p.setObjectName('btn_quality_1440p')
        self.btn_quality_2160p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_2160p.setGeometry(QtCore.QRect(130, 270, 61, 21))
        self.btn_quality_2160p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_2160p.setStyleSheet('font: bold 11px;\n'
                                             '\n'
                                             'color: rgb(255, 255, 255);\n'
                                             'background-color: rgb(223, 54, 45);\n'
                                             'border-color: rgb(223, 54, 45);\n'
                                             '\n'
                                             'border-style: outset;\n'
                                             'border-width: 1px;\n'
                                             'border-radius: 4px;')

        self.btn_quality_2160p.setObjectName('btn_quality_2160p')
        self.btn_quality_4320p = QtWidgets.QPushButton(self.centralwidget)
        self.btn_quality_4320p.setGeometry(QtCore.QRect(200, 270, 61, 21))
        self.btn_quality_4320p.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_quality_4320p.setStyleSheet('font: bold 11px;\n'
                                             '\n'
                                             'color: rgb(255, 255, 255);\n'
                                             'background-color: rgb(223, 54, 45);\n'
                                             'border-color: rgb(223, 54, 45);\n'
                                             '\n'
                                             'border-style: outset;\n'
                                             'border-width: 1px;\n'
                                             'border-radius: 4px;')

        self.btn_quality_4320p.setObjectName('btn_quality_4320p')
        self.warning_wait = QtWidgets.QLabel(self.centralwidget)
        self.warning_wait.setGeometry(QtCore.QRect(320, 140, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.warning_wait.setFont(font)
        self.warning_wait.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.warning_wait.setStyleSheet('font: bold 12px;\n'
                                        '\n'
                                        'color: rgb(255, 255, 255);\n'
                                        'background-color: rgb(104, 131, 188);\n'
                                        'border-color: rgb(104, 131, 188);\n'
                                        '\n'
                                        'border-style: outset;\n'
                                        'border-width: 2px;\n'
                                        'border-radius: 4px;')

        self.warning_wait.setObjectName('warning_wait')
        self.decorative_color_block_2 = QtWidgets.QLabel(self.centralwidget)
        self.decorative_color_block_2.setGeometry(QtCore.QRect(270, 210, 151, 81))
        self.decorative_color_block_2.setStyleSheet('background-color: rgb(59, 62, 69);\n'
                                                    '\n'
                                                    'border-style: outset;\n'
                                                    'border-width: 0px;\n'
                                                    'border-radius: 4px;')

        self.decorative_color_block_2.setText('')
        self.decorative_color_block_2.setObjectName('decorative_color_block_2')
        self.decorative_color_block = QtWidgets.QLabel(self.centralwidget)
        self.decorative_color_block.setGeometry(QtCore.QRect(-10, 210, 61, 81))
        self.decorative_color_block.setStyleSheet('background-color: rgb(59, 62, 69);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        self.decorative_color_block.setText('')
        self.decorative_color_block.setObjectName('decorative_color_block')
        self.txt_chooseresolution = QtWidgets.QLabel(self.centralwidget)
        self.txt_chooseresolution.setGeometry(QtCore.QRect(60, 180, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_chooseresolution.setFont(font)
        self.txt_chooseresolution.setStyleSheet('font: bold 11px;\n'
                                                '\n'
                                                'color: rgb(255, 255, 255);')

        self.txt_chooseresolution.setObjectName('txt_chooseresolution')
        self.decorative_line_2 = QtWidgets.QLabel(self.centralwidget)
        self.decorative_line_2.setGeometry(QtCore.QRect(10, 130, 391, 121))
        self.decorative_line_2.setStyleSheet('image: url(:/imgs/imgs/decorative_line.png);')
        self.decorative_line_2.setText('')
        self.decorative_line_2.setObjectName('decorative_line_2')
        self.txt_progress = QtWidgets.QLabel(self.centralwidget)
        self.txt_progress.setGeometry(QtCore.QRect(110, 180, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_progress.setFont(font)
        self.txt_progress.setStyleSheet('font: bold 11px;\n'
                                        '\n'
                                        'color: rgb(255, 255, 255);')

        self.txt_progress.setObjectName('txt_progress')
        self.txt_video = QtWidgets.QLabel(self.centralwidget)
        self.txt_video.setGeometry(QtCore.QRect(10, 210, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_video.setFont(font)
        self.txt_video.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.txt_video.setStyleSheet('font: bold 11px;\n'
                                     '\n'
                                     'color: rgb(255, 255, 255);\n'
                                     'background-color: rgb(104, 131, 188);\n'
                                     'border-color: rgb(104, 131, 188);\n'
                                     '\n'
                                     'border-style: outset;\n'
                                     'border-width: 2px;\n'
                                     'border-radius: 4px;')

        self.txt_video.setObjectName('txt_video')
        self.txt_progress_video = QtWidgets.QLabel(self.centralwidget)
        self.txt_progress_video.setGeometry(QtCore.QRect(100, 210, 301, 21))
        self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')

        self.txt_progress_video.setObjectName('txt_progress_video')
        self.txt_audio = QtWidgets.QLabel(self.centralwidget)
        self.txt_audio.setGeometry(QtCore.QRect(10, 240, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_audio.setFont(font)
        self.txt_audio.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.txt_audio.setStyleSheet('font: bold 11px;\n'
                                     '\n'
                                     'color: rgb(255, 255, 255);\n'
                                     'background-color: rgb(104, 131, 188);\n'
                                     'border-color: rgb(104, 131, 188);\n'
                                     '\n'
                                     'border-style: outset;\n'
                                     'border-width: 2px;\n'
                                     'border-radius: 4px;')

        self.txt_audio.setObjectName('txt_audio')
        self.txt_progress_audio = QtWidgets.QLabel(self.centralwidget)
        self.txt_progress_audio.setGeometry(QtCore.QRect(100, 240, 301, 21))
        self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')

        self.txt_progress_audio.setObjectName('txt_progress_audio')
        self.txt_rendering = QtWidgets.QLabel(self.centralwidget)
        self.txt_rendering.setGeometry(QtCore.QRect(10, 270, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_rendering.setFont(font)
        self.txt_rendering.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.txt_rendering.setStyleSheet('font: bold 11px;\n'
                                         '\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'background-color: rgb(104, 131, 188);\n'
                                         'border-color: rgb(104, 131, 188);\n'
                                         '\n'
                                         'border-style: outset;\n'
                                         'border-width: 2px;\n'
                                         'border-radius: 4px;')

        self.txt_rendering.setObjectName('txt_rendering')
        self.txt_progress_rendering = QtWidgets.QLabel(self.centralwidget)
        self.txt_progress_rendering.setGeometry(QtCore.QRect(100, 270, 301, 21))
        self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(255, 197, 0);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        self.txt_progress_rendering.setObjectName('txt_progress_rendering')
        self.txt_finishing = QtWidgets.QLabel(self.centralwidget)
        self.txt_finishing.setGeometry(QtCore.QRect(10, 300, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.txt_finishing.setFont(font)
        self.txt_finishing.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.txt_finishing.setStyleSheet('font: bold 11px;\n'
                                         '\n'
                                         'color: rgb(255, 255, 255);\n'
                                         'background-color: rgb(104, 131, 188);\n'
                                         'border-color: rgb(104, 131, 188);\n'
                                         '\n'
                                         'border-style: outset;\n'
                                         'border-width: 2px;\n'
                                         'border-radius: 4px;')

        self.txt_finishing.setObjectName('txt_finishing')
        self.txt_progress_finishing = QtWidgets.QLabel(self.centralwidget)
        self.txt_progress_finishing.setGeometry(QtCore.QRect(100, 300, 301, 21))
        self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(255, 197, 0);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        self.txt_progress_finishing.setObjectName('txt_progress_finishing')
        self.btn_reset_screen = QtWidgets.QPushButton(self.centralwidget)
        self.btn_reset_screen.setGeometry(QtCore.QRect(80, 350, 251, 31))
        self.btn_reset_screen.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.btn_reset_screen.setStyleSheet('font: bold 12px;\n'
                                            '\n'
                                            'color: rgb(255, 255, 255);\n'
                                            'background-color: rgb(254, 86, 86);\n'
                                            'border-color: rgb(254, 86, 86);\n'
                                            '\n'
                                            'border-style: outset;\n'
                                            'border-width: 2px;\n'
                                            'border-radius: 4px;')

        self.btn_reset_screen.setObjectName('btn_reset_screen')
        self.decorative_line_2.raise_()
        self.decorative_line.raise_()
        self.logo_banner.raise_()
        self.input_url.raise_()
        self.txt_inputurl.raise_()
        self.btn_quality_144p.raise_()
        self.btn_quality_240p.raise_()
        self.btn_quality_360p.raise_()
        self.btn_quality_480p.raise_()
        self.btn_quality_720p.raise_()
        self.btn_quality_1080p.raise_()
        self.btn_quality_1440p.raise_()
        self.btn_quality_2160p.raise_()
        self.btn_quality_4320p.raise_()
        self.btn_show_resolutions.raise_()
        self.warning_wait.raise_()
        self.decorative_color_block_2.raise_()
        self.decorative_color_block.raise_()
        self.txt_chooseresolution.raise_()
        self.txt_progress.raise_()
        self.txt_video.raise_()
        self.txt_progress_video.raise_()
        self.txt_audio.raise_()
        self.txt_progress_audio.raise_()
        self.txt_rendering.raise_()
        self.txt_progress_rendering.raise_()
        self.txt_finishing.raise_()
        self.txt_progress_finishing.raise_()
        self.btn_reset_screen.raise_()
        main.setCentralWidget(self.centralwidget)

        self.retranslateUi(main)
        QtCore.QMetaObject.connectSlotsByName(main)

    def retranslateUi(self, main):
        _translate = QtCore.QCoreApplication.translate
        main.setWindowTitle(_translate('main', 'Instaplay Project'))
        self.input_url.setToolTip(_translate('main', '<html><head/><body><p><br/></p></body></html>'))
        self.txt_inputurl.setText(_translate('main', '   Input YouTube Video URL'))
        self.btn_show_resolutions.setText(_translate('main', 'GO!'))
        self.btn_quality_144p.setText(_translate('main', '144p'))
        self.btn_quality_240p.setText(_translate('main', '240p'))
        self.btn_quality_360p.setText(_translate('main', '360p'))
        self.btn_quality_480p.setText(_translate('main', '480p'))
        self.btn_quality_720p.setText(_translate('main', '720p'))
        self.btn_quality_1080p.setText(_translate('main', '1080p'))
        self.btn_quality_1440p.setText(_translate('main', '1440p'))
        self.btn_quality_2160p.setText(_translate('main', '2160p'))
        self.btn_quality_4320p.setText(_translate('main', '4320p'))
        self.warning_wait.setText(_translate('main', '   WAIT...'))
        self.txt_chooseresolution.setText(_translate('main', ' Choose the resolution to download'))
        self.txt_progress.setText(_translate('main', '  Task Progression'))
        self.txt_video.setText(_translate('main', 'Video...'))
        self.txt_progress_video.setText(_translate('main', ' Pending...'))
        self.txt_audio.setText(_translate('main', 'Audio...'))
        self.txt_progress_audio.setText(_translate('main', ' Pending...'))
        self.txt_rendering.setText(_translate('main', 'Rendering...'))
        self.txt_progress_rendering.setText(_translate('main', ' Pending...'))
        self.txt_finishing.setText(_translate('main', 'Cleanup...'))
        self.txt_progress_finishing.setText(_translate('main', ' Pending...'))
        self.btn_reset_screen.setText(_translate('main', 'Click here to download another video'))

        ###############################################################################################################

        main.setFixedSize(411, 411)
        self.input_url.setMaxLength(100)

        # Section: Get Resolutions
        self.warning_wait.hide()
        self.input_url.setPlaceholderText('https://www.youtube.com/watch?v=...')
        self.txt_chooseresolution.hide()
        self.decorative_color_block.hide()
        self.decorative_color_block_2.hide()
        self.btn_quality_144p.hide()
        self.btn_quality_240p.hide()
        self.btn_quality_360p.hide()
        self.btn_quality_480p.hide()
        self.btn_quality_720p.hide()
        self.btn_quality_1080p.hide()
        self.btn_quality_1440p.hide()
        self.btn_quality_2160p.hide()
        self.btn_quality_4320p.hide()

        self.txt_progress.hide()
        self.txt_video.hide()
        self.txt_progress_video.hide()
        self.txt_audio.hide()
        self.txt_progress_audio.hide()
        self.txt_rendering.hide()
        self.txt_progress_rendering.hide()
        self.txt_finishing.hide()
        self.txt_progress_finishing.hide()
        self.btn_reset_screen.hide()

        self.btn_reset_screen.clicked.connect(self.reset_screen)
        self.btn_quality_144p.clicked.connect(self.set_quality_144p)
        self.btn_quality_240p.clicked.connect(self.set_quality_240p)
        self.btn_quality_360p.clicked.connect(self.set_quality_360p)
        self.btn_quality_480p.clicked.connect(self.set_quality_480p)
        self.btn_quality_720p.clicked.connect(self.set_quality_720p)
        self.btn_quality_1080p.clicked.connect(self.set_quality_1080p)
        self.btn_quality_1440p.clicked.connect(self.set_quality_1440p)
        self.btn_quality_2160p.clicked.connect(self.set_quality_2160p)
        self.btn_quality_4320p.clicked.connect(self.set_quality_4320p)

        self.btn_show_resolutions.clicked.connect(self.get_resolutions)

    def get_resolutions(self):
        from pytube import YouTube
        from re import match

        self.input_url.setStyleSheet('font: 12px;\n'
                                     '\n'
                                     'color: rgb(0, 0, 0);\n'
                                     'background-color: rgb(255, 255, 255);\n'
                                     'border-color: rgb(255, 255, 255);\n'
                                     '\n'
                                     'border-style: outset;\n'
                                     'border-width: 2px;\n'
                                     'border-radius: 4px;')

        url = self.input_url.text()
        yt_pattern = r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$'
        is_valid = match(yt_pattern, url)

        if is_valid:
            global yt
            yt = YouTube(url)
            self.btn_show_resolutions.hide()
            self.warning_wait.show()
            self.txt_chooseresolution.show()
            self.input_url.setReadOnly(True)
            self.input_url.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

            # The resolution buttons will appear if the video has them
            if yt.streams.filter(res='144p').first() is not None:
                self.btn_quality_144p.show()
            if yt.streams.filter(res='240p').first() is not None:
                self.btn_quality_240p.show()
            if yt.streams.filter(res='360p').first() is not None:
                self.btn_quality_360p.show()
            if yt.streams.filter(res='480p').first() is not None:
                self.btn_quality_480p.show()
            if yt.streams.filter(res='720p').first() is not None:
                self.btn_quality_720p.show()
            if yt.streams.filter(res='1080p').first() is not None:
                self.btn_quality_1080p.show()
            if yt.streams.filter(res='1440p').first() is not None:
                self.btn_quality_1440p.show()
            if yt.streams.filter(res='2160p').first() is not None:
                self.btn_quality_2160p.show()
            if yt.streams.filter(res='4320p').first() is not None:
                self.btn_quality_4320p.show()

        else:
            self.input_url.setStyleSheet('font: 12px;\n'
                                         '\n'
                                         'color: rgb(255, 0, 0);\n'
                                         'background-color: rgb(255, 255, 255);\n'
                                         'border-color: rgb(255, 255, 255);\n'
                                         '\n'
                                         'border-style: outset;\n'
                                         'border-width: 2px;\n'
                                         'border-radius: 4px;')

    # Section: Downloading
    def hide_resolutions_section(self):
        self.txt_chooseresolution.hide()
        self.decorative_color_block.hide()
        self.decorative_color_block_2.hide()
        self.btn_quality_144p.hide()
        self.btn_quality_240p.hide()
        self.btn_quality_360p.hide()
        self.btn_quality_480p.hide()
        self.btn_quality_720p.hide()
        self.btn_quality_1080p.hide()
        self.btn_quality_1440p.hide()
        self.btn_quality_2160p.hide()
        self.btn_quality_4320p.hide()

    def show_progress_bars(self):
        self.txt_progress.show()
        self.txt_video.show()
        self.txt_progress_video.show()
        self.txt_audio.show()
        self.txt_progress_audio.show()
        self.txt_rendering.show()
        self.txt_progress_rendering.show()
        self.txt_finishing.show()
        self.txt_progress_finishing.show()

    def set_quality(self, video_quality):
        self.hide_resolutions_section()
        self.show_progress_bars()
        userprofile_name = environ['userprofile']
        output_path = fr'{userprofile_name}\AppData\Local\Instaplay Project\temp'
        global yt
        title = format_title(yt.title)

        wait_processes = [processes['download_ffmpeg']]
        processes['download_video'] = Process(target=d_video, args=(self, yt, output_path, title, video_quality, wait_processes))
        processes['download_video'].start()

        processes['download_audio'] = Process(target=d_audio, args=(self, yt, output_path, title, wait_processes))
        processes['download_audio'].start()

        wait_processes = [processes['download_audio'], processes['download_video']]
        processes['render'] = Process(target=f_render, args=(self, output_path, title, wait_processes))
        processes['render'].start()

        wait_processes = [processes['render']]
        processes['cleanup'] = Process(target=f_cleanup, args=(self, output_path, wait_processes))
        processes['cleanup'].start()

    def set_quality_144p(self):
        self.set_quality(video_quality='144p')
    def set_quality_240p(self):
        self.set_quality(video_quality='240p')
    def set_quality_360p(self):
        self.set_quality(video_quality='360p')
    def set_quality_480p(self):
        self.set_quality(video_quality='480p')
    def set_quality_720p(self):
        self.set_quality(video_quality='720p')
    def set_quality_1080p(self):
        self.set_quality(video_quality='1080p')
    def set_quality_1440p(self):
        self.set_quality(video_quality='1440p')
    def set_quality_2160p(self):
        self.set_quality(video_quality='2160p')
    def set_quality_4320p(self):
        self.set_quality(video_quality='4320p')

    def reset_screen(self):
        self.warning_wait.hide()
        self.btn_show_resolutions.show()
        self.input_url.setReadOnly(False)
        self.input_url.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.input_url.setText('')
        self.input_url.setStyleSheet('font: 12px;\n'
                                     '\n'
                                     'color: rgb(0, 0, 0);\n'
                                     'background-color: rgb(255, 255, 255);\n'
                                     'border-color: rgb(255, 255, 255);\n'
                                     '\n'
                                     'border-style: outset;\n'
                                     'border-width: 2px;\n'
                                     'border-radius: 4px;')

        self.warning_wait.setText('   WAIT...')
        self.warning_wait.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.txt_video.hide()
        self.txt_chooseresolution.hide()
        self.txt_progress.hide()
        self.txt_progress_video.hide()
        self.txt_audio.hide()
        self.txt_progress_audio.hide()
        self.txt_rendering.hide()
        self.txt_progress_rendering.hide()
        self.txt_finishing.hide()
        self.txt_progress_finishing.hide()
        self.btn_reset_screen.hide()

        # Reset progress bars text
        self.txt_progress_video.setText(' Pending...')
        self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')

        self.txt_progress_audio.setText(' Pending...')
        self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')

        self.txt_progress_rendering.setText(' Pending...')
        self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')

        self.txt_progress_finishing.setText(' Pending...')
        self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                              '\n'
                                              'color: rgb(255, 197, 0);\n'
                                              'background-color: rgb(255, 255, 255);\n'
                                              '\n'
                                              'border-style: outset;\n'
                                              'border-width: 0px;\n'
                                              'border-radius: 4px;')


    '''
    def download_video(self, yt, output_path, video_quality):
        from ffmpeg import input as ffinput, output as ffoutput
        from shutil import rmtree


        def format_title(title):
            from re import sub
            new_title = ''
            for ch in title:
                if ch in 'aáàâãäåbcçdeéèêëfghiíìîïjklmnoóòôõöpqrstuúùûüvwxyzAÁÀÂÃÄÅBCÇDEÉÈÊËFGHIÍÌÎÏJKLMNOÓÒÔÕÖPQRSTUÚÙÛÜVWXYZ0123456789-_()[]{}# ':
                    new_title += ch
            new_title = sub(' +', ' ', new_title)
            new_title = new_title.strip()
            return new_title

        video_title_mp4 = format_title(yt.title) + '.mp4'
        video_title_mp3 = format_title(yt.title) + '.mp3'

        def d_video():
            self.txt_progress_video.setText(' Downloading...')
            self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(233, 77, 78);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')
            yt.streams.filter(res=video_quality).first().download(output_path=output_path, filename=video_title_mp4)
            self.txt_progress_video.setText(' Completed!')
            self.txt_progress_video.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(56, 229, 77);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        def d_audio():
            self.txt_progress_audio.setText(' Downloading...')
            self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(233, 77, 78);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')
            yt.streams.filter(only_audio=True).first().download(output_path=output_path, filename=video_title_mp3)
            self.txt_progress_audio.setText(' Completed!')
            self.txt_progress_audio.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(56, 229, 77);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        def f_merging():
            makedirs('Videos', exist_ok=True)
            temp_video = fr'{output_path}\{video_title_mp4}'
            temp_audio = fr'{output_path}\{video_title_mp3}'
            output = fr'Videos\{video_title_mp4}'

            input_video = ffinput(temp_video)
            input_audio = ffinput(temp_audio)

            self.txt_progress_rendering.setText(' Merging...')
            self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(233, 77, 78);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')
            ffoutput(input_video, input_audio, output, acodec='copy', vcodec='copy').run(quiet=True, overwrite_output=True)
            self.txt_progress_rendering.setText(' Completed!')
            self.txt_progress_rendering.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(56, 229, 77);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')

        def f_cleanup():
            self.txt_progress_finishing.setText(' Cleaning up...')
            self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                                  '\n'
                                                  'color: rgb(233, 77, 78);\n'
                                                  'background-color: rgb(255, 255, 255);\n'
                                                  '\n'
                                                  'border-style: outset;\n'
                                                  'border-width: 0px;\n'
                                                  'border-radius: 4px;')
            rmtree(output_path, ignore_errors=True)
            self.txt_progress_finishing.setText(' Completed!')
            self.txt_progress_finishing.setStyleSheet('font: bold 11px;\n'
                                      '\n'
                                      'color: rgb(56, 229, 77);\n'
                                      'background-color: rgb(255, 255, 255);\n'
                                      '\n'
                                      'border-style: outset;\n'
                                      'border-width: 0px;\n'
                                      'border-radius: 4px;')

            self.warning_wait.setText('    DONE!')
            self.input_url.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.warning_wait.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.btn_reset_screen.show()

        # p1 = Process(target=d_video)
        # p2 = Process(target=d_audio)
        # p3 = Process(target=f_merging)
        # p4 = Process(target=f_cleanup)

        # p1.start()
        # p1.join()

        # p2.start()
        # p2.join()

        # p3.start()
        # p3.join()

        # p4.start()
        # p4.join()

        d_video()
        d_audio()
        f_merging()
        f_cleanup()
    '''


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = QtWidgets.QMainWindow()
    ui = Ui_main()
    ui.setupUi(main)
    main.show()
    sys.exit(app.exec_())
