import pygame
#输入框类
class text_box:
    #初始化
    def __init__(self, w, h, s, x, y, font=None):
        self.wide = w      #输入框宽度
        self.height = h    #输入框高度
        self.size = s      #输入框尺字体大小
        self.xx = x        #输入框x坐标
        self.yy = y        #输入框y坐标


        self.text = ""  # 文本框内容
        if font is None:    #字体指针
            self.font = pygame.font.Font(None, 32)
        else:
            self.font = font


    def text_box_paint(self, dest_surf):
        #输入内容屏幕绘制
        line = self.string_split()
        font = pygame.font.Font("LeviReBrushed.ttf", self.size)
        flag = 0
        for temp in line:
            tmp = font.render(temp, True, (0, 0, 100))
            dest_surf.blit(tmp, (self.xx, self.yy + flag * (self.size + 10)))
            flag += 1


    def string_split(self):
        #拆分输入字符串
        line = []
        line.append('')
        flag = 0
        for s in self.text:
            if s == '\n':
                flag += 1
                line.append('')
            elif len(line[flag]) >= self.wide:
                flag += 1
                line.append('')
                line[flag] += s
            else:
                line[flag] += s
        return line


    def key_down(self, event):
        #键盘监听函数
        unicode = event.unicode
        key = event.key

        # 退位键
        if key == 8:
            if self.text[-1] == '\n':
                self.text = self.text[:-1]
            self.text = self.text[:-1]
            return

        # 切换大小写键
        if key == 301:
            return

        # 回车键
        if key == 13:
            self.text += '\n'
            return

        if key == 32:
            self.text += ' '
            return

        if unicode != "":
            char = unicode
            self.text += char
        elif within_font(key):
            char = chr(key)
            self.text += char


def within_font(key):
    #判断该字是否在字体库中
    dictionary = [36,43,45,42,47,61,37,34,39,35,64,38,95,40,41,44,46,59,58,63,33,92,124,60,62,91,93,96,94,126,174]
    if 96 < key < 123:
        return True
    elif 64 < key < 91:
        return True
    elif 47 < key < 58:
        return True
    elif 47 < key < 58:
        return True
    for i in dictionary:
        if key == i:
            return True

    return False

