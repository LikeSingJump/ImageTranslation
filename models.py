# 导入mmcv和mmgeneration
# import mmcv
from mmgen.apis import init_model, sample_img2img_model
# 导入 opencv
import cv2
# 导入numpy和matplotlib
import numpy as np
import matplotlib.pyplot as plt


# 定义可视化图像函数，输入图像路径，可视化图像
def show_img_from_path(img_path):
    '''opencv 读入图像，matplotlib 可视化格式为 RGB，因此需将 BGR 转 RGB，最后可视化出来'''
    img = cv2.imread(img_path)
    img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img_RGB)
    plt.show()


# 梵高
model_vangogh = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_vangogh2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_vangogh2photo/ckpt/cyclegan_vangogh2photo/latest.pth',
    device='cuda:0'
)

# 莫奈
model_monet = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_monet2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_monet2photo/ckpt/cyclegan_monet2photo/latest.pth',
    device='cuda:0'
)

# 塞尚
model_cezanne = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_cezanne2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_cezanne2photo/ckpt/cyclegan_cezanne2photo/latest.pth',
    device='cuda:0'
)

# 浮世绘
model_ukiyoe = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_ukiyoe2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_ukiyoe2photo/ckpt/cyclegan_ukiyoe2photo/latest.pth',
    device='cuda:0'
)

# 建筑外立面
model_facades = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_facades_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_facades/latest.pth',
    device='cuda:0'
)

# 野马斑马
model_horse2zebra = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_horse2zebra_b1x1_270k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_horse2zebra/latest.pth',
    device='cuda:0'
)

# 冬天夏天
model_summer2winter = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_summer2winter_b1x1_250k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_summer2winter/latest.pth',
    device='cuda:0'
)

model_iphone2dslr_flower = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_iphone2dslr_flower_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_iphone2dslr_flower/ckpt/cyclegan_iphone2dslr_flower/latest.pth',
    device='cuda:0'
)

model_hayao2photo = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_hayao2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_hayao2photo/ckpt/cyclegan_hayao2photo/latest.pth',
    device='cuda:0'
)

model_shinkai2photo = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_shinkai2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_shinkai2photo/ckpt/cyclegan_shinkai2photo/latest.pth',
    device='cuda:0'
)

model_summerwar2photo = init_model(
    'mmgeneration/configs/cyclegan/cyclegan_lsgan_resnet_in_summerwar2photo_b1x1_80k.py',
    'mmgeneration/work_dirs/experiments/cyclegan_summerwar2photo/ckpt/cyclegan_summerwar2photo/latest.pth',
    device='cuda:0'
)


models = {
    'vangogh': model_vangogh,
    'monet': model_monet,
    'cezanne': model_cezanne,
    'ukiyoe': model_ukiyoe,
    'mask': model_facades,
    'horse': model_horse2zebra,
    'zebra': model_horse2zebra,
    'summer': model_summer2winter,
    'winter': model_summer2winter,
    'dslr_flower': model_iphone2dslr_flower,
    'hayao': model_hayao2photo,
    'shinkai': model_shinkai2photo,
    'summerwar': model_summerwar2photo,
}
# models = {
#     'vangogh': model_vangogh,
#     'monet': model_monet,
#     'cezanne': model_cezanne,
#     'ukiyoe': model_ukiyoe,
# }

image_styles = models.keys()


def show_styles(input_path, models, figsize=15, save_path=False, title=True):
    # 读入输入图像，获取高宽尺寸
    input_img = cv2.imread(input_path)

    num_styles = len(models)

    plt.figure(figsize=(figsize, figsize))
    # 展示原始输入图像
    plt.subplot(1, num_styles + 1, 1)
    if title:
        plt.title('input')
    input_RGB = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(input_RGB)

    for i, target_domain in enumerate(models):

        # 生成迁移图像，注意 target_domain 要设置正确
        fake_imgs = sample_img2img_model(models[target_domain], input_path, target_domain=target_domain)

        # 获取生成图像尺寸
        img_size = fake_imgs.shape[2]

        # 分别抽取RGB三通道图像，归一化为0-255的uint8自然图像
        RGB = np.zeros((img_size, img_size, 3))
        RGB[:, :, 0] = fake_imgs[0][2]
        RGB[:, :, 1] = fake_imgs[0][1]
        RGB[:, :, 2] = fake_imgs[0][0]
        # 将生成图转为输入图像大小
        RGB = cv2.resize(RGB, dsize=(input_img.shape[1], input_img.shape[0]))
        # 像素值归一化
        RGB = 255 * (RGB - RGB.min()) / (RGB.max() - RGB.min())
        # 像素值转为整数
        RGB = RGB.astype('uint8')

        if save_path:
            # 导出生成的图像文件
            cv2.imwrite('mmgeneration/outputs/F5_photo2{}.jpg'.format(target_domain), cv2.cvtColor(RGB, cv2.COLOR_BGR2RGB))

        # 展示生成图
        plt.subplot(1, num_styles + 1, i + 2)
        if title:
            plt.title(target_domain)
        plt.xticks([])
        plt.yticks([])
        plt.imshow(RGB)

    # 自动调节子图间距
    plt.tight_layout()
    plt.show()


# show_styles('mmgeneration/data/memory/memory_san.jpg', models, figsize=25, save_path=False, title=True)