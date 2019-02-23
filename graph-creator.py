# Dominik Sedlak, 2019
# Alfa version v0.0001 - prototype in chaos

from PIL import Image, ImageDraw, ImageFont  # pip install Pillow
from datetime import datetime
import random

"""
Example functions stolen from: https://www.tutorialspoint.com/python/python_sorting_algorithms.htm
======================== FUNCTIONS =====================================
"""
def bubblesort(list):
# Swap the elements to arrange in order
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if list[idx]>list[idx+1]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp

def merge_sort(unsorted_list):
    if len(unsorted_list) <= 1:
        return unsorted_list
# Find the middle point and devide it
    middle = len(unsorted_list) // 2
    left_list = unsorted_list[:middle]
    right_list = unsorted_list[middle:]

    left_list = merge_sort(left_list)
    right_list = merge_sort(right_list)
    return list(merge(left_list, right_list))

# Merge the sorted halves

def merge(left_half,right_half):

    res = []
    while len(left_half) != 0 and len(right_half) != 0:
        if left_half[0] < right_half[0]:
            res.append(left_half[0])
            left_half.remove(left_half[0])
        else:
            res.append(right_half[0])
            right_half.remove(right_half[0])
    if len(left_half) == 0:
        res = res + right_half
    else:
        res = res + left_half
    return res

def insertion_sort(InputList):
    for i in range(1, len(InputList)):
        j = i-1
        nxt_element = InputList[i]
# Compare the current element with next one

        while (InputList[j] > nxt_element) and (j >= 0):
            InputList[j+1] = InputList[j]
            j=j-1
        InputList[j+1] = nxt_element

def shellSort(input_list):

    gap = len(input_list) // 2
    while gap > 0:

        for i in range(gap, len(input_list)):
            temp = input_list[i]
            j = i
# Sort the sub list for this gap

            while j >= gap and input_list[j - gap] > temp:
                input_list[j] = input_list[j - gap]
                j = j-gap
            input_list[j] = temp

# Reduce the gap for the next element

        gap = gap//2

def selection_sort(input_list):

    for idx in range(len(input_list)):

        min_idx = idx
        for j in range( idx +1, len(input_list)):
            if input_list[min_idx] > input_list[j]:
                min_idx = j
# Swap the minimum value with the compared value

        input_list[idx], input_list[min_idx] = input_list[min_idx], input_list[idx]

def gen(n):
    data = []
    for i in range(n):
        data.append(random.randrange(n)+1)
    return data

""" Your implementation """
def generator_for_your_function(n):
    pass
def your_function(input):
    pass
""" ======================================================================== """

# image creating
def getY(y, height=500):
    return height - 50 - y   # TODO check
def getX(x):
    return x + 50
def toImg(image, name, data, width, height, filename, bgC, descrC, graphC, max_n, max_t):
    # DATA
    dLine = ImageDraw.Draw(image)
    #max_n, max_t = data[len(data)-1][0]+1, data[len(data)-1][1]
    x2, y2 = data[0][0], data[0][1]
    for item in data:
        x1, y1 = x2, y2
        x2 = ( (width-100) / max_n ) * item[0]
        y2 = ( (height-100) / max_t ) * item[1]
        #print("n = ",item[0],"t =", item[1], "=> x =",int(x2),"y =", int(y2))
        dLine.line((getX(x1), getY(y1, image.size[1]), getX(x2), getY(y2, image.size[1])), fill=graphC)

# create data and img, time_unit 1=s 1000=ms 1000000=μ
def analyze(function, genData, max_value, accuracy=10, time_unit=1000):
    data = []
    for n in range(accuracy):
        input_size = int((max_value / accuracy) * n)
        inputData = genData(input_size)
        tstart = datetime.now()
        function(inputData)
        tstop = datetime.now()
        duration = tstop - tstart
        data.append([input_size, duration.total_seconds() * time_unit])
        print(input_size,"input size complete")
    return data

def start(functions, width, height, filename, bgC, descrC, graphC, max_n, data_count, time_unit):
    image = Image.new('RGB', (width, height), color = 'black').convert('RGBA')

    # Axis
    dLine = ImageDraw.Draw(image)
    dLine.line((width-50,height-50,50,height-50), fill=descrC)
    dLine.line((50,height-50,50,50), fill=descrC)
    del dLine

    # TEXT
    text = Image.new('RGBA', image.size, (0,0,0,0))  # transparent layer
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 20)  # font
    dText = ImageDraw.Draw(text)  # drawer
    for i in range(2):  # aby to bylo tucnejsi
        dText.text((28,10), "time", font=font, fill=descrC)
        dText.text((width-300,height-45), "input size, max="+str(max_n), font=font, fill=descrC)
        dText.text((35,height-45), "0", font=font, fill=descrC)

        for j in range(len(functions)):
            dText.text((53, 65+25*j), functions[j][2], font=font, fill=functions[j][3])

    for func in functions:
        print("\n"+func[2]+" ("+func[3]+")\n")
        func.append(analyze(func[0], func[1], max_n, data_count, time_unit))

    max_t = 0
    for func in functions:
        if func[4][len(func[4])-1][1] > max_t:
            max_t = func[4][len(func[4])-1][1]

    dText.text((12,30), "max="+str(max_t), font=font, fill=descrC)

    for func in functions:
        toImg(image, func[2], func[4], width, height, filename, bgC, descrC, func[3], max_n, max_t)

    out = Image.alpha_composite(image, text)

    out.show()
    image.save(filename)

""" =========================== RUN ======================================== """

# [algorithm, array generator for it, name, color, (then data)]
functions = [
    [bubblesort, gen, "bubble sort", "blue"],
    [merge_sort, gen, "merge sort", "yellow"],
    [insertion_sort, gen, "insert sort", "green"],
    [shellSort, gen, "shell sort", "red"],
    [selection_sort, gen, "selection sort", "pink"]
]

filename = input("Output filename without .png: ") + ".png"
max_size = int(input("Max testing array size: "))
samples = int(input("Samples: "))
time_unit = int(input("Time unit (1=s, 1000=ms, 1000000=μ): "))

# functions, width, height, filename, bgC, textC, graphC, max_size, data count, time_unit (1000=ms)
start(functions, 800, 800, filename, "black", "white", "yellow", max_size, samples, time_unit)
