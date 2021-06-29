from gui import Interface

tool = Interface()
tool.init(f"迷你工具", "450x600")

from menu import init_menu

init_menu()

tool.run()
