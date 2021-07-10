# DataAugmentationForChineseByCCL
Data Augmentation For Chinese Character   Recognition By Using Connected-Component  Labeling Algorithm

本文提供另類的中文字擴增法，透過連通法找出中文字分離的部位再各自進行縮放、位移來擴充中文資料。
(文中連通法演算法修改自https://github.com/spwhitt/cclabel)

![Image](https://github.com/yuanshinNCHU/DataAugmentationForChineseByCCL/blob/main/%E4%B9%83_CCL%E7%A4%BA%E6%84%8F%E5%9C%96_%E4%BF%AE%E6%94%B9.png)


![iMAGE](https://github.com/yuanshinNCHU/DataAugmentationForChineseByCCL/blob/main/%E4%B9%83_Simple%E7%A4%BA%E6%84%8F%E5%9C%96_%E4%BF%AE%E6%94%B9.png)

見下圖，比較普通擴增方式(Normal)、連通擴增方式(CCL)擴增資料的平均圖，可以看出連通擴增法的變動較小重複的部位較多，使得在重複的地方較為清晰(銳化)。

![iMAGE](https://github.com/yuanshinNCHU/DataAugmentationForChineseByCCL/blob/main/%E6%93%B4%E5%85%85%E8%B3%87%E6%96%99%E5%B9%B3%E5%9D%87.png)
