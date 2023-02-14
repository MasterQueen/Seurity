# _*_conding : UTF-8
# 开发时间 :  9:02
# 文件名称 : MLXG_kill_2.PY
import os
import win32api as w32a,win32gui as w32g,win32con as w32c
import re
import glob
import psutil

class MLXG_kiss_2():

    def __init__(self):
        pass
    """
    结束'wrme.exe'进程
    """
    def processWrmeKill(self):
        for a in psutil.process_iter():#遍历当前进程
            if a.name().find('wrme.exe')!= -1:#如果进程名在病毒文件中
                a.kill()#杀死病毒进程
                print(f'{a.name()}进程已结束')

    """
    结束'J833.exe'进程
    """
    def processJ833Kill(self):
        for a in psutil.process_iter():  # 遍历当前进程
            if a.name().find('J833.exe') != -1:  # 如果进程名在病毒文件中
                a.kill()  # 杀死病毒进程
                print(f'{a.name()}进程已结束')


    """
    获取病毒文件根路径
    """
    def getRootPath(self):
        key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services', 0, w32c.KEY_READ)
        ia_lsit = []
        sysSourcePath = 0
        patten = re.compile(r'C.*')
        for item in w32a.RegEnumKeyEx(key):  # 遍历Services下的子项
            if item[0].startswith('iaL'):
                ia_lsit.append(item[0])  # 获取以iaL开头的子项名称
        for a in ia_lsit:  # 遍历以iaL开头的子项名称
            key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, f'SYSTEM\\CurrentControlSet\\Services\\{a}',0,w32c.KEY_ALL_ACCESS)  # 获取访问子项的句柄
            i = 0
            while True:
                if w32a.RegEnumValue(key, i)[0] == 'ImagePath':  # 判断key是否为ImagePath
                    if w32a.RegEnumValue(key, i)[1].startswith('\??\C:'):  # 判断value中是否包含病毒路径
                        sysSourcePath = w32a.RegEnumValue(key, i)[1]  # 获取病毒文件value值
                        sysSourcePath = re.search(patten, sysSourcePath).group(0)  # 正则表达截取病毒文件路径
                i += 1
        if sysSourcePath == 0:
            print('未找到.sys文件注册表')
            return False
        else:
            sysSourcePath = sysSourcePath.split('WindowsApps')  # 病毒文件夹路径
            print(f'病毒文件根路径为{sysSourcePath[0]}')
            return sysSourcePath[0]

    """
    删除J833.exe
    """
    def deleteJ833Exe(self,rootPath):
        if rootPath:
            rootPath = rootPath.split('Microsoft')[0]
            print(rootPath)
            path=rootPath+'Temp\J833.exe'
            os.remove(path)
            print('J833.exe文件删除成功')
        else:
            print('未获取J833源文件路径（J833.exe文件删除失败）')

    """
    删除注册表R项
    """
    def deleteRegR(self):
        key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, f'SYSTEM\\CurrentControlSet\\Services\\R',0,w32c.KEY_ALL_ACCESS)  # 获取访问子项的句柄
        i = 0
        while True:
            if w32a.RegEnumValue(key, i)[0] == 'ImagePath':  # 判断key是否为ImagePath
                if w32a.RegEnumValue(key, i)[1].endswith('J833.exe'):  # 判断value中是否包含病毒路径
                    w32a.RegDeleteValue(key, 'ImagePath')  # 删除注册表
                    print(sysSourcePath + '注册表已删除')
                i += 1

    """
    删除Event Viwer下.exe文件
    """
    def deleteEventExe(self,rootPath):
        path=rootPath+'Event Viewer'
        path=os.rename(path,rootPath+'Event Viewer1')
        exeFiles=os.listdir(path)
        for file in exeFiles:
            if file.endswith('.exe'):
                os.remove(file)
                print(f'成功删除{file}')

    """
    删除.sys注册表项
    """
    def deleteRegSYS(self):
        key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services',0,w32c.KEY_READ)  # 获取Services的句柄
        ia_lsit = []  # iaL开头的子项列表
        LS_list = []  # LS开头的子项列表
        sysSourcePath_one = ""  # ial中的.sys文件
        sysSourcePath_two = ""  # LS中的.sys文件
        patten = re.compile(r'C.*')
        for item in w32a.RegEnumKeyEx(key):  # 遍历Services下的子项
            if item[0].startswith('iaL'):
                # print(item[0])
                ia_lsit.append(item[0])  # 获取以iaL开头的子项名称
            if item[0].startswith('LS'):
                # print(item[0])
                LS_list.append(item[0])  # 获取以LS开头的子项名称
        for a in ia_lsit:  # 遍历以iaL开头的子项名称
            key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, f'SYSTEM\\CurrentControlSet\\Services\\{a}',0,w32c.KEY_ALL_ACCESS)  # 获取访问子项的句柄
            i = 0
            while True:
                if w32a.RegEnumValue(key, i)[0] == 'ImagePath':  # 判断key是否为ImagePath
                    if w32a.RegEnumValue(key, i)[1].startswith('\??\C:'):  # 判断value中是否包含病毒路径
                        sysSourcePath_one = w32a.RegEnumValue(key, i)[1]  # 获取病毒文件value值
                        sysSourcePath_one = re.search(patten, sysSourcePath_one).group(0)  # 正则表达截取病毒文件路径
                        print(sysSourcePath_one)
                        w32a.RegDeleteValue(key, 'ImagePath')  # 删除注册表
                        print(sysSourcePath_one + '注册表已删除')
                i += 1
        for a in LS_list:  # 遍历以LS开头的子项名称
            key = w32a.RegOpenKey(w32c.HKEY_LOCAL_MACHINE, f'SYSTEM\\CurrentControlSet\\Services\\{a}',0,w32c.KEY_ALL_ACCESS)  # 获取访问子项的句柄
            i = 0
            while True:
                if w32a.RegEnumValue(key, i)[0] == 'ImagePath':  # 判断key是否为ImagePath
                    if w32a.RegEnumValue(key, i)[1].startswith('\??\C:'):  # 判断value中是否包含病毒路径
                        sysSourcePath_two = w32a.RegEnumValue(key, i)[1]  # 获取病毒文件value值
                        sysSourcePath_two = re.search(patten, sysSourcePath_two).group(0)  # 正则表达截取病毒文件路径
                        print(sysSourcePath_two)
                        w32a.RegDeleteValue(key, 'ImagePath')  # 删除注册表
                        print(sysSourcePath_two + '注册表已删除')
                i += 1
        return sysSourcePath_one, sysSourcePath_two  # 返回两个.sys文件路径

    """
    删除.sys文件
    """
    def deleteSYS(self,sysSourcePath_one,sysSourcePath_two,rootPath):

        if 'WindowsApps' in os.listdir(rootPath):
            path = rootPath+'WindowsApps'
            os.rename(path,rootPath+'WindowsApps1')
        if sysSourcePath_one:
            sysSourcePath_one=sysSourcePath_one.replace('WindowsApps','WindowsApps1')
            os.remove(sysSourcePath_one)
            print(f'文件{sysSourcePath_one}已删除')
        else:
            print(f'文件{sysSourcePath_one}删除失败')
        if sysSourcePath_two:
            sysSourcePath_two = sysSourcePath_two.replace('WindowsApps', 'WindowsApps1')
            os.remove(sysSourcePath_two)
            print(f'文件{sysSourcePath_two}已删除')
        else:
            print(f'文件{sysSourcePath_two}删除失败')

