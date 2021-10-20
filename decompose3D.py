from wand.image import Image
import os, shutil
import sys,shutil
from wand.image import Image
import string

class DDDmax():
    def __init__(self, filePath, *imageDir) -> None:
        self.filePath = filePath
        self.imageDir = imageDir
        self.fileDir = os.path.dirname(filePath) + '/'
        self.fileName = os.path.basename(filePath)

    def decompose(self, targetDir, targetFormat, label):
        f = open(self.filePath, 'r', encoding='GBK')
        try:
            os.mkdir(targetDir)
        except:
            pass
        try:  
            os.mkdir(targetDir + '/' + 'TempMtl')
        except:
            pass

        newmtl = 'ImageTemp'
        countMtllib, countObj, countMtl, countV, countVn, countVt, countF, countO, countS, countG = 0,0,0,0,0,0,0,0,0,0
        for row in f:
            if 'mtllib' == row[0:6]:
                countMtllib += 1
                pass
            if '# object' == row[0:8]:
                countObj += 1
                targetObjName = row[10:-1]
                targetObjFile = open(targetDir + '/' + targetObjName + '.obj', 'w', encoding='utf-8')
                targetObjFile.write
                pass
            if "usemtl" == row[0:6]:
                countMtl += 1
                pass
            if 'v ' == row[0:2]:
                countV += 1
                pass
            if 'vn ' == row[0:3]:
                countVn += 1
                pass
            if 'vt ' == row[0:3]:
                countVt += 1
                pass
            if 'f ' == row[0:2]:
                countF += 1
                pass
            if 'o ' == row[0:2]:
                countO += 1
                pass
            if 's ' == row[0:2]:
                countS += 1
                pass
            if 'g ' == row[0:2]:
                countG += 1
                pass
        print(countMtllib, countObj, countMtl, countV, countVn, countVt, countF, countO, countS, countG)
        #     1            149       23014     893162  270966   1683622  743740  149     151706  149



    def convertImageFormat(self, imagePath, targetFormat, resultFile):
        with Image(filename=imagePath) as im:
            im.save()


if __name__ == "__main__":
    # obj文件路径
    obj_file = r'./SM_FSNH_QDH/qdh.obj'
    # obj文件贴图路径，图片应是全部在此文件夹，无二级文件夹
    imageDir = r'./obj/'
    # 拆分后存储路径，此路径下存储obj与mtl文件，并新建map文件夹存放所有贴图
    resultDir = r'./SM_FSNH_QDH/result'
    # 贴图转换的目标格式
    imageTargetFormat = 'jpg'
    # 对象区分标志
    label = '# object'

    testOBJ = DDDmax(obj_file, imageDir)
    testOBJ.decompose(resultDir, imageTargetFormat, label)