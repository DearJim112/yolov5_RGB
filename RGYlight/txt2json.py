
import os
import datetime
import json
import cv2


def txt2json(txtpath='./RGYlightpic/labels/train2',jsonpath="./task1 样例数据/label2/",imagepath="./task1/images/"):
# path = "./RGYlightpic/labels/train2" #文件夹目录
# path2= "./task1 样例数据/label2/" #文件夹目录
# pathimage="./task1/images/" #图片路径
    dic_rev={'0':'red','1':'green','2':'yellow','3':'other'}
    newdic={}
    files= os.listdir(txtpath) #得到文件夹下的所有文件名称
    for file in files: #遍历文件夹
         if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
              f = open(txtpath+"/"+file) #打开文件
              # print(file[:-4])
              newdic['info']={'data':datetime.datetime.now().strftime('%Y%m%d'),'image_name':file[:-3]+'jpg'}
              data = f.readlines()  #直接将文件中按行读到list里，效果与方法2一样
              f.close()
              img = cv2.imread(imagepath+file[:-3]+'jpg')  #读取图片信息
              annotationslist=[]
              for i in data:
                   # print(i)
                   xy=i.split(' ')
                   color=xy[0]
                   xc=float(xy[1])
                   yc=float(xy[2])
                   w=float(xy[3])
                   h=float(xy[4])
                   # print(xy[4])
                   annotationslist.append({"bbox":[round(xc*img.shape[1]),
                                                   round(yc*img.shape[0]),
                                                   round(w*img.shape[1]),
                                                   round(h*img.shape[0])],
                                           "color":dic_rev[color]})
              newdic['annotations']=annotationslist
              jsObj = json.dumps(newdic)
              jsonfile=jsonpath+'/'+file[:-3]+'json'
              fileObject = open(jsonfile, 'w')
              fileObject.write(jsObj)
              fileObject.close()
              # print(newdic)

def json2txt(txtpath='./RGYlightpic/labels/train2',jsonpath="./task1 样例数据/label2/",imagepath="./task1/images/"):

    dic={'red':'0','green':'1','yellow':'2','other':'3'}
    files= os.listdir(jsonpath) #得到文件夹下的所有文件名称
    for file in files: #遍历文件夹
         if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开
              f = open(jsonpath+"/"+file) #打开文件
              json_data = json.load(f)
              txtfile=txtpath+"/"+json_data['info']['image_name'][:-3]+'txt'
              img = cv2.imread(imagepath+json_data['info']['image_name'])  #读取图片信息
              # img2=cv2.imread(imagepath+json_data['info']['image_name'])
              # print(img2.shape)

              # print(size)
              with open(txtfile, 'w') as txtf:
                   txtf.write('')
                   for i in (json_data['annotations']):
                        xc=format(i['bbox'][0]/img.shape[1],".6f")
                        yc=format(i['bbox'][1]/img.shape[0],".6f")
                        w=format(i['bbox'][2]/img.shape[1],".6f")
                        h=format(i['bbox'][3]/img.shape[0],".6f")
                        bbox=dic[i['color']]+' '+str(xc)+' '+str(yc)+' '+str(w)+' '+str(h)+'\n'
                        # print(bbox)
                        txtf.writelines(bbox)


def main():
    pathimage="./task1/images/" #图片路径
    path = "./task1/labels" #文件夹目录 json label放的位置
    txtpath="./task1/label2" #保存到处的txt路径
    json2txt(txtpath, path, pathimage)
    # txt2json()

if __name__ == "__main__":
    main()