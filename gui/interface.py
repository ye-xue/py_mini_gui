import sys
import time
import logging
import threading
from datetime import datetime
from logging import StreamHandler, Formatter
from tkinter import Tk, Frame, Menu, YES, font, Label
from tkinter.scrolledtext import ScrolledText
from tkinter import N, E, W, X, Y, BOTTOM, BOTH, TOP, RIGHT, END, LEFT

from queue import Queue

# 基础logging消息使用最好的等级进行过滤,防止出现其它库提交的log信息
logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.WARNING)
logger = logging.getLogger('gui')
logger.setLevel(logging.DEBUG)

MESSAGE_QUEUE = Queue()


class _Tk(Tk):

    def report_callback_exception(self, exc, val, tb):
        """Report callback exception on sys.stderr.

        Applications may want to override this internal function, and
        should when sys.stderr is None."""
        import traceback
        # print("Exception in Tkinter callback", file=sys.stderr)
        sys.last_type = exc
        sys.last_value = val
        sys.last_traceback = tb
        # 将错误堆栈打印出来,方便追踪
        traceback.print_exception(exc, val, tb)
        Message.error("程序执行中出现错误")


MAIN_TK = _Tk()


class MessageObject:
    """信息对象"""

    def __init__(self, message, style):
        # 信息内容
        self.message = str(message)
        self.style = style  # debug info warning error success
        self.time = datetime.now()

        if style not in ['debug', 'info', 'warning', 'error', 'success']:
            raise TypeError(f'{style}:信息类型错误')


def _init_menu():
    """初始化目录"""
    menu_bar = Menu(MAIN_TK)
    MAIN_TK.config(menu=menu_bar)
    return menu_bar


def _init_functional_area():
    """初始化功能区"""
    functional_area = Frame(MAIN_TK)
    functional_area.pack(side=TOP, fill=BOTH, expand=YES)

    # 将初始描述添加到界面中
    label_font = font.Font(family="微软雅黑", size=17)
    label = Label(functional_area, text='欢迎使用本工具\n请选择目录对应功能', font=label_font, height=4)
    label.pack()

    return functional_area


def _init_message_box():
    """初始化信息框"""
    message_box = ScrolledText(MAIN_TK)
    message_box.pack(side=BOTTOM, fill=BOTH)
    # 设置消息展示样式
    message_box.tag_configure('info', font=('微软雅黑', 8), foreground='#303133')
    message_box.tag_configure('warning', font=('微软雅黑', 10), foreground='#ebb563')
    message_box.tag_configure('error', font=('微软雅黑', 12, 'bold'), foreground='#f56c6c')
    message_box.tag_configure('success', font=('微软雅黑', 14, 'bold'), foreground='#85ce61')

    return message_box


class Interface:
    """界面框架"""
    _run_fun = []  # 运行界面时执行的函数
    _exit_fun = []  # 关闭界面时执行的函数

    menu = _init_menu()
    functional_area = _init_functional_area()
    message_box = _init_message_box()

    @classmethod
    def init(cls, title='工具', geometry='450x900'):

        # 初始化界面,设置标题与界面大小位置
        MAIN_TK.title(title)
        MAIN_TK.geometry(geometry)

        # 自定义停止调用函数
        MAIN_TK.protocol("WM_DELETE_WINDOW", cls._exit)

    @classmethod
    def init_run(cls, fun):
        """注册界面运行时执行的函数"""
        Message.debug(f"注册运行时执行函数:{fun}")
        cls._run_fun.append(fun)

    @classmethod
    def run(cls):
        """运行界面"""
        Message.debug("执行注册在开始时运行的函数")
        # 单开一个线程用于处理消息,设置为守护线程,主线程退出后,直接退出该线程
        message_thread = threading.Thread(target=cls._update_message, daemon=True)
        message_thread.start()
        Message.debug("启动消息更新线程")
        for fun in cls._run_fun:
            result = fun()
            Message.debug(f"执行运行函数:{fun},结果:{result}")
        MAIN_TK.mainloop()

    @classmethod
    def init_exit(cls, fun):
        """注册退出时运行的函数"""
        Message.debug(f"注册退出时执行函数:{fun}")
        cls._exit_fun.append(fun)

    @classmethod
    def _exit(cls):
        """设置关闭程序时执行的函数,然后关闭页面"""
        # 执行关闭函数
        for fun in cls._exit_fun:
            result = fun()
            logger.debug(f"执行关闭函数:{fun},结果:{result}")
        logger.debug("执行注册在退出时运行的函数")
        # 关闭界面
        MAIN_TK.destroy()
        logger.debug("关闭程序界面")

    @classmethod
    def update(cls):
        """更新界面"""
        MAIN_TK.update()

    @classmethod
    def _insert_message(cls, message_object: MessageObject):
        """插入消息,根据消息的级别进行对应格式的展示,并同时在将消息出入主程序消息logger对象"""
        message = message_object.message
        style = message_object.style
        cls.message_box.insert(END, message + '\n', style)

    @classmethod
    def _update_message(cls):
        """轮询队列,有新消息就插入"""
        update = False
        while True:
            if MESSAGE_QUEUE.empty() and update:
                cls.message_box.see(END)
                update = False
            message_object = MESSAGE_QUEUE.get()
            cls._insert_message(message_object)
            update = True

    @classmethod
    def functional_area_clean(cls):
        """清空功能区域的所有控件"""
        for widget in cls.functional_area.winfo_children():
            widget.destroy()


class Message:
    """信息组件"""

    @classmethod
    def debug(cls, *messages):
        """调试"""
        message = ",".join([str(data) for data in messages])
        logger.debug(message)

    @classmethod
    def info(cls, *messages):
        """信息"""
        message = ",".join([str(data) for data in messages])
        message_object = MessageObject(message, 'info')
        MESSAGE_QUEUE.put(message_object)
        logger.info(message)

    @classmethod
    def warning(cls, *messages):
        """警告"""
        message = ",".join([str(data) for data in messages])
        message_object = MessageObject(message, 'warning')
        MESSAGE_QUEUE.put(message_object)
        logger.warning(message)

    @classmethod
    def error(cls, *messages):
        """错误"""
        message = ",".join([str(data) for data in messages])
        message_object = MessageObject(message, 'error')
        MESSAGE_QUEUE.put(message_object)
        logger.error(message)

    @classmethod
    def success(cls, *messages):
        """信息"""
        message = ",".join([str(data) for data in messages])
        message_object = MessageObject(message, 'success')
        MESSAGE_QUEUE.put(message_object)
        logger.info(message)
