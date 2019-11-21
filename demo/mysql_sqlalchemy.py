from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

# 连接 mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
engine = create_engine('mysql+pymysql://root:2017916@localhost/itc?charset=utf8')

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)

# para_list = ['系统时间', '班次', '配方', '测试模式',  '大漏值', '工作压力','扭矩', 'ΔP1', 'ΔP2', '报错信息', '测试结果']


class TestResults(Base):
    """声明模型"""
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_pos_id = Column(Integer, nullable=False)
    sys_time = Column(String(20), nullable=False)
    formula = Column(String(20), nullable=False)
    test_mode = Column(String(20), nullable=False)
    big_leak = Column(String(20), default="")
    work_press = Column(String(20), default="")
    torque = Column(String(20), default="")
    cur_test = Column(String(20), default="")
    cur_p1 = Column(String(20), default="")
    cur_p2 = Column(String(20), default="")
    error_msg = Column(String(20), default="")
    is_pass = Column(String(5), default="")
    is_delete = Column(Boolean, default=0)

    def __repr__(self):
        pass

    def str(self):
        return "{},{},{},{},{},{},{},{},{},{},{}".format(
            self.sys_time, self.formula, self.test_mode, self.big_leak,
            self.work_press, self.torque, self.cur_test, self.cur_p1,
            self.cur_p2, self.error_msg, self.is_pass)


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

    def get_more(self, work_pos, start_time, end_time):
        """获取多条数据"""
        try:
            return self.session.query(TestResults).filter(
                TestResults.is_delete == 0,
                TestResults.work_pos_id == work_pos,
                TestResults.sys_time >= start_time,
                TestResults.sys_time <= end_time).all()
        except:
            pass






