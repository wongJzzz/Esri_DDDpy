# -*- coding: utf-8 -*-
# A:wangj
# 说明：该工具用于处理使用3ds max按默认模式导出的OBJ文件，要求每一个单体是一个对象且尽量具备唯一的名称。
# Import arcpy module

import os,os.path
from os.path import exists
import sys,shutil
from wand.image import Image
import string
# import arcpy

mtlnamelist={}

def endwith(s,*endstring):
    array = map(s.endswith,endstring)
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

def changeImgae(folder,ext): 
    arr=getAllSourceFile(folder,ext)
    for ar in arr:
        with Image(filename=ar) as im:
            fname=os.path.basename(ar)
            findex=fname.rfind('.')
            fname=fname[:findex]
            print(fname)
            im.rotate(90)
            im.transpose()
            im.save(filename=folder+fname+".jpg")

#mtl参数采用自定义的参数，模型能够更加明亮
def mtlChaifen(mtlfile,imagePath):
    
    rfile=open(mtlfile,'r')
    wrlLines=rfile.readlines()
    rfile.close()
    dicname={}
    Numlist=[]
    for i in range(0,len(wrlLines)):
        wrlstring=wrlLines[i]
        wrlstring=wrlstring.strip()
        wl=len(wrlstring)
        if wrlstring[0:6]=='newmtl':
            Numlist.append(i)           
        elif wrlstring[wl-4:wl]=='.tga':
            wrlLines[i]=wrlLines[i].replace('tga','jpg')
        elif wrlstring[wl-4:wl]=='.TGA':
            wrlLines[i]=wrlLines[i].replace('TGA','jpg')

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
    
def OBJChaiFen(objfile,objfolder,mtlList=""):
    #读取OBJ文件并记录
    rfile=open(objfile,'r')
    objLines=rfile.readlines()
    rfile.close()

    #用于记录生成新的OBJ文件数量以及区分同名的对象
    NewOBJNum=1

    #以object做为关键字对OBJ进行区分，行号记录在Numlist中
    Numlist=[]
    for i in range(0,len(objLines)):
        if objLines[i][0:8]=='# object':
            Numlist.append(i)
        if objLines[i][0:6]=='usemtl':
            mtlstring=objLines[i].strip()
            mtln=objLines[i].find(' ')
            mtlname=mtlstring[mtln+1:len(mtlstring)]
            objLines[i]=objLines[i].replace(mtlname,mtlnamelist[mtlname])
    for i in range(0,len(Numlist)):
        SigOBJ=[]
        if i!=len(Numlist)-1:
            SigOBJ=objLines[Numlist[i]:Numlist[i+1]]
        else:
            SigOBJ=objLines[Numlist[i]:]

        # 按对象名称赋给新生成的obj文件
        NameAttr=objLines[Numlist[i]][:-1].split(' ')

        newobj=NameAttr[-1]+'_'+str(NewOBJNum)+'.obj'
        newmtl=NameAttr[-1]+'_'+str(NewOBJNum)+'.mtl'

        NewOBJNum+=1

        #写入新的OBJ文件
        OBJWrite(SigOBJ,objfolder,newobj,newmtl,mtlList)

def OBJWrite(OBJList,objfolder,newobj,newmtl,mtlList=""):
    #模型写入
    objpath=os.path.join(objfolder,newobj)
    wfile=open(objpath,'w')
    wfile.writelines('# Product by Esri China Information Technology Co.,Ltd.\n')
    wfile.writelines('\n mtllib '+newmtl+'\n\n')
    wfile.writelines(OBJList)
    wfile.close()

    #OBJ文件优化
    OBJoptimization(objpath)
    
    #mtl文件写入
    # mtlpath=newmtl
    mtlpath=os.path.join(objfolder,newmtl)
    wmtlfile=open(mtlpath,'w')
    wmtlfile.writelines('# Product by Esri China Information Technology Co.,Ltd.\n\n')

    wmtl=[]
    for j in range(0,len(OBJList)):
        if 'usemtl' in OBJList[j]:
            strmtlline='new'+OBJList[j][3:]
            for k in range(0,len(mtlList)):
                if strmtlline in mtlList[k]:
                    wmtl.append(mtlList[k])
                    #wmtlfile.writelines(mtlList[k])
    newlist=list(set(wmtl))
    for j in range(0,len(newlist)):
        wmtlfile.writelines(newlist[j])

    wmtlfile.close()        

