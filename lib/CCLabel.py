# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:40:23 2021
@author: rodger
"""

from PIL import Image, ImageDraw
#import Image, ImageDraw

import sys
import math, random
from itertools import product
from ufarray import *

class CCLabel:

    def __init__(self, imgUrl):
        self._imgUrl = imgUrl
        self._labels = None
        self._output_img = None

        # print('CCLabel')
        img = Image.open(imgUrl)
        # Threshold the image, this implementation is designed to process b+w
        # images only
        img = img.point(lambda p: p > 190 and 255)
        img = img.convert('1')
        # labels is a dictionary of the connected component data in the form:
        #     (x_coordinate, y_coordinate) : component_id
        #
        # if you plan on processing the component data, this is probably what you
        # will want to use
        #
        # output_image is just a frivolous way to visualize the components.
        (self._labels, self.partImgs, self._output_img) = self.run(img)
        # print(len(self._output_img1))
        # output_img.save('output_img.jpg')
        # output_img.show()
    
    def saveColor(self, name):
        if len(self.partImgs) == 1:
            return
        self._output_img.save('%s.png'%(name))

    def hasParts(self):
        if len(self.partImgs) > 1:
            return True
        else:
            return False

    def save(self, name):
        if len(self.partImgs) == 1:
            return
        
        # self._output_img.save('%s.png'%(name))
        
        # img = Image.new('L', (50, 50), 255)
        for i in range(len(self.partImgs)):
            self.partImgs[i].save('%s_%i.png'%(name, i))

    # 針對各部件縮放
    def getAugmentedImgs(self):
        
        imgsC = []
        posesC = []        
        for i in range(len(self.partImgs)):
            c = self.getCoreCrop(self.partImgs[i])
            imgsC.append(self.partImgs[i].crop(c))
            posesC.append(c)

        imgS = [[] for _ in range(len(imgsC))]
        posesS = [[] for _ in range(len(imgsC))]

        print(len(imgsC))
        # 如果只有一個部件則回傳原圖
        if len(imgsC) == 1:
          return None
          # return Image.open(self._imgUrl)

        for i in range(len(imgsC)):
            # print('i=%i,len1=%i,len2=%i'%(i, len(imgsC), len(posesS)))
            imgs, poses = self.getTrans(imgsC[i], posesC[i])
            imgS[i] = imgs
            posesS[i] = poses
        
        idxLists = self.getCombIDList(imgS)
        print(len(idxLists))
        idxLists_limit = idxLists
        if len(idxLists) > 2:
            random.shuffle(idxLists)
            idxLists_limit = idxLists[:5]
        retImgs = self.getImgsByIDLists(idxLists_limit, imgS, posesS)
        return retImgs      

    def getCoreCrop(self, img):
           
        outdata = img.load()
        minx = 50
        maxx = 0
        miny = 50
        maxy = 0
        for x in range(50):
            for y in range(50):
                if outdata[x,y] < 200:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        return (minx, miny, maxx + 1, maxy +1)

    def getTrans(self, img, crop):

        imgMove, posesMove = self.getSimpleMoves(img, crop)
        imgsScale = []
        posesScale = []
        for i in range(len(imgMove)):
            imgs, poses = self.getSimpleScales(imgMove[i], posesMove[i])
            imgsScale = imgsScale + imgs
            posesScale = posesScale + poses
        return imgsScale, posesScale

    def getSimpleMoves(self, img, crop):
        lx = crop[0]
        ly = crop[1]
        rx = crop[2]
        ry = crop[3]
        x = []
        y = []
        imgs = []
        poses = []
        if lx == 0:
          x = [2, 3]
        elif rx == 51:
          x = [-2, -3]
        else:
            if random.randint(0,1) == 1:
                x = [-1, -2]
            else:
                x = [1, 2]
        if ly == 0:
          y = [2, 1, 0]
        elif ry == 51:
          y = [-2, -1, 0]
        else:
            if random.randint(0,1) == 1:
                y = [-1, -2]
            else:
                y = [1, 2]
        # x = [0]
        # y = [0]
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              lx = crop[0] + i
              ly = crop[1] + j
              rx = crop[2] + i
              ry = crop[3] + j
              imgs.append(img)
              poses.append((lx, ly, rx, ry))
        return imgs, poses   

    def getSimpleScales(self, img, crop):
        
        imgs = []
        poses = []
        x = []
        y = []
        w = crop[2] - crop[0]
        h = crop[3] - crop[1]
        if w == 1:
            x = [0,1,2]
        else:
            x = [-2,0,2]
        if h == 1:
            y = [0,2,3]
        else:
            y = [-2,0,2]
        
        # x = [0]
        # y = [0]
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              nMaxx = crop[2] + i
              nMaxy = crop[3] + j
              w = nMaxx - crop[0]
              h = nMaxy - crop[1]
              if w == 0 or h == 0:
                  continue
              imgs.append(img.resize((w, h)))
              poses.append((crop[0], crop[1], nMaxx, nMaxy))
        return imgs, poses
    # 回傳所有位移組合
    def getMoves(self, img, crop):
        lx = crop[0]
        ly = crop[1]
        rx = crop[2]
        ry = crop[3]
        x = []
        y = []
        imgs = []
        poses = []
        if lx == 0:
          for _ in range(0,3,1):
            x.append(_)
        elif rx == 51:
          for _ in range(-2,1,1):
            x.append(_)
        else:
          for _ in range(-1,2,1):
            x.append(_)
        if ly == 0:
          for _ in range(0,3,1):
            y.append(_)
        elif ry == 51:
          for _ in range(-2,1,1):
            y.append(_)
        else:
          for _ in range(-1,2,1):
            y.append(_)
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              lx = crop[0] + i
              ly = crop[1] + j
              rx = crop[2] + i
              ry = crop[3] + j
              imgs.append(img)
              poses.append((lx, ly, rx, ry))
        return imgs, poses            

    # 回傳所有縮放組合
    def getScales(self, img, crop):
        imgs = []
        poses = []
        x = []
        y = []
        w = crop[2] - crop[0]
        h = crop[3] - crop[1]
        if w == 1:
            for _ in range(0,3,1):
                x.append(_)
        else:            
            for _ in range(-1,2,1):
                x.append(_)
        if h == 1:
            for _ in range(0,3,1):
                y.append(_)
        else:
            for _ in range(-1,2,1):
                y.append(_)
        for i in x:
            for j in y:
              if i == 0 and y == 0:
                continue
              nMaxx = crop[2] + i
              nMaxy = crop[3] + j
              w = nMaxx - crop[0]
              h = nMaxy - crop[1]
              imgs.append(img.resize((w, h)))
              poses.append((crop[0], crop[1], nMaxx, nMaxy))
        return imgs, poses

    def combinationsList(self, list1, list2):
        comb = []
        for i in list1:
            for j in list2:
                #print('%i %i'%(i, j))
                temp = []
                if type(i) == list:
                    temp = i.copy()
                else:
                    temp.append(i)
                temp.append(j)
                comb.append(temp)
                if len(comb) >= 120:
                    return comb
        return comb

    def getCombIDList(self, lists):
        
        idxLists = self.getIndexList(lists)
        length = len(lists)
        if length == 2:
            return self.combinationsList(idxLists[0], idxLists[1])
        elif length > 2:
            comb = idxLists[0]
            for i in range(1, len(idxLists)):
                comb = self.combinationsList(comb, idxLists[i])
            return comb
        else:
            print('len is 1')
            return idxLists

    def getImgsByIDLists(self, idLists, pImgs, pPoses):
        imgs = []
        for i in range(len(idLists)):
            img = Image.new('L', (50, 50), 255)
            for j in range(len(idLists[i])):
              if type(idLists[i][j]) != int:
                print(idLists[i][j])              
              img.paste(pImgs[j][idLists[i][j]], pPoses[j][idLists[i][j]])
            imgs.append(img)
            # imgs.append(self.centerized(img))
        return imgs

    def centerized(self, img):
        
        data = img.load()
        w, h = img.size
        minx = 50
        miny = 50
        maxx = 0
        maxy = 0
        # cnt = 0
        for x in range(w):
            for y in range(h):
                if data[x, y] < 220:
                    # cnt = cnt + 1
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
        # if cnt == 0:
        #     print('empty')
        #     return
        w = maxx - minx
        h = maxy - miny
        # img.save('%s_%i_%i.png'%(name, w, h))

        posx = int(25 - (w / 2))
        posy = int(25 - (h / 2))
        temp = img.crop((minx, miny, maxx + 1, maxy + 1))
        imgNew =  Image.new('L', (50, 50), 255)
        imgNew.paste(temp, (posx,posy))
        return imgNew

    # 回傳idx 陣列
    # ex [img1, img2, img3] = [0, 1, 2]
    def getIndexList(self, lists):
        rets = [[] for _ in range(len(lists))]
        for i in range(len(lists)):
            idx = 0
            for j in range(len(lists[i])):
                rets[i].append(idx)
                idx = idx + 1
        return rets
        
    def getCropImgs(self):
        imgs = []
        poss = []
        img = Image.open(self._imgUrl)
        group = self.getGroup(self._labels)
        for key in group:
            # print(key)
            c = self.getCrop(group[key])
            temp = img.crop(c)
            imgs.append(temp)
            # poss.append((c[0], c[1]))
            poss.append(c)
        return imgs, poss

    def getCrop(self, list):
        tempX = []
        tempY = []
        for i in range(len(list)):
            tempX.append(list[i][0])  
            tempY.append(list[i][1])  
        minx = min(tempX)
        maxx = max(tempX)
        miny = min(tempY)
        maxy = max(tempY)
        # print('minx=%i miny=%i maxx=%i maxy=%i'%(minx, miny, maxx, maxy))
        return (minx, miny, maxx + 1, maxy + 1)

    def run(self, img):
        data = img.load()
        width, height = img.size
    
        # Union find data structure
        uf = UFarray()
    
        #
        # First pass
        #    
        labels = {}
        for y, x in product(range(height), range(width)):
            if data[x, y] == 255:
                pass
            elif y > 0 and data[x, y-1] == 0:
                # print('x:%i,y:%i'%(x,y))
                labels[x, y] = labels[(x, y-1)]
            elif x+1 < width and y > 0 and data[x+1, y-1] == 0:    
                c = labels[(x+1, y-1)]
                labels[x, y] = c
                if x > 0 and data[x-1, y-1] == 0:
                    a = labels[(x-1, y-1)]
                    uf.union(c, a)
                elif x > 0 and data[x-1, y] == 0:
                    d = labels[(x-1, y)]
                    uf.union(c, d)
            elif x > 0 and y > 0 and data[x-1, y-1] == 0:
                labels[x, y] = labels[(x-1, y-1)]
            elif x > 0 and data[x-1, y] == 0:
                labels[x, y] = labels[(x-1, y)]
            else: 
                labels[x, y] = uf.makeLabel()
        
        #
        # Second pass
        #    
        uf.flatten()    
        colors = {}
        output_img = Image.new("RGB", (width, height))
        outdata = output_img.load()

        idxMap = []
        imgs = []
        imgDatas = []
        cnt = 0
        for (x, y) in labels:
            cnt = cnt + 1
            # print(labels[(x, y)])
            component = uf.find(labels[(x, y)])
            # print('label:%i,component=%i'%(labels[(x, y)], component))
            labels[(x, y)] = component    
            if component not in colors:
                img = Image.new('L', (50, 50), 255)
                imgs.append(img)
                imgDatas.append(img.load())
                idxMap.append(component)
                colors[component] = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
                # colors[component] = self.getColor(component)

            # outdata[x, y] = colors[component]
            idx = idxMap.index(component)
            outdata[x, y] = self.getColor(idx)
            imgDatas[idx][(x,y)] = data[(x,y)]
            # print(data[(x,y)])
        # print(cnt)
        return (labels, imgs, output_img)
    
    def getColor(self, idx):
        colors = [
            (64, 0,0), (128, 0,0), (192, 0,0), (255, 0,0),
            (64, 64,0), (128, 64,0), (192, 64,0), (255, 64,0),
            (64, 128,0), (128, 128,0), (192, 128,0), (255, 128,0),
            (64, 192,0), (128, 192,0), (192, 192,0), (255, 192,0),
            (64, 255,0), (255, 192,0), (192, 255,0), (255, 255,0),
            (64, 64, 64), (128, 64, 64), (192, 64, 64), (255, 64, 64),
            (64, 128, 64), (128, 128, 64), (192, 128, 64), (255, 128, 64),        
        ]
        return colors[idx]