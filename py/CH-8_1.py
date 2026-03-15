import cv2
import numpy as np


def blur_outside_region(image_path, x1, y1, x2, y2, output_path='output.jpg', blur_strength=(20, 20)):
    """
    将指定区域外的图像区域模糊化

    Args:
        image_path: 输入图像路径
        x1, y1: 区域左上角坐标
        x2, y2: 区域右下角坐标
        output_path: 输出图像路径
        blur_strength: 模糊强度，数值越大越模糊
    """
    # 读取图像
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return

    height, width = img.shape[:2]

    # 确保坐标在图像范围内
    x1, x2 = max(0, min(x1, width)), max(0, min(x2, width))
    y1, y2 = max(0, min(y1, height)), max(0, min(y2, height))

    # 创建原始图像的副本
    result = img.copy()

    # 对整个图像进行模糊处理
    blurred = cv2.GaussianBlur(img, blur_strength, 0)

    # 创建掩码，白色部分保留原始图像
    mask = np.zeros((height, width), dtype=np.uint8)
    cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)

    # 将模糊图像和原始图像合并
    result = np.where(mask[:, :, np.newaxis] == 255, img, blurred)

    # 可选：在区域周围添加边框
    cv2.rectangle(result, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色边框

    # 保存结果
    cv2.imwrite(output_path, result)
    print(f"处理完成，结果已保存到: {output_path}")

    # 显示结果（可选）
    cv2.imshow('Result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result


# 使用示例
if __name__ == "__main__":
    # 定义关注区域坐标
    x1, y1 = 408, 91  # 左上角
    x2, y2 = 575, 226  # 右下角

    # 处理图像
    blur_outside_region(
        image_path='1.png',
        x1=x1, y1=y1,
        x2=x2, y2=y2,
        output_path='1_blurred.jpg',
        blur_strength=(25, 25)  # 模糊强度，可以调整
    )