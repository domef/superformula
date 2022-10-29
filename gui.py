import pyvista as pv

from superformula import Superformula


class SuperformulaGUI:
    def __init__(self):
        self.resolution = 0.05
        self.superformula = Superformula()
        self.current = pv.PolyData()
        self.update_point_cloud()

        self.plotter = pv.Plotter()
        self.event_type = "always"
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("resolution", value),
            rng=[0.001, 0.1],
            value=self.resolution,
            title="resolution",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.89),
            pointb=(0.95, 0.89),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("a", value),
            rng=[-20, 20],
            value=self.superformula.a,
            title="a",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.76),
            pointb=(0.95, 0.76),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("b", value),
            rng=[-20, 20],
            value=self.superformula.b,
            title="b",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.63),
            pointb=(0.95, 0.63),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("m", value),
            rng=[-20, 20],
            value=self.superformula.m,
            title="m",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.50),
            pointb=(0.95, 0.50),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("n1", value),
            rng=[-20, 20],
            value=self.superformula.n1,
            title="n1",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.37),
            pointb=(0.95, 0.37),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("n2", value),
            rng=[-20, 20],
            value=self.superformula.n2,
            title="n2",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.24),
            pointb=(0.95, 0.24),
        )
        self.plotter.add_slider_widget(
            callback=lambda value: self.update("n3", value),
            rng=[-20, 20],
            value=self.superformula.n3,
            title="n3",
            style="modern",
            event_type=self.event_type,
            pointa=(0.75, 0.11),
            pointb=(0.95, 0.11),
        )

        self.plotter.add_points(
            self.current, color="2192FF", render_points_as_spheres=True
        )
        self.plotter.show()

    def update(self, param, value):
        if param == "resolution":
            self.resolution = value
        else:
            self.superformula.__dict__[param] = value
        self.update_point_cloud()

    def update_point_cloud(self):
        pc = self.superformula.point_cloud(self.resolution)
        self.current.overwrite(pv.PolyData(pc))
