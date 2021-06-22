import os
from ocr import ocr
import time
import shutil
import numpy as np
from PIL import Image
from glob import glob


def single_pic_proc(image_file):
    image = np.array(Image.open(image_file).convert('RGB'))
    result, image_framed, image_char_rate = ocr(image)
    return result, image_framed, image_char_rate


if __name__ == '__main__':
    image_files = glob('./test_images/*.*')
    result_dir = './test_result'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)
    result_csv = 'result.csv'

    csv_f = open(os.path.join(result_dir, result_csv), 'w')

    for image_file in sorted(image_files):
        t = time.time()
        result, image_framed, image_char_rate = single_pic_proc(image_file)
        output_file = os.path.join(result_dir, image_file.split('/')[-1])
        file_name = image_file.split('/')[-1].split('.')[0]
        txt_file = os.path.join(result_dir, file_name + '.txt')
        print(txt_file)
        txt_f = open(txt_file, 'w')
        Image.fromarray(image_framed).save(output_file)
        print("Mission complete, it took {:.3f}s".format(time.time() - t))
        print("\nRecognition Result:\n")
        for key in result:
            print(result[key][1])
            txt_f.write(result[key][1]+'\n')
        txt_f.close()
        csv_f.write(file_name + ',' + image_char_rate + '\n')
    csv_f.close()