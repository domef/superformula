import numpy as np
import pyvista as pv

from superformula import Superformula


class SuperformulaGUI:
    def __init__(self):
        self.resolution = 500
        self.superformula = Superformula()
        self.current_data = pv.PolyData()
        self.current_actor = None
        self.visualization_type = "point_cloud"
        self.update_data()

        self.plotter = pv.Plotter()
        self.event_type = "always"
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("resolution", x),
            rng=[100, 5000],
            value=self.resolution,
            title="resolution",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.89),
            pointb=(0.95, 0.89),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("a", x),
            rng=[-20, 20],
            value=self.superformula.a,
            title="a",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.76),
            pointb=(0.95, 0.76),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("b", x),
            rng=[-20, 20],
            value=self.superformula.b,
            title="b",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.63),
            pointb=(0.95, 0.63),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("m", x),
            rng=[-20, 20],
            value=self.superformula.m,
            title="m",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.50),
            pointb=(0.95, 0.50),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("n1", x),
            rng=[-20, 20],
            value=self.superformula.n1,
            title="n1",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.37),
            pointb=(0.95, 0.37),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("n2", x),
            rng=[-20, 20],
            value=self.superformula.n2,
            title="n2",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.24),
            pointb=(0.95, 0.24),
        )
        self.plotter.add_slider_widget(
            callback=lambda x: self.update("n3", x),
            rng=[-20, 20],
            value=self.superformula.n3,
            title="n3",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.11),
            pointb=(0.95, 0.11),
        )
        self.plotter.add_checkbox_button_widget(
            callback=lambda x: self.switch_visualization(x),
            value=False,
            position=(10.0, 10.0),
            color_on="green",
            color_off="green",
        )
        self.plotter.add_checkbox_button_widget(
            callback=lambda x: self.save_data(x),
            value=False,
            position=(70.0, 10.0),
            color_on="blue",
            color_off="blue",
        )

        self.update_visualization()
        self.plotter.show()

    def update(self, param, value):
        if param == "resolution":
            self.resolution = int(value)
        else:
            self.superformula.__dict__[param] = value
        self.update_data()

    def update_data(self):
        pc = self.superformula.point_cloud(self.resolution)
        if self.visualization_type == "point_cloud":
            new_data = pv.PolyData(pc)
        elif self.visualization_type == "mesh":
            triangles = self.superformula.triangulate(pc)
            arr3 = np.full((len(triangles), 1), 3)
            triangles_pv = np.concatenate([arr3, triangles], axis=1).flatten()
            new_data = pv.PolyData(pc, triangles_pv)
        self.current_data.overwrite(new_data)

    def update_visualization(self):
        if self.current_actor is not None:
            self.plotter.remove_actor(self.current_actor)

        if self.visualization_type == "point_cloud":
            self.current_actor = self.plotter.add_points(
                self.current_data, color="2192FF", render_points_as_spheres=True
            )
        elif self.visualization_type == "mesh":
            self.current_actor = self.plotter.add_mesh(self.current_data)

    def switch_visualization(self, value):
        self.visualization_type = "mesh" if value else "point_cloud"
        self.update_data()
        self.update_visualization()

    def save_data(self, value):
        self.current_data.save("./superformula.ply")
