from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test_result.db?check_same_thread=False")

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)


class TestResult(Base):
    """声明模型"""
    # '系统时间', '班次', '配方', '测试模式', '测试时间', '测试结果',
    # 'A-ΔP1', 'A-ΔP2', 'A-全开扭矩', 'A-全关扭矩', 'A-测试结果',
    # 'B-ΔP1', 'B-ΔP2', 'B-全开扭矩', 'B-全关扭矩', 'B-测试结果',
    # 'C-ΔP1', 'C-ΔP2', 'C-全开扭矩', 'C-全关扭矩', 'C-测试结果',
    # 'D-ΔP1', 'D-ΔP2', 'D-全开扭矩', 'D-全关扭矩', 'D-测试结果',
    # '合格数', '不合格数', '总数', '合格率']
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_pos = Column(Integer)
    sys_time = Column(String(50))
    order = Column(String(20))
    formula = Column(String(20))
    mode = Column(String(20))
    test_time = Column(String(20))
    test_result = Column(String(50))

    a_p1 = Column(String(20))
    a_p2 = Column(String(20))
    a_open = Column(String(20))
    a_close = Column(String(20))
    a_res = Column(String(20))
    b_p1 = Column(String(20))
    b_p2 = Column(String(20))
    b_open = Column(String(20))
    b_close = Column(String(20))
    b_res = Column(String(50))
    c_p1 = Column(String(20))
    c_p2 = Column(String(20))
    c_open = Column(String(20))
    c_close = Column(String(20))
    c_res = Column(String(50))
    d_p1 = Column(String(20))
    d_p2 = Column(String(20))
    d_open = Column(String(20))
    d_close = Column(String(20))
    d_res = Column(String(50))

    pass_count = Column(String(20))
    unpass_count = Column(String(20))
    count = Column(String(20))
    pass_rate = Column(String(20))

    def __str__(self):
        temp = "{}," * 29 + "{}"
        return temp.format(
            self.sys_time, self.order, self.formula, self.mode, self.test_time,
            self.test_result, self.a_p1, self.a_p2, self.a_open, self.a_close,
            self.a_res, self.b_p1, self.b_p2, self.b_open, self.b_close,
            self.b_res, self.c_p1, self.c_p2, self.c_open, self.c_close,
            self.c_res, self.d_p1, self.d_p2, self.d_open, self.d_close,
            self.d_res, self.pass_count, self.unpass_count, self.count,
            self.pass_rate)


class Crud(object):
    """操作对象，增删改查"""
    def __init__(self):
        self.session = Session()

    def add_one(self, test_list, work_pos):
        """新增数据"""
        new_obj = TestResult(
            work_pos=work_pos, sys_time=test_list[0],
            order=test_list[1], formula=test_list[2], mode=test_list[3],
            test_time=test_list[4], test_result=test_list[5],
            a_p1=test_list[6], a_p2=test_list[7],
            a_open=test_list[8], a_close=test_list[9],
            a_res=test_list[10], b_p1=test_list[11],
            b_p2=test_list[12], b_open=test_list[13],
            b_close=test_list[14], b_res=test_list[15],
            c_p1=test_list[16], c_p2=test_list[17],
            c_open=test_list[18], c_close=test_list[19],
            c_res=test_list[20], d_p1=test_list[21],
            d_p2=test_list[22], d_open=test_list[23],
            d_close=test_list[24], d_res=test_list[25],
            pass_count=test_list[26], unpass_count=test_list[27],
            count=test_list[28], pass_rate=test_list[29],)
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        """获取一条数据，参数为id"""
        return self.session.query(TestResult).get(1).__str__()

    def get_more(self, work_pos_index, start_time, end_time):
        """获取多条数据"""
        res = self.session.query(TestResult).filter(
            TestResult.work_pos == work_pos_index,
            TestResult.sys_time >= start_time,
            TestResult.sys_time <= end_time).all()

        return [r.__str__().split(",") for r in res]

    def update_data(self, id):
        """修改单条数据"""
        obj = self.session.query(TestResult).get(id)
        if obj:
            obj.is_delete = 0
            self.session.add(obj)
            self.session.commit()
            return obj
        return False

    def update_datas(self, id):
        """修改多条数据"""
        data_list = self.session.query(TestResult).filter(id > 5)
        for data in data_list:
            data.is_delete = 0
            self.session.add(data)
        self.session.commit()

    def delete_data(self, id):
        """删除数据"""
        data = self.session.query(TestResult).get(id)
        self.session.delete(data)
        self.session.commit()


# 创建数据表
TestResult.metadata.create_all(engine)


