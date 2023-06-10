from functions import *
import time


def time_format():
    return str(time.strftime("%Y%m%d%H%M%S", time.localtime()))


style = "summerwar"
gen_vis_fake_img('./mmgeneration/data/memory/winter.jpg', models[style], target_domain=style, figsize=5, save_path='mmgeneration/outputs/'+style+time_format()+'.jpg')


# # 对文件夹中的每一张图像运行画作风格迁移
# photo_path = 'mmgeneration/data/memory'
#
# os.chdir(photo_path)
# for each in os.listdir():
#     try:
#         gen_vis_fake_img(each, model, target_domain='vangogh', figsize=8)
#     except:
#         pass
# os.chdir('../../')



# generate_video(input_path='mmgeneration/data/memory/tongji_video.mp4', output_path=f"mmgeneration/outputs/photo2{style}_video{time_format()}.mp4", target_domain=style)
# show_styles('./mmgeneration/data/memory/test1.jpg', models, figsize=25, save_path=False, title=True)

# 循环展示图片
# while True:
#     # 用户输入要展示的风格
#     style = input('请输入要展示的风格（{}）：'.format(', '.join(image_styles)))
#     # 判断输入的风格是否可用
#     if style not in image_styles:
#         print('输入的风格不可用，请重新输入！')
#         continue
#     # 加载并展示图片
#     try:
#         gen_vis_fake_img('mmgeneration/data/memory/test2.jpg', models[style], target_domain=style, figsize=5, save_path='mmgeneration/outputs/'+style+'.jpg')
#     except Exception as e:
#         print('展示图片时发生错误：{}'.format(str(e)))
#     # 等待2秒
#     time.sleep(2)