if __name__ == '__main__':

    MLXG_kiss_2 = MLXG_kiss_2()

    #杀掉 j833进程
    try:
        MLXG_kiss_2.processJ833Kill()
    except:
        print('J833进程未找到')
    # 杀掉 wrme进程
    try:
        MLXG_kiss_2.processWrmeKill()
    except:
        print('wrme进程未找到')
    #获取病毒文件根路径
    rootPath=0
    try:
        rootPath = MLXG_kiss_2.getRootPath()
    except:
        print('未获取病毒文件根路径')
    #删除Event Viwer下.exe文件
    try:
        MLXG_kiss_2.deleteEventExe(rootPath=rootPath)
    except:
        print('Event Viwer下病毒文件删除失败')
    # 删除j833.exe文件
    try:
        MLXG_kiss_2.deleteJ833Exe(rootPath=rootPath)
    except:
        print('J833.exe病毒文件删除失败')
    #删除R注册表
    try:
        MLXG_kiss_2.deleteRegR()
    except:
        print('注册表R项未找到')

    #重启

    #删除.sys文件注册表
    sysSourcePath_one=0
    sysSourcePath_two=0
    try:
        sysSourcePath_one,sysSourcePath_two=MLXG_kiss_2.deleteRegSYS()
    except:
        print('.sys注册表未找到')
    #删除.sys文件
    try:
        MLXG_kiss_2.deleteSYS(sysSourcePath_one,sysSourcePath_two,rootPath)
    except:
        print('.sys文件删除失败')







