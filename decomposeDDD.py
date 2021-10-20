import os,os.path
from os.path import exists
import sys,shutil
from wand.image import Image
import string

mtlnamelist={}


def endwith(s,*endstring):
    array = map(s.endswith, endstring)
    if True in array:
        return True
    else:
        return False

def getAllSourceFile(folder,ext):
    arrSource = []
    for root,dirs,files in os.walk(folder):
        for file in files:
            if endwith(file,ext) or endwith(file,ext.upper()):
                allSourceFile = os.path.join(root,file)
                arrSource.append(allSourceFile)
    return arrSource


def changeImage(folder, ext, outputFolder, targetFormat):
    arr = getAllSourceFile(folder, ext)
    for ar in arr:
        with Image(filename = ar) as im:
            fname = os.path.basename(ar)
            findex = fname.rfind('.')
            fname = fname[:findex]
            im.rotate(90)
            im.transpose()
            print(outputFolder+"\\texture\\"+fname+'.'+targetFormat)
            im.save(filename=outputFolder+"\\texture\\"+fname+'.'+targetFormat)


def OBJSplit(objPath, changeFormat,mapsFolder, outputFolder,targetFormat):
    try:
        os.mkdir(outputFolder+"\\texture")
    except:
        pass

    changeImage(mapsFolder, changeFormat, outputFolder, targetFormat)


def mtlChaifen(changeFormat, targetFormat, mtlfile,imagePath):
    
    rfile=open(mtlfile,'r')
    wrlLines=rfile.readlines()
    rfile.close()
    dicname={}
    Numlist=[]
    for i in range(0,len(wrlLines)):
        wrlstring=wrlLines[i]
        wrlstring=wrlstring.strip()
        wl=len(wrlstring)
        
        extendsion = os.path.splitext(wrlstring)[-1]
        if(changeFormat==""):
            changeFormat = extendsion

        if wrlstring[0:6]=='newmtl':
            Numlist.append(i)           
        elif extendsion== '.' + changeFormat:
            wrlLines[i]=wrlLines[i].replace(changeFormat,targetFormat)
        elif extendsion== '.' + changeFormat.upper():
            wrlLines[i]=wrlLines[i].replace(changeFormat.upper(),targetFormat)

    strList=[]
    for i in range(0,len(Numlist)):
        strcontent=''
        if i!=len(Numlist)-1:
            
            for j in range(Numlist[i],Numlist[i+1]):
                if 'newmtl ' in wrlLines[j]:
                    wrlstring=wrlLines[j].strip()
                    mtln=wrlstring.find(' ')
                    mtlname=wrlstring[mtln+1:len(wrlstring)]
                    if mtlname not in mtlnamelist:
                        mtlnamelist[mtlname]='mtlname'+str(j)
                    strcontent+=wrlLines[j].replace(mtlname,mtlnamelist[mtlname])
                elif 'map_Ka ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                    print(imagePath+imagename)
                    if os.path.isfile(imagePath+imagename):
                        if os.path.isfile(imagePath+dicname[imagename]):
                            print("文件已存在")
                        else:
                            shutil.copy(imagePath+imagename,imagePath+dicname[imagename])
                    #strcontent+='\n'
                elif 'map_Kd ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                elif 'map_d ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                elif '\td ' in wrlLines[j]:
                    strcontent+='\td 1.0\n'
                elif 'illum ' in wrlLines[j]:
                    strcontent+='\tillum 3\n'
                elif 'Ka ' in wrlLines[j]:
                    strcontent+='\tKa 0 0 0\n'
                elif 'Kd ' in wrlLines[j]:
                    strcontent+='\tKd 1 1 1\n'
                elif 'Ks ' in wrlLines[j]:
                    strcontent+='\tKs 0 0 0\n'
                elif 'Ns ' in wrlLines[j]:
                    strcontent+='\tNs 0\n'
                elif 'Ni ' in wrlLines[j]:
                    strcontent+='\tNi 1.0\n'
                elif 'Tf ' in wrlLines[j]:
                    strcontent+='\tTf 1.0 1.0 1.0\n'                
            strList.append(strcontent)
                
        else:
            for j in range(Numlist[i],len(wrlLines)):
                if 'newmtl ' in wrlLines[j]:
                    wrlstring=wrlLines[j].strip()
                    mtln=wrlLines[j].find(' ')
                    mtlname=wrlstring[mtln+1:len(wrlstring)]
                    if mtlname not in mtlnamelist:
                        mtlnamelist[mtlname]='mtlname'+str(j)
                    strcontent+=wrlLines[j].replace(mtlname,mtlnamelist[mtlname])

                elif 'map_Ka ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                    print(imagePath+imagename)
                    if os.path.isfile(imagePath+imagename):
                        if os.path.isfile(imagePath+dicname[imagename]):
                            print("文件已存在")
                        else:
                            shutil.copy(imagePath+imagename,imagePath+dicname[imagename])
                elif 'map_Kd ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                elif 'map_d ' in wrlLines[j]:
                    strname=wrlLines[j]
                    len2=strname.rfind('.')
                    len3=strname.find(' ')
                    imagename=strname[len3+1:len2+4]
                    imageext=strname[len2:len2+4]
                    if imagename not in dicname:
                        dicname[imagename]='textureobj'+str(j)+imageext
                    strname=strname.replace(imagename,dicname[imagename])
                    strcontent+=strname
                elif '\td ' in wrlLines[j]:
                    strcontent+='\td 1.0\n'
                elif 'illum ' in wrlLines[j]:
                    strcontent+='\tillum 3\n'
                elif 'Ka ' in wrlLines[j]:
                    strcontent+='\tKa 0 0 0\n'
                elif 'Kd ' in wrlLines[j]:
                    strcontent+='\tKd 1 1 1\n'
                elif 'Ks ' in wrlLines[j]:
                    strcontent+='\tKs 0 0 0\n'
                elif 'Ns ' in wrlLines[j]:
                    strcontent+='\tNs 0\n'
                elif 'Ni ' in wrlLines[j]:
                    strcontent+='\tNi 1.0\n'
                elif 'Tf ' in wrlLines[j]:
                    strcontent+='\tTf 1.0 1.0 1.0\n'
                
            strList.append(strcontent)

    return strList

if __name__ == "__main__":
    # obj文件
    objPath = '新建文件夹\tietu.obj'
    # 贴图文件夹
    mapsFolder = '新建文件夹\maps'
    # 输出文件夹，这里输出新的多个obj、mtl文件，以及texture文件夹存放所有模型贴图
    # 建议使用空文件夹
    outputFolder = 'output'
    # print(getAllSourceFile(mapsFolder, "tga"))
    changeFormat = ""
    targetFormat = "jpg"
    OBJSplit(objPath, changeFormat,mapsFolder, outputFolder,targetFormat)