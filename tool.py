from gui import Interface
from menu import load_menu

tool = Interface()
tool.init(f"迷你工具", "450x600")

load_menu()

tool.run()
