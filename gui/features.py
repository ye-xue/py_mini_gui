"""功能"""
import json
import os
import sys
import time
import traceback
from threading import Thread
from tkinter import Tk, Scrollbar, Text, Frame, Label, Button, font, Entry, Menu as Tkinter_Menu
from tkinter import N, E, W, X, Y, BOTTOM, BOTH, TOP, RIGHT, END, LEFT, YES, NO
from tkinter import filedialog, Radiobutton, Checkbutton
from tkinter import StringVar, BooleanVar, IntVar
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from gui.interface import Message, Interface
from gui.data import RunTimeData


class MenuBase:
    """菜单"""

    def __init__(self, menu: Tkinter_Menu):
        """初始化主菜单数据"""
        self._menu = menu

    def add_cascade(self, name):
        """添加一个父菜单"""
        menu = Tkinter_Menu(self._menu, tearoff=0)
        self._menu.add_cascade(label=name, menu=menu)
        return MenuBase(menu)

    def add_command(self, name, description, components, run_func):
        """添加一个执行功能"""

        def reset_command():
            """将添加了前后功能处理的函数添加到目录中"""
            RunTimeData.reset()
            Interface.functional_area_clean()
            _description(description)
            RunTimeData.set_components(components)
            for component in components:
                component.show()
            _run(run_func)
            Message.info(f"选择功能: {name}")

        self._menu.add_command(label=name, command=reset_command)

    def add_separator(self):
        """添加一个分割线"""
        self._menu.add_separator()


Menu: MenuBase = MenuBase(Interface.menu)


def _description(description=''):
    """描述组件"""
    label_font = font.Font(family="微软雅黑", size=16)
    label = Label(Interface.functional_area, text=description, font=label_font, height=3,
                  wraplength=590)
    label.pack(fill=X)


def _run(command):
    """运行程序按钮"""

    def reset_command():
        """添加运行程序的头尾标识,并将异常信息添加到程序中"""
        try:
            Message.success("开始运行")
            start_time = time.time()
            values = RunTimeData.get_run_values()
            Message.debug(f"运行程序使用的值列表:{values}")
            command(*values)
            # 查看警告信息,如果有警告信息,就显示出来
            warn = RunTimeData.get_warning()
            if warn:
                for key, message in warn.items():
                    key_message = f"{key}:{message}"
                    Message.warning(key_message)
                Message.error("以上为警告信息")

            end_time = time.time()
            Message.success("成功结束, 运行时间: {:.4f} 秒".format(end_time - start_time))

        except:
            Message.error("错误详细信息:{}".format(traceback.format_exc()))
            Message.error("程序运行出现错误")

    def thread_command():
        """使用子线程进行数据的处理,防止程序阻塞界面显示"""
        thread = Thread(target=reset_command)
        thread.start()

    button = Button(Interface.functional_area, text="开始运行", command=thread_command, bg="#409eff")
    button.pack(side=BOTTOM, fill=X)


class OneFileSelect:
    """单文件选择"""

    def __init__(self, button_text="标识", file_types=None, default_value=None):
        """添加文件选择功能按钮"""
        self._value = default_value
        self._label_str = StringVar()
        if default_value:
            self._label_str.set(str(default_value))
        else:
            self._label_str.set(f"选择 {button_text} 对应的文件")

        self._button_text = button_text
        self._file_types = file_types

    def _select_file(self):
        """选择指定格式文件"""
        select_file_path = filedialog.askopenfilename(title=f'选择 {self._button_text} 文件',
                                                      filetypes=_file_types(self._file_types))
        if select_file_path:
            Message.info("选择文件:" + select_file_path)
            self._value = select_file_path
            self._label_str.set(select_file_path)
        else:
            Message.warning("未选择文件")

    def show(self):
        # bd是边框宽度, relief是边框样式 sunken是凹陷
        frame = Frame(Interface.functional_area, bd=1, relief="sunken")
        frame.pack(fill=X)
        button = Button(frame, text=self._button_text, command=self._select_file)
        button.pack(fill=X, side=LEFT)
        label = Label(frame, textvariable=self._label_str)
        label.pack(fill=X, side=RIGHT)

    def get(self):
        return self._value


class MultiFileSelect:
    """多文件选择"""

    def __init__(self, button_text="标识", file_types=None, default_value=None):
        """添加文件选择功能按钮"""
        self._value = []
        self._label_str = StringVar()
        if default_value:
            self._value = default_value
            self._label_str.set(str(default_value))
        else:
            self._label_str.set(f"选择 {button_text} 对应的多个文件")

        self._button_text = button_text
        self._file_types = file_types

    def _select_files(self):
        """选择指定格式文件"""
        select_file_paths = filedialog.askopenfilenames(title=f'选择 {self._button_text} 对应的多个文件',
                                                        filetypes=_file_types(self._file_types))
        if select_file_paths:
            self._value = select_file_paths
            self._label_str.set(json.dumps(select_file_paths, ensure_ascii=False))
            Message.info("选择的多个文件为:")
            for file_path in select_file_paths:
                Message.info(file_path)
        else:
            Message.warning("未选择文件")

    def show(self):
        # bd是边框宽度, relief是边框样式 sunken是凹陷
        frame = Frame(Interface.functional_area, bd=1, relief="sunken")
        frame.pack(fill=X)
        button = Button(frame, text=self._button_text, command=self._select_files)
        button.pack(fill=X, side=LEFT)
        label = Label(frame, textvariable=self._label_str)
        label.pack(fill=X, side=RIGHT)

    def get(self):
        return self._value


