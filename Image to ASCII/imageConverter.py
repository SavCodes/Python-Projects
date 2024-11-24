import cv2

def map_brightness_to_ascii(brightness):
    color_map = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
    negative_color_map = color_map[::-1]
    interval = 255 / (len(color_map)-1)
    map_index = int(brightness // interval)
    new_text = negative_color_map[map_index]
    if new_text == "$":
        new_text = " "
    return new_text

def load_image_and_convert():
    image = cv2.imread('img.png', cv2.IMREAD_GRAYSCALE)
    resized_image = cv2.resize(image, (100, 100))
    full_ascii = ""
    for row in resized_image:
        for pixel in row:
            ascii_character = map_brightness_to_ascii(pixel)
            full_ascii += ascii_character
        full_ascii += "\n"
    cv2.imshow("Original Image: ", image)
    print(full_ascii)
    cv2.waitKey(0)


if __name__ == "__main__":
    load_and_convert_image()
