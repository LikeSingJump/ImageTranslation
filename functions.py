# 导入mmcv和mmgeneration
from models import *
from tqdm import tqdm
from mmgen.apis import init_model, sample_img2img_model
# 导入 opencv
import cv2
# 导入numpy和matplotlib
import numpy as np
import matplotlib.pyplot as plt


def gen_vis_fake_img(input_path, model, target_domain='vangogh', figsize=15, save_path='mmgeneration/outputs/imageSave.jpg'):
    # 读入输入图像，获取高宽尺寸
    input_img = cv2.imread(input_path)
    # 生成图像，注意 target_domain 要设置正确
    fake_imgs = sample_img2img_model(model, input_path, target_domain=target_domain)
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
        cv2.imwrite(save_path, cv2.cvtColor(RGB, cv2.COLOR_BGR2RGB))

    plt.figure(figsize=(figsize, figsize))
    # 展示原始输入图像
    plt.subplot(1, 2, 1)
    plt.title('input')
    input_RGB = cv2.cvtColor(input_img, cv2.COLOR_BGR2RGB)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(input_RGB)

    # 展示生成图
    plt.subplot(1, 2, 2)
    plt.title(target_domain)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(RGB)

    plt.show()


# 处理单帧
def process_frame(img, target_domain):
    # 临时将本帧图像导出为图片文件
    cv2.imwrite('mmgeneration/outputs/video_temp/frame_temp.jpg', img)

    # 生成梵高油画，注意 target_domain 要设置正确
    fake_imgs = sample_img2img_model(models[target_domain], 'mmgeneration/outputs/video_temp/frame_temp.jpg', target_domain)
    # 获取生成图像尺寸
    img_size = fake_imgs.shape[2]

    # 分别抽取RGB三通道图像，归一化为0-255的uint8自然图像
    RGB = np.zeros((img_size, img_size, 3))
    RGB[:, :, 0] = fake_imgs[0][2]
    RGB[:, :, 1] = fake_imgs[0][1]
    RGB[:, :, 2] = fake_imgs[0][0]
    # 将生成图转为输入图像大小
    RGB = cv2.resize(RGB, dsize=(img.shape[1], img.shape[0]))
    # 像素值归一化
    RGB = 255 * (RGB - RGB.min()) / (RGB.max() - RGB.min())
    # 像素值转为整数
    RGB = RGB.astype('uint8')

    # 蓝绿通道调换
    RGB = cv2.cvtColor(RGB, cv2.COLOR_BGR2RGB)

    return RGB

# 视频逐帧处理
def generate_video(input_path='mmgeneration/data/memory/tongji_video.mp4', output_path='mmgeneration/data/output.mp4', target_domain='vangogh'):
    print('视频开始处理', input_path)

    # 获取视频总帧数
    cap = cv2.VideoCapture(input_path)
    frame_count = 0
    while (cap.isOpened()):
        success, frame = cap.read()
        frame_count += 1
        if not success:
            break
    cap.release()
    print('视频总帧数为', frame_count)

    cap = cv2.VideoCapture(input_path)
    frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (int(frame_size[0]), int(frame_size[1])))

    # 进度条绑定视频总帧数
    with tqdm(total=frame_count - 1) as pbar:
        try:
            while (cap.isOpened()):
                success, frame = cap.read()
                if not success:
                    break

                # 处理帧
                try:
                    frame = process_frame(frame, target_domain)
                except Exception as e:
                    print(e)
                    pass

                if success == True:
                    out.write(frame)

                    # 进度条更新一帧
                    pbar.update(1)

        except:
            print('中途中断')
            pass

    cv2.destroyAllWindows()
    out.release()
    cap.release()
    print('视频已保存', output_path)