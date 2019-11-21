from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///test_process.db?check_same_thread=False")

# 声明映像
Base = declarative_base()

# 创建会话
Session = sessionmaker(bind=engine)


class TestProcess(Base):
    """声明模型"""
    __tablename__ = 'test_process'
    id = Column(Integer, primary_key=True, autoincrement=True)
    work_pos_id = Column(Integer, nullable=False)

    sys_time = Column(String(20), nullable=False)
    # order = Column(String(20), nullable=False)
    # formula = Column(String(20), nullable=False)
    # test_mode = Column(String(20), nullable=False)
    # test_time = Column(String(20), nullable=False)
    # test_result = Column(String(20), nullable=False)

    a_p1 = Column(String(20))
    a_p2 = Column(String(20))
    # a_open_torque = Column(String(20), nullable=False)
    # a_close_torque = Column(String(20), nullable=False)
    # a_test_result = Column(String(20), nullable=False)

    b_p1 = Column(String(20))
    b_p2 = Column(String(20))
    # b_open_torque = Column(String(20), nullable=False)
    # b_close_torque = Column(String(20), nullable=False)
    # b_test_result = Column(String(20), nullable=False)

    c_p1 = Column(String(20))
    c_p2 = Column(String(20))
    # c_open_torque = Column(String(20), nullable=False)
    # c_close_torque = Column(String(20), nullable=False)
    # c_test_result = Column(String(20), nullable=False)

    d_p1 = Column(String(20))
    d_p2 = Column(String(20))
    # d_open_torque = Column(String(20), nullable=False)
    # d_close_torque = Column(String(20), nullable=False)

    press = Column(String(20))
    leak = Column(String(20))
    torque = Column(String(20))

    is_delete = Column(Boolean, default=0)

    def str(self):
        return "{},{},{},{},{},{},{},{},{},{},{},{}".format(
            self.sys_time,
            self.a_p1, self.a_p2,
            self.b_p1, self.b_p2,
            self.c_p1, self.c_p2,
            self.d_p1, self.d_p2,
            self.press, self.leak, self.torque
        )


# 创建数据表
TestProcess.metadata.create_all(engine)


class AddAndGetP(object):
    """操作对象，增删改查"""
    def __init__(self):
        self.session = Session()

    def add_one(self, new_obj):
        """新增数据"""
        self.session.add(new_obj)

    def commit(self):
        self.session.commit()
        # return new_obj

    def get_more(self, work_pos, start_time, end_time):
        """获取多条数据"""
        try:
            return self.session.query(TestProcess).filter(
                TestProcess.is_delete == 0,
                TestProcess.work_pos_id == work_pos,
                TestProcess.sys_time >= start_time,
                TestProcess.sys_time <= end_time).all()
        except:
            pass






