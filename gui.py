from functools import partial
from superformula import Superformula
import numpy as np
import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering


class SuperformulaGUI(object):

    def __init__(self, step: float = 0.04):
        self._step = step
        self._size = 100
        self._color = [1., 0., 0.]

        self._superformula = Superformula()

        self._window = gui.Application.instance.create_window("Superformula", 1000, 750)
        self._scene = gui.SceneWidget()
        self._scene.scene = rendering.Open3DScene(self._window.renderer)
        self._load_point_cloud()

        em = self._window.theme.font_size
        self._settings = gui.Vert(0, gui.Margins(0.25 * em, 0.25 * em, 0.25 * em, 0.25 * em))

        self._sf_items = []
        for k, v in self._superformula.__dict__.items():
            label = gui.Label(k)
            slider = gui.Slider(gui.Slider.DOUBLE)
            slider.double_value = float(v)
            slider.set_on_value_changed(partial(self._on_update, key=k))
            slider.set_limits(-20, 20)
            self._sf_items.append(label)
            self._sf_items.append(slider)

        for item in self._sf_items:
            self._settings.add_child(item)

        self._window.add_child(self._scene)
        self._window.add_child(self._settings)
        self._window.set_on_layout(self._on_layout)

    def _on_layout(self, theme):
        r = self._window.content_rect
        self._scene.frame = r
        width = 16 * theme.font_size
        height = min(r.height, self._settings.calc_preferred_size(theme).height)
        self._settings.frame = gui.Rect(r.get_right() - width, r.y, width, height)

    def _on_update(self, value, key):
        self._superformula.__dict__[key] = value
        self._load_point_cloud()

    def _load_point_cloud(self):
        self._scene.scene.clear_geometry()
        pc = self._superformula.point_cloud(self._step) * self._size
        pc = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(pc))
        pc = pc.paint_uniform_color(np.array(self._color))
        self._scene.scene.add_geometry('superformula', pc, rendering.Material())
