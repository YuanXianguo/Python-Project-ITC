def lineEdit_input_modify(self):
    """对文本进行格式化"""
    text1 = self.lineEdit_input.text()
    text1 = '0' if text1 == '' else text1
    text = ''
    count, count_ = 0, 0
    # 负号只能出现在首位，小数点只能出现一次，且在首位时前面补0，在末位删除
    for i in text1:
        if i == '-' and count_ != 0:
            break
        if i == '.':
            count += 1
        if count < 2:
            text += i
        else:
            break
        count_ += 1
    text = text.lstrip('0') if text != '0' else text
    text = '-0' + text[1:] if text[:2] == '-.' else text
    text = '0' + text if text[0] == '.' else text
    # text = '{:.6f}'.format(eval(text))只能保留小数点后位数
    # 文本长度大于7时保留6位有效数字,遵循四舍五入法，并引入科学记数法
    if text[0] == '-':
        text = text[1:]
        text = self.dot_in_seven(text) if '.' in text[:7] else self.dot_not_in_seven(text)
        text = '-' + text
    else:
        text = self.dot_in_seven(text) if '.' in text[:7] else self.dot_not_in_seven(text)
    text = '0' if text in ['-0.', '-0.0', '0.', '0.0', '-'] else text
    return text


def dot_in_seven(self, text):
    """首位是0，且小数点在前7位，左移直到首位不为0，计算后再右移"""
    count = 0
    if text[:2] == '0.':
        for i in text[2:]:
            count += 1
            if i != '0':
                break
        text1 = str(eval(text) * pow(10, count))
        text2 = self.dot_in_seven0(text1)
        if count < 5:
            text = eval(text2) * pow(10, -count)
            text = '{:.10f}'.format(text).rstrip('0')  # 处理计算机误差
        else:
            text = text2 + 'e-{:0>3}'.format(count)
    else:
        text = self.dot_in_seven0(text)
    return text


def dot_in_seven0(self, text):
    """首位不是0，且小数点在前7位"""
    if len(text) > 7:
        if text[6] == '.':  # 小数点在第7位
            if eval(text[7]) < 5:
                text1 = text[:6]
            else:
                text1 = text[:5] + str(eval(text[5]) + 1)
                if eval(text[5]) + 1 == 10:
                    text1 = str(eval(text[:6]) + 1)
                    if text1 == '1000000':
                        text1 = '1e+7'
        else:  # 小数点在前6位
            count = 0
            for i in text[5::-1]:  # 判断小数点在第几位
                count += 1
                if i == '.':
                    break
            if eval(text[7]) < 5:
                text1 = text[:7]
            else:
                text1 = text[:6] + str(eval(text[6]) + 1)
                if eval(text[6]) + 1 == 10:
                    text1 = str(eval(text[:7]) + pow(10, -count))
    else:
        text1 = text
    if '.' in text1:
        for i in text1[text1.index('.'):]:
            if i != '0' and i != '.':
                break
        else:  # 如果小数点后面都是0就删除
            text1 = text1[:text1.index('.')]
    return text1


def dot_not_in_seven(self, text):
    """小数点不在前7位,引入科学记数法"""
    if len(text) > 6:
        if eval(text[6]) < 5:
            text1 = text
        else:
            text1 = text[:5] + str(eval(text[5]) + 1) + text[6:]
            if eval(text[5]) + 1 == 10:
                text1 = str(eval(text[:6]) + 1) + text[6:]
        text = (text1[0] + '.' + text1[1:6]).rstrip('.0') + 'e+{:0>3}'.format(len(text1))
    return text
