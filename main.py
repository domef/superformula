from gui import SuperformulaGUI
import open3d.visualization.gui as gui


if __name__ == '__main__':
    gui.Application.instance.initialize()
    _ = SuperformulaGUI()
    gui.Application.instance.run()