def OBJoptimization(objfile):
    rfile=open(objfile,'r')
    objLines=rfile.readlines()
    rfile.close()

     #分别记录节点、法线、贴图坐标的最小值
    VNum_min=0
    VnNum_min=0
    VtNum_min=0

    #赋值
    for i in range(0,len(objLines)):
        if objLines[i].__str__()[0:2]=='f ':            
            fstrLines=objLines[i][:-1].strip().split(' ')[1]
                        
            VNum_min=float(fstrLines.split('/')[0])
            try:
                VnNum_min=float(fstrLines.split('/')[1])
            except:
                pass
            VtNum_min=float(fstrLines.split('/')[2])
            break

    for i in range(0,len(objLines)):
        if objLines[i].__str__()[0:2]=='f ':
            fstrLines=objLines[i][:-1].strip().split(' ')
           
            for k in range(1,len(fstrLines)):
                if float(fstrLines[k].split('/')[0])<VNum_min:
                    VNum_min=round(float(fstrLines[k].split('/')[0]))
                if fstrLines[k].split('/')[1]!="":
                    if float(fstrLines[k].split('/')[1])<VnNum_min:
                        VnNum_min=round(float(fstrLines[k].split('/')[1]))
                if float(fstrLines[k].split('/')[2])<VtNum_min:                    
                    VtNum_min=round(float(fstrLines[k].split('/')[2]))

    # 面值调整                
    for i in range(0,len(objLines)):
        if objLines[i].__str__()[0:2]=='f ':
            fstrLines=objLines[i][:-1].strip().split(' ')
            fstrx=''
            for k in range(1,len(fstrLines)):
                if fstrLines[k].split('/')[1]=="":
                    fstrLines[k]=str(int(round(float(fstrLines[k].split('/')[0]))-VNum_min+1.0))+'//'+str(int(round(float(fstrLines[k].split('/')[2]))-VtNum_min+1))
                else:
                    fstrLines[k]=str(int(round(float(fstrLines[k].split('/')[0]))-VNum_min+1.0))+'/'+str(int(round(float(fstrLines[k].split('/')[1]))-VnNum_min+1))+'/'+str(int(round(float(fstrLines[k].split('/')[2]))-VtNum_min+1))
                    
            for k in range(0,len(fstrLines)):
                fstrx+=fstrLines[k]+' '
            objLines[i]=fstrx[:-1]+'\n'

    wfile=open(objfile,'w')
    wfile.writelines(objLines)
    wfile.close()

def OBJSplit():
    #该参数处理用于输入的OBJ文件
   
    OBJFilePath=r'E:\_ESRI\0824 丝路视觉科技\c04_test_obj\c04_test_obj.obj'
    imagePath="E:\\_ESRI\\0824 丝路视觉科技\\c04_test_obj\\maps\\"  #贴图地址
    changeImgae(imagePath, "tga")

    imagaSFolder = os.path.abspath(os.path.join(imagePath, "../"))+"\\"
    print("xx"+imagaSFolder)
    DeswrlFolder = os.path.dirname(OBJFilePath)
    if exists(OBJFilePath[:-3]+'mtl'):
        mtlList=mtlChaifen(OBJFilePath[:-3]+'mtl',imagaSFolder)
        OBJChaiFen(OBJFilePath,DeswrlFolder,mtlList)
    else:
        OBJChaiFen(OBJFilePath,DeswrlFolder)

    #os.remove(OBJFilePath)

    
if __name__=='__main__':
    print('start')
    OBJSplit()
    print('finish')
    
