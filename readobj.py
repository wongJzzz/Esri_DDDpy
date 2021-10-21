import os,shutil
from PIL import Image


class D3OBJ():
    def __init__(self, filePath):
        self.filePath = filePath
        self.fileDir = os.path.dirname(filePath) + '/'
        self.fileName = os.path.basename(filePath)

    def decomposeByO(self, targetDir, imageFormat):
        """
        :param targetDir: 存分割后obj、mtl、贴图的路径
        :param imageFormat: 题图格式转换目标 'jpg'或'png'
        :按照O标签分割obj模型，每个结果obj对应对应一个mtl，有贴图还对应一个文件夹
        :obj、mtl、贴图文件夹名称一样
        :其中会转贴图格式，如果不是jpg、png就会转换成imageForamt指定的 'jpg'或'png'
        """
        f = open(self.filePath, "r", encoding='utf-8')
        try:  
            os.mkdir(targetDir)
        except:
            pass
        Context_mtllib = ''
        v_list, vn_list, vt_list, f_list = [], [], [], []
        len_v, len_vn, len_vt = 0, 0, 0
        obj_count = 0
        targetObjFile = self.fileName
        targetObjName = self.fileName
        # targetMtlFIle = self.fileName.replace('.obj', '.mtl')
        for row in f:
            if 'mtllib' == row[0:6]:  
                Context_mtllib = row
                print(self.fileDir + Context_mtllib[7:-1])
                print(targetDir + '/' + Context_mtllib[7:-1])
                self.decomposeMTL(Context_mtllib[7:-1], targetDir, imageFormat)
                # shutil.copy(self.fileDir + Context_mtllib[7:-1], targetDir + '/' + Context_mtllib[7:-1])
            if 'usemtl' == row[0:6]:
                targetObjFile.write(row)
                # targetMtlFile = open(targetDir + '/' + targetObjName + '.mtl', 'w', encoding='utf-8')
                self.copyMtlTree(row[7:].rstrip('\n'),targetDir,targetObjName)
            if '# object' == row[0:8]:
                targetObjName = row[2:-1]
                try:
                    for line in v_list:
                        targetObjFile.write(line + '\n')
                    for line in vn_list:
                        targetObjFile.write(line + '\n')
                    for line in vt_list:
                        targetObjFile.write(line + '\n')
                    for line in f_list:
                        targetObjFile.write(line + '\n')
                except:
                    pass
                targetObjFile = open(targetDir + '/' + targetObjName + '.obj', 'w', encoding='utf-8')
                # targetObjFile.write(Context_mtllib)
                targetObjFile.write('mtllib '+targetObjName+'.mtl\n')
                len_v += len(v_list)
                len_vn += len(vn_list)
                len_vt += len(vt_list)
                v_list, vn_list, vt_list, f_list = [], [], [], []
                obj_count += 1
            if 'v ' == row[0:2]:
                v_list.append(row[:-1])
            elif 'vn' == row[0:2]:
                vn_list.append(row[:-1])
            elif 'vt' == row[0:2]:
                vt_list.append(row[:-1])
            if 'f' == row[0:1]:
                vnts = [item.split('/') for item in row[2:-2].split(' ')]
                f_row = 'f '
                for vnt in vnts:
                    vnt[0] = str(int(vnt[0]) - len_v)
                    vnt[1] = int(vnt[1]) - len_vt if vnt[1] != '' else vnt[1]
                    vnt[2] = int(vnt[2]) - len_vn if vnt[2] != '' else vnt[2]
                    f_row += str(vnt[0]) + '/' + str(vnt[1]) + '/' + str(vnt[2]) + ' '
                f_row += ' '
                f_list.append(f_row)
        print(obj_count)
        shutil.rmtree(targetDir+'/TempMtl')


    def convertImageFormat(self, resultFile, targetFormat, imagePath):
        """
        :param resultFile: 转后后文件路径
        :param targetFormat: 题图格式转换目标 'jpg'或'png'
        :param imagePath: 图片路径
        :转贴图格式
        """
        im = Image.open(imagePath)
        if 'jpg' == targetFormat:
            imNew = im.convert('RGB')
            imNew.save(resultFile)
        if 'png' == targetFormat:
            imNew = im.convert('RGBA')
            imNew.save(resultFile)

    def decomposeMTL(self, mtlName, targetDir, targetFormat):
        """
        按照newmtl分割mtl文件，并将贴图存入相应文件夹
        mtl和贴图文件存在目标路径的TempMtl文件夹，再decomposeByO结尾会删除这个文件夹
        """
        try:  
            os.mkdir(targetDir)
        except:
            pass
        try:  
            os.mkdir(targetDir + '/' + 'TempMtl')
        except:
            pass
        f = open(self.fileDir + '/' + mtlName, 'r', encoding='utf-8' )
        newmtl = 'ImageTemp'
        count = 0
        for row in f:
            if 'newmtl' == row[:6]:  # obj指定了mtl文件，先按newmtl分割生成临时的分割结果
                count = 0            # 后面根据分割的obj来拷贝相应的mtl，最后再删除临时的
                newmtl = row[7:-1]
                f_new = open(targetDir + '/' + 'TempMtl/' + row[7:-1] + '.mtl', 'w', encoding='utf-8')
            if 'map_' in row:     # mtl文件指定了题图，这里修改贴图格式，和修改路径名称
                count += 1
                try:  
                    os.mkdir(targetDir + '/' + 'TempMtl/' + newmtl)
                except:
                    pass
                imagePath = row.split(' ')[-1].rstrip('\n')
                targetFormat = targetFormat if os.path.splitext(imagePath)[-1][1:] not in ('jpg', 'jpeg', 'png') else os.path.splitext(imagePath)[-1][1:]
                resultFile = '{}/TempMtl/{}/image_{}.{}'.format(targetDir, newmtl, count, targetFormat)
                # print(imagePath)
                # print(resultFile)
                # image = MtlPic(imagePath)
                if os.path.splitext(imagePath)[-1][1:] not in ('jpg', 'jpeg'):
                    self.convertImageFormat(resultFile, targetFormat, imagePath)
                else:
                    shutil.copy(imagePath, resultFile)
                # print(row)
                row = row.replace(imagePath, resultFile)
                # print(row)
            f_new.write(row)
        
    
    def copyMtlTree(self, mtlName, targetDir, targetObjName):
        """
        :分割完mtl文件后，按照obj文件信息拷贝相应的mtl和贴图文件夹
        """
        mtlP = targetDir+'/TempMtl/'+mtlName
        tarP = targetDir+'/'+targetObjName
        if not os.path.exists(mtlP):
            shutil.copy(mtlP+'.mtl', tarP+'.mtl')
        else:
            with open(mtlP+'.mtl', 'r', encoding='utf-8') as f, open(tarP+'.mtl', 'w', encoding='utf-8') as f_tar:
                for row in f:
                    if 'map_' in row:
                        row = row.replace('/TempMtl/{}/'.format(mtlName), '/{}/'.format(targetObjName))
                    # print(row)
                    f_tar.write(row)
            shutil.copytree(mtlP, tarP)


if __name__ == "__main__":
    obj_file = r"D:\Code\Esri_DDDpy\Data\c04_vray_obj1_osg\tets.obj"
    resultDir = r"D:\#_ESRI\\temp\\out\\"
    testOBJ = D3OBJ(obj_file)
    testOBJ.decomposeByO(resultDir, 'jpg')