
import os
import sys
sys.path.insert(1, './lib')
from CCLabel import CCLabel
from DataLoader import DataLoader

# get all paths from the path
dataLoader = DataLoader('res/')
picts = dataLoader.getData()

newRoot = 'augmented/'
cnt = 0
for key in picts:
  for pathPic in picts[key]:
    cclabel = CCLabel(pathPic)
    imgs = cclabel.getAugmentedImgs()
    if imgs is not None:
      lens = len(imgs)
      for i in range(lens):
        imgs[i].save('%s%s_%i_%i.png'%(newRoot, key, cnt, i))
    else:
        print(pathPic + ' is None')
    cnt = cnt + 1