from gui.interface import Message


class RunTimeData:
    """运行时数据"""
    _data = {}  # 程序数据
    _warn = {}  # 警告数据
    _components = []  # 运行程序对应的组件

    @classmethod
    def add_warning(cls, key, message):
        """程序运行中添加警告信息, key为标识, message添加到key对应的set中"""
        if key not in cls._warn:
            cls._warn[key] = set()
        cls._warn[key].add(str(message))
        Message.debug(f"运行时数据添加警告信息:{key},{message}")

    @classmethod
    def get_warning(self):
        """获取警告信息"""
        warn = {}
        for key, message_set in self._warn.items():
            warn_str = ",".join([str(i) for i in message_set])
            warn[key] = warn_str
        Message.debug(f"运行时数据获取警告数据:{warn}")
        return warn

    @classmethod
    def reset(cls):
        """重置数据"""
        cls._data = {}
        cls._warn = {}
        cls._components = []
        Message.debug('运行时数据重置')

    @classmethod
    def set_components(cls, components):
        """设置运行程序对应的组件"""
        cls._components = list(components)

    @classmethod
    def get_run_values(cls):
        """获取运行时对应的值"""
        values = []
        for component in cls._components:
            values.append(component.get())
        return values


class Data:
    """总程序数据"""
    pass

# class Feature:
#     """每个功能存放的数据"""
#
#     def __init__(self):
#         # 程序运行时的所有数据
#         self._data = {}  # 程序数据
#         self._warn = {}  # 警告信息
#
#     def add_warning(self, key, message):
#         """程序运行中添加警告信息, key为标识, message添加到key对应的set中"""
#         if key not in self._warn:
#             self._warn[key] = set()
#         self._warn[key].add(str(message))
#         logging.debug(f"添加警告信息:{key},{message}")
#
#     def get_warning(self):
#         """获取警告信息"""
#         warn = {}
#         for key, message_set in self._warn.items():
#             warn_str = ",".join([str(i) for i in message_set])
#             warn[key] = warn_str
#         return warn
#
#     def init(self, key, value=None):
#         """初始化数据"""
#         self._data[key] = value
#         logging.debug('功能数据初始化<{}:{}>'.format(key, value))
#
#     def set(self, key, value=None):
#         """修改数据"""
#         raw_data = self._data[key]
#         # 根据不同的数据类型对数据进行设置
#         if isinstance(raw_data, StringVar):
#             self._data[key].set(value)
#         else:
#             self._data[key] = value
#
#         logging.debug('功能数据修改<{}:{}>'.format(key, value))
#
#     def get(self, key, default=None):
#         """获取数据,如果要获取输入框的数据就单独处理"""
#         raw_value = self._data.get(key, default)
#         return_value = raw_value
#         if isinstance(raw_value, (Entry, Combobox, StringVar)):
#             return_value = raw_value.get()
#         elif isinstance(raw_value, Text):
#             # 从第一个字返回到最后一个字
#             return_value = raw_value.get(index1='1.0', index2=END)
#         logging.debug('功能数据获取<{}:{}>'.format(key, return_value))
#         return return_value
#
#     def run_reset(self):
#         """运行重置"""
#         self._warn = {}
#         logging.debug('运行重置')
#
#     def function_reset(self):
#         """功能重置"""
#         logging.debug('功能数据重置前<{}>,{}'.format(id(self), self._data, self._warn))
#         self._data = {}
#         self._warn = {}
#         logging.debug('功能数据重置后<{}>,{}'.format(id(self), self._data, self._warn))
