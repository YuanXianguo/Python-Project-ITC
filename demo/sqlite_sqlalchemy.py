from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test_result.db?check_same_thread=False")

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)

# self.para_list = [
# '系统时间', '班次', '配方', '测试模式', '测试时间', '测试结果',
# 'A-ΔP1', 'A-ΔP2', 'A-全开扭矩', 'A-全关扭矩', 'A-测试结果',
# 'B-ΔP1', 'B-ΔP2', 'B-全开扭矩', 'B-全关扭矩', 'B-测试结果',
# 'C-ΔP1', 'C-ΔP2', 'C-全开扭矩', 'C-全关扭矩', 'C-测试结果',
# 'D-ΔP1', 'D-ΔP2', 'D-全开扭矩', 'D-全关扭矩', 'D-测试结果',
# '合格数', '不合格数', '总数', '合格率']


class TestResults(Base):
    """声明模型"""
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_pos_id = Column(Integer, nullable=False)

    sys_time = Column(String(20), nullable=False)
    order = Column(String(20), nullable=False)
    formula = Column(String(20), nullable=False)
    test_mode = Column(String(20), nullable=False)
    test_time = Column(String(20), nullable=False)
    test_result = Column(String(20), nullable=False)

    a_p1 = Column(String(20), nullable=False)
    a_p2 = Column(String(20), nullable=False)
    a_open_torque = Column(String(20), nullable=False)
    a_close_torque = Column(String(20), nullable=False)
    a_test_result = Column(String(20), nullable=False)

    b_p1 = Column(String(20), nullable=False)
    b_p2 = Column(String(20), nullable=False)
    b_open_torque = Column(String(20), nullable=False)
    b_close_torque = Column(String(20), nullable=False)
    b_test_result = Column(String(20), nullable=False)

    c_p1 = Column(String(20), nullable=False)
    c_p2 = Column(String(20), nullable=False)
    c_open_torque = Column(String(20), nullable=False)
    c_close_torque = Column(String(20), nullable=False)
    c_test_result = Column(String(20), nullable=False)

    d_p1 = Column(String(20), nullable=False)
    d_p2 = Column(String(20), nullable=False)
    d_open_torque = Column(String(20), nullable=False)
    d_close_torque = Column(String(20), nullable=False)
    d_test_result = Column(String(20), nullable=False)

    pass_count = Column(String(20), nullable=False)
    un_pass_count = Column(String(20), nullable=False)
    total = Column(String(20), nullable=False)
    pass_rate = Column(String(20), nullable=False)

    is_delete = Column(Boolean, default=0)

    def str(self):
        return "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},".format(
            self.sys_time, self.order, self.formula, self.test_mode, self.test_time, self.test_result,
            self.a_p1, self.a_p2, self.a_open_torque, self.a_close_torque, self.a_test_result,
            self.b_p1, self.b_p2, self.b_open_torque, self.b_close_torque, self.b_test_result,
            self.c_p1, self.c_p2, self.c_open_torque, self.c_close_torque, self.c_test_result,
            self.d_p1, self.d_p2, self.d_open_torque, self.d_close_torque, self.d_test_result,
            self.pass_count, self.un_pass_count, self.total, self.pass_rate
        )


# 创建数据表
TestResults.metadata.create_all(engine)


class AddAndGet(object):
    """操作对象，增删改查"""
    def __init__(self):
        self.session = Session()

    def add_one(self, new_obj):
        """新增数据"""
        self.session.add(new_obj)
        self.session.commit()
        return new_obj

    def get_one(self):
        """获取一条数据，参数为id"""
        return self.session.query(TestResults).get(1)

    def get_more(self, work_pos, start_time, end_time, order):
        """获取多条数据"""
        try:
            return self.session.query(TestResults).filter(
                TestResults.is_delete == 0,
                TestResults.work_pos_id == work_pos,
                TestResults.order == order,
                TestResults.sys_time >= start_time,
                TestResults.sys_time <= end_time).all()
        except:
            pass






