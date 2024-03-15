#-*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Author: delimitry
#-----------------------------------------------------------------------


class AsciiCanvas(object):
    """
    ASCII canvas for drawing in console using ASCII chars
    """

    def __init__(self, cols, lines, fill_char=' '):
        """
        Initialize ASCII canvas
        初始化画板，填充fill_char
        """
        if cols < 1 or cols > 1000 or lines < 1 or lines > 1000:
            raise Exception('Canvas cols/lines must be in range [1..1000]')
        self.cols = cols
        self.lines = lines
        if not fill_char:
            fill_char = ' '
        elif len(fill_char) > 1:
            fill_char = fill_char[0]
        self.fill_char = fill_char
        self.canvas = [[fill_char] * (cols) for _ in range(lines)]  # 得到一个cols列的一维数组，然后lines个数组组成二维数组

    def clear(self):
        """
        Fill canvas with empty chars
        """
        self.canvas = [[self.fill_char] * (self.cols) for _ in range(self.lines)]  # 清空，用fill_char清空

    def print_out(self):
        """
        Print out canvas to console
        """
        print(self.get_canvas_as_str())  # 打印到荧幕

    def add_line(self, x0, y0, x1, y1, fill_char='o'):
        """
        Add ASCII line (x0, y0 -> x1, y1) to the canvas, fill line with `fill_char`
        用fill_char画线
        """
        if not fill_char:
            fill_char = 'o'
        elif len(fill_char) > 1:
            fill_char = fill_char[0]
        if x0 > x1: # 从左边画到右边 
            # swap A and B
            x1, x0 = x0, x1
            y1, y0 = y0, y1
        # get delta x, y
        dx = x1 - x0
        dy = y1 - y0
        # if a length of line is zero just add point
        if dx == 0 and dy == 0:
            if self.check_coord_in_range(x0, y0): # 这个点在画布内
                self.canvas[y0][x0] = fill_char
            return
        # when dx >= dy use fill by x-axis, and use fill by y-axis otherwise
        # 哪条边长度长，就填哪边
        if abs(dx) >= abs(dy):
            for x in range(x0, x1 + 1):  # 闭区间[x0,x1+1)
                # 如果是竖线，y就是y0，如果是一条斜线，y的坐标按照比例重新计算绘图点y坐标
                y = y0 if dx == 0 else y0 + int(round((x - x0) * dy / float((dx)))) #
                if self.check_coord_in_range(x, y):
                    self.canvas[y][x] = fill_char  # 填充点
        else:
            if y0 < y1: # 从下往上画
                for y in range(y0, y1 + 1):
                    x = x0 if dy == 0 else x0 + int(round((y - y0) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = fill_char
            else:  # 从上往下画
                for y in range(y1, y0 + 1):
                    x = x0 if dy == 0 else x1 + int(round((y - y1) * dx / float((dy))))
                    if self.check_coord_in_range(x, y):
                        self.canvas[y][x] = fill_char

    def add_text(self, x, y, text):
        """
        Add text to canvas at position (x, y)
        在指定位置添加文本
        """
        for i, c in enumerate(text): # i为字的个数
            if self.check_coord_in_range(x + i, y):
                self.canvas[y][x + i] = c  # 在[x,x+i]位置添加char

    def add_rect(self, x, y, w, h, fill_char=' ', outline_char='o'):
        """
        Add rectangle filled with `fill_char` and outline with `outline_char`
        在画板外围添加方框，增加画面感
        """
        if not fill_char:
            fill_char = ' '
        elif len(fill_char) > 1:
            fill_char = fill_char[0]
        if not outline_char:
            outline_char = 'o'
        elif len(outline_char) > 1:
            outline_char = outline_char[0]
        for px in range(x, x + w):
            for py in range(y, y + h):
                if self.check_coord_in_range(px, py):
                    if px == x or px == x + w - 1 or py == y or py == y + h - 1: #如果坐标位于画板四周
                        self.canvas[py][px] = outline_char
                    else:
                        self.canvas[py][px] = fill_char

    def add_nine_patch_rect(self, x, y, w, h, outline_3x3_chars=None):  #画方框格
        """
        Add nine-patch rectangle
        """
        default_outline_3x3_chars = (
            '.', '-', '.', 
            '|', ' ', '|', 
            '`', '-', "'"
        )
        if not outline_3x3_chars:
            outline_3x3_chars = default_outline_3x3_chars
        # filter chars
        filtered_outline_3x3_chars = []
        for index, char in enumerate(outline_3x3_chars[0:9]):
            if not char:
                char = default_outline_3x3_chars[index]
            elif len(char) > 1:
                char = char[0]
            filtered_outline_3x3_chars.append(char)
        for px in range(x, x + w):  #在方格绘图区域
            for py in range(y, y + h): #在方格绘图区域
                if self.check_coord_in_range(px, py):  #在绘图区域把9个元素放上去
                    if px == x and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[0]
                    elif px == x and y < py < y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[3]
                    elif px == x and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[6]
                    elif x < px < x + w - 1 and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[1]
                    elif x < px < x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[7]
                    elif px == x + w - 1 and py == y:
                        self.canvas[py][px] = filtered_outline_3x3_chars[2]
                    elif px == x + w - 1 and y < py < y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[5]
                    elif px == x + w - 1 and py == y + h - 1:
                        self.canvas[py][px] = filtered_outline_3x3_chars[8]
                    else:
                        self.canvas[py][px] = filtered_outline_3x3_chars[4]

    def check_coord_in_range(self, x, y):
        """
        检查坐标位于画布有效范围
        Check that coordinate (x, y) is in range, to prevent out of range error
        """
        return 0 <= x < self.cols and 0 <= y < self.lines

    def get_canvas_as_str(self):
        """
        Return canvas as a string
        画布输出成可打印字符串，打印到荧幕
        """
        return '\n'.join([''.join(col) for col in self.canvas])

    def __str__(self):
        """
        Return canvas as a string
        """
        return self.get_canvas_as_str()
