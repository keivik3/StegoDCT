from itertools import product

from PIL import Image
import math



def bin_check(orig, new):
    cnt, mis = 0, 0
    for i in range(min(len(orig), len(new))):
        for j in range(min(len(orig[i]), len(new[i]))):
            if orig[i][j] != new[i][j]:
                mis += 1
            cnt += 1
    return [cnt, mis]

def BER(orig, new):
    cnt, mis = 0, 0
    for i in range(min(len(orig), len(new))):
        for j in range(min(len(orig[i]), len(new[i]))):
            if orig[i][j] != new[i][j]:
                mis += 1
            cnt += 1
    ber = mis / cnt
    return ber

def prepare(image):
    ans = []
    for i in range(image.size[0]):
        temp = []
        for j in range(image.size[1]):
            temp.append(image.getpixel((j, i))[0] - 128)
        ans.append(temp)
    return ans


def bin_prepare(image):
    ans = []
    for i in range(image.size[0]):
        temp = []
        for j in range(image.size[1]):
            if image.getpixel((j, i))[0] == 0:
                temp.append(1)
            else:
                temp.append(0)
        ans.append(temp)

    return ans


def photo(image, new):

    for i in range(len(new)):
        for j in range(len(new[0]) - 8):
            temp = image.getpixel((j, i))
            image.putpixel((j, i), (new[i][j] + 128, temp[1], temp[2]))
    image.save("result.png")


def bin_photo(binary, orig):
    key_size = len(binary)
    extract_key = Image.new("RGB", (key_size, key_size), color=(255, 255, 255))
    for i in range(len(binary)):
        for j in range(len(binary[i])):
            if binary[i][j] == 1:
                extract_key.putpixel((j, i), (0, 0, 0))
    extract_key.save("extract_key.png")
    stat = bin_check(bin_prepare(orig), binary)
    return stat


def zigzag_easy(ac):
    ans = [ac[0][1], ac[1][0], ac[1][1], ac[0][2], ac[0][3], ac[1][2], ac[2][1], ac[2][1], ac[3][0]]
    return sorted(ans)[4]


def dcp(i, j, image):
    ans, n = 0, len(image)

    for x in range(8):
        for y in range(8):
            temp_cos = math.cos(((2 * y + 1) * j * math.pi) / (2 * n)) * math.cos(((2 * x + 1) * i * math.pi) / (2 * n))

            ans += image[x][y] * temp_cos
    if i == 0:
        ans /= math.sqrt(2)
    if j == 0:
        ans /= math.sqrt(2)
    return round(ans / 4, 2)


def dcp_back(i, j, image):
    ans, n = 0, len(image)
    for x in range(8):
        for y in range(8):
            temp_cos = math.cos(((2 * i + 1) * math.pi * x) / (2 * n)) * math.cos(((2 * j + 1) * math.pi * y) / (2 * n))
            if x == 0:
                temp_cos *= math.sqrt(1 / n)
            else:
                temp_cos *= math.sqrt(2 / n)
            if y == 0:
                temp_cos *= math.sqrt(1 / n)
            else:
                temp_cos *= math.sqrt(2 / n)
            ans += image[x][y] * temp_cos
    return round(ans)


def modification(ac):
    z = 4
    dc = ac[0][0]
    med = zigzag_easy(ac)
    if 1 <= abs(dc) <= 1000:
        m = abs(z * ((dc - med) / dc))
    else:
        m = abs(z * med)
    return m


def encryption(image):
    new = list()
    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(dcp(i, j, image))
        new.append(temp)
    return new


def decryption(image):
    ans = list()
    for i in range(8):
        temp = []
        for j in range(8):
            temp.append(dcp_back(i, j, image))
        ans.append(temp)
    return ans


def insert(image, key):
    matrix = prepare(image)
    binary = bin_prepare(key)

    t, k, mse = 80, 12, 0
    for p in range(len(binary)):
        for q in range(len(binary[0])):
            matrix_temp = []
            matrix_next = []
            for i in range(8):
                matrix_temp.append(matrix[p * 8 + i][q * 8:(q + 1) * 8])
                matrix_next.append(matrix[p * 8 + i][(q + 1) * 8:(q + 2) * 8])
            new = encryption(matrix_temp)
            power = modification(new)

            if(matrix_next==[[], [], [], [], [], [], [], []]): continue
            temp_value = encryption(matrix_next)[4][4]
            delta = new[3][3] - temp_value

            if binary[p][q] == 1:
                if delta > (t - k):
                    while delta > (t - k):
                        new[3][3] = new[3][3] - power
                        delta = new[3][3] - temp_value
                elif k > delta > -(t / 2):
                    while k > delta:
                        new[3][3] = new[3][3] + power
                        delta = new[3][3] - temp_value
                elif delta < -(t / 2):
                    while delta > (-t - k):
                        new[3][3] = new[3][3] - power
                        delta = new[3][3] - temp_value

            else:
                if delta > (t / 2):
                    while delta <= (t + k):
                        new[3][3] = new[3][3] + power
                        delta = new[3][3] - temp_value
                elif 0-k < delta < (t / 2):
                    while -k <= delta:
                        new[3][3] = new[3][3] - power
                        delta = new[3][3] - temp_value
                elif delta < (k - t):
                    while delta <= (k - t):
                        new[3][3] = new[3][3] + power
                        delta = new[3][3] - temp_value

            new_back = decryption(new)
            for i in range(8):
                for j in range(8):
                    mse += (matrix[p * 8 + i][q * 8 + j] - new_back[i][j]) ** 2
                    matrix[p * 8 + i][q * 8 + j] = new_back[i][j]

    return matrix


def extract(image):
    matrix = prepare(image)
    binary = []
    t, k = 80, 12
    w = int(image.size[0] / 8) - 1
    h = int(image.size[1] / 8) - 1

    for p in range(w):
        bin_temp = []
        for q in range(h):
            matrix_temp = []
            matrix_next = []
            for i in range(8):
                matrix_temp.append(matrix[p * 8 + i][q * 8:(q + 1) * 8])
                matrix_next.append(matrix[p * 8 + i][(q + 1) * 8:(q + 2) * 8])
            new = encryption(matrix_temp)
            temp_value = encryption(matrix_next)[4][4]
            delta = new[3][3] - temp_value

            if (delta < (-t)) or ((delta > 0) and (delta < t)):
                bin_temp.append(1)
            elif (delta > t) or ((delta < 0) and (delta > (-t))):
                bin_temp.append(0)

        binary.append(bin_temp)
    print("Success")
    return binary






if __name__ == "__main__":
    #container = Image.open("im256.png")

    cvz = Image.open("wm32.png")
    #result = insert(container, cvz)
    #photo(container, result)

    # извлечение
    image_with_cvz = Image.open("Rres4.jpg")
    extraction = extract(image_with_cvz)
    clear = bin_photo(extraction, cvz)
    pros = (clear[0] - clear[1]) / clear[0]

    print(f"\r{clear[1]} / {clear[0]} {round(pros * 100, 2)}%")
    print("BER:", BER(bin_prepare(cvz), extraction))