class FolderSelect:
    """文件夹选择"""

    def __init__(self, button_text="文件夹", default_value=None):
        self._value = default_value

        self._label_str = StringVar()

        if self._value:
            self._label_str.set(str(self._value))
        else:
            self._label_str.set(f"选择 {button_text} 对应文件夹")

        self._button_text = button_text

    def _select_dir(self):
        """选择文件夹"""
        select_dir_path = filedialog.askdirectory(title=f"选择 {self._button_text} 对应文件夹")
        if select_dir_path:
            Message.info("选择文件夹:" + select_dir_path)
            self._value = select_dir_path
            self._label_str.set(select_dir_path)
        else:
            Message.warning("未选择文件夹")

    def show(self):
        frame = Frame(Interface.functional_area, bd=1, relief="sunken")
        frame.pack(fill=X)
        button = Button(frame, text=self._button_text, command=self._select_dir)
        button.pack(fill=X, side=LEFT)
        label = Label(frame, textvariable=self._label_str)
        label.pack(fill=X, side=RIGHT)

    def get(self):
        return self._value


class OutFolderSelect(FolderSelect):
    """输出文件夹选择"""

    def __init__(self, button_text="输出位置"):
        dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        super().__init__(button_text, default_value=dir_path)


class Input:
    """文本输入"""

    def __init__(self, button_text="文本", default_value='输入文本'):
        self._button_text = button_text
        self._value = default_value
        self._entry = None

    def show(self):
        frame = Frame(Interface.functional_area)
        frame.pack(fill=X)
        label = Label(frame, text=self._button_text)
        label.pack(side=LEFT)
        self._entry = Entry(frame, show=None)
        self._entry.pack(fill=X)
        self._entry.insert(0, self._value)

    def get(self):
        return self._entry.get()


class InputText:
    """长文本输入"""

    def __init__(self, button_text="文本", default_value='输入长文本', height=6):
        self._button_text = button_text
        self._default_value = default_value
        self._height = height
        self._scrolled_text = None

    def show(self):
        frame = Frame(Interface.functional_area)
        frame.pack(fill=X)
        label = Label(frame, text=self._button_text)
        label.pack(side=TOP)
        self._scrolled_text = ScrolledText(frame, height=self._height)
        self._scrolled_text.pack(side=BOTTOM)
        self._scrolled_text.insert("1.0", self._default_value)

    def get(self):
        return self._scrolled_text.get(index1='1.0', index2=END)


class RadioButton:
    """单选按钮"""

    def __init__(self, button_text="单选", default_value=True, options=None):
        self._button_text = button_text
        self._value = _tkinter_var(default_value)
        self._value.set(default_value)
        self._options = options if options else [('是', True), ("否", False)]

    def show(self):
        frame = Frame(Interface.functional_area)
        frame.pack(fill=X)
        label = Label(frame, text=self._button_text)
        label.pack(side=LEFT)
        for text, value in self._options:
            radio_button = Radiobutton(frame, variable=self._value, text=text, value=value)
            radio_button.pack(side=LEFT)

    def get(self):
        return self._value.get()


class CheckButton:
    """多选按钮"""

    def __init__(self, button_text="多选", options=None):
        self._button_text = button_text
        self._options = options if options else [("选项1", True), ("选项2", True)]
        self._value_list = []

    def show(self):
        frame = Frame(Interface.functional_area)
        frame.pack(fill=X)
        label = Label(frame, text=self._button_text)
        label.pack(side=LEFT)
        for text, value in self._options:
            var = BooleanVar()
            var.set(value)
            check_button = Checkbutton(frame, text=text, variable=var, onvalue=True, offvalue=False)
            check_button.pack(side=LEFT)
            self._value_list.append(var)

    def get(self):
        return [var.get() for var in self._value_list]


def _file_types(types=None):
    if types == "pdf":
        return [('PDF文件', '*.pdf *.PDF')]
    elif types == "excel":
        return [('excel文件', '*.xlsx *.xls *.xlsm')]
    elif types == "csv":
        return [('csv文件', '*.csv')]
    elif types == "exe":
        return [('exe文件', '*.exe')]
    elif types == "png":
        return [('png', '*.png')]
    elif types is None:
        return [('所有文件', '*.*')]
    elif not isinstance(types, list):
        raise ValueError(f"文件类型:{types}不是列表")
    else:
        return types


def _tkinter_var(value):
    """根据值的类型返回对应的tkinter变量"""
    value_type = type(value)
    if value_type == bool:
        return BooleanVar()
    elif value_type == int:
        return IntVar()
    elif value_type == str:
        return StringVar()
    else:
        raise ValueError("未定义变量类型")
