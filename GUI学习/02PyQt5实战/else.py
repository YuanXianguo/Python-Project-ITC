def replace_text():
    with open('demo.py', 'r+', encoding='utf-8') as f:
        text = f.read()
        text1 = text.replace('QtWidgets.QLineEdit(self.tab_press1)', 'QLineEditClicked()')
        text2 = text1.replace('QtWidgets.QLineEdit(self.tab_press2)', 'QLineEditClicked()')
        f.seek(0)
        f.write(text2)


def get_list(self, type, str_):
    """获得某一类控件的指针集合"""
    list = []
    i = 1
    while True:
        str_name = "{}{}".format(str_, str(i))
        btn = self.findChild((type), str_name)
        if btn:
            list.append(btn)
            i += 1
        else:
            break
    return list


self.model.dataChanged.connect(self.tableView_data_changed)
def tableView_data_changed(self, index):
    """tableview数据改变"""
    changed_data = self.model.data(self.model.index(index.row(), index.column()))
    self.formula_data_list[index.row() + self.current_step * len(self.para_list)][index.column()] = changed_data


