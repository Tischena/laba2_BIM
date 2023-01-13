import NemAll_Python_Geometry as geometry
import NemAll_Python_BaseElements as baseElements
import NemAll_Python_BasisElements as basisElements
import NemAll_Python_Utility as utility
import geometryValidate as geometryValidate
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties

def create_el(build_ele, doc):
    element = balka(doc)
    return element.create(build_ele)

def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True

def move_handle(build_ele, handle_prop, input_pnt, doc):
    build_ele.change_property(handle_prop, input_pnt)
    return create_el(build_ele, doc)

class balka:

    def create(self, build_ele):
        self.top(build_ele)
        self.handle(build_ele)
        return (self.model_ele_list, self.handle_list)

    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def top(self, build_ele):
        c = geometry.a.CreateCuboid(geometry.AxisPlacement3D(geometry.point(0 - (build_ele.Width.value - build_ele.length.value) / 2, 0, 
        build_ele.depth.value + build_ele.height.value), geometry.Vector3D(1, 0, 0), geometry.Vector3D(0, 0, 1)), build_ele.Width.value, build_ele.width.value, build_ele.dep.value)
        c_plate = geometry.a.CreateCuboid( geometry.AxisPlacement3D(geometry.point(build_ele.PlateSpace.value - (build_ele.Width.value - build_ele.length.value) / 2,
        0, build_ele.depth.value + build_ele.height.value + build_ele.dep.value), geometry.Vector3D(1, 0, 0),
        geometry.Vector3D(0, 0, 1)), build_ele.Width.value - build_ele.PlateSpace.value*2, build_ele.width.value, build_ele.plheight.value)
        com_prop = baseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_ele.color.value
        balka_width_top = build_ele.balkaWidth.value
        if balka_width_top > 0:
            b = utility.VecSizeTList()
            b.append(8)
            b.append(10)
            err, c = geometry.balkaCalculus.Calculate( c, b, balka_width_top, False)
            if not geometryValidate.polyhedron(err):
                return
        err, ok = geometry.MakeUnion( c, self.center(build_ele))
        err, ok = geometry.MakeUnion(ok, c_plate)
        self.model_ele_list.append( basisElements.ModelElement3D(com_prop, ok))

    def center(self, build_ele):
        c = geometry.a.CreateCuboid( geometry.AxisPlacement3D(geometry.point(build_ele.length.value / 2 - build_ele.centralWidth.value / 2, 0, 
        build_ele.depth.value),geometry.Vector3D(1, 0, 0),geometry.Vector3D(0, 0, 1)),build_ele.centralWidth.value, build_ele.width.value,
        build_ele.height.value)
        cone = geometry.a.CreateCylinder(geometry.AxisPlacement3D(geometry.point(build_ele.balkawidth.value, 
        build_ele.width.value / 8, build_ele.depth.value + build_ele.height.value / 2),geometry.Vector3D(0, 0, 1),geometry.Vector3D(1, 0, 0)),
        build_ele.Radius.value , build_ele.centralWidth.value)
        cone1 = geometry.a.CreateCylinder(geometry.AxisPlacement3D(geometry.point(build_ele.balkawidth.value, 
        build_ele.width.value - build_ele.width.value / 8, build_ele.depth.value + build_ele.height.value / 2),geometry.Vector3D(0, 0, 1),
        geometry.Vector3D(1, 0, 0)), build_ele.Radius.value , build_ele.centralWidth.value)
        err, c = geometry.MakeSubtraction(c, cone)
        err, c = geometry.MakeSubtraction(c, cone1)
        err, ok = geometry.MakeUnion(c, self.bottom(build_ele))
        return ok

    def bottom(self, build_ele):
        c = geometry.a.CreateCuboid(geometry.AxisPlacement3D(geometry.point(0, 0, 0), geometry.Vector3D(1, 0, 0), geometry.Vector3D(0, 0, 1)),
        build_ele.length.value, build_ele.width.value, build_ele.depth.value)
        c_inter = geometry.a.CreateCuboid(geometry.AxisPlacement3D(geometry.point(0, 0, 0), geometry.Vector3D(1, 0, 0), geometry.Vector3D(0, 0, 1)),
        build_ele.length.value, build_ele.width.value, build_ele.depth.value)
        balka_width = build_ele.balkawidth.value
        balka_width_bottom = build_ele.balkaWidthBottom.value
        if balka_width_bottom > 0:
            b = utility.VecSizeTList()
            b.append(8)
            b.append(10)
            err, c_inter = geometry.balkaCalculus.Calculate(c_inter, b, balka_width_bottom, False)
            if not geometryValidate.polyhedron(err):
                return
        err, ok = geometry.MakeIntersection(c, c_inter)
        return ok
        if balka_width_bottom > 0:
            b = utility.VecSizeTList()
            b.append(8)
            b.append(10)
            err, c_inter = geometry.balkaCalculus.Calculate(c_inter, b, balka_width_bottom, False)
            if not geometryValidate.polyhedron(err):
                return
        err, ok = geometry.MakeIntersection(c, c_inter)
        return ok

    def handle(self, build_ele):
        direct1 = geometry.point( build_ele.length.value / 2, build_ele.width.value, build_ele.height.value + build_ele.depth.value)
        direct2 = geometry.point( build_ele.length.value / 2, 0, build_ele.depth.value / 2)
        direct3 = geometry.point( 0, build_ele.width.value, (build_ele.depth.value - build_ele.balkawidth.value) / 2)
        direct4 = geometry.point( 0 - (build_ele.Width.value - build_ele.length.value) / 2, build_ele.width.value, build_ele.height.value + build_ele.depth.value + build_ele.balkaWidth.value)
        direct5 = geometry.point( build_ele.length.value / 2, build_ele.width.value, build_ele.height.value + build_ele.depth.value - build_ele.depth.value / 4)
        direct6 = geometry.point( build_ele.length.value / 2, build_ele.width.value, build_ele.height.value + build_ele.depth.value + build_ele.dep.value)
        direct7 = geometry.point( build_ele.length.value / 2, build_ele.width.value, 0)
        direct8 = geometry.point( build_ele.length.value / 2 - build_ele.centralWidth.value / 2, build_ele.width.value, build_ele.height.value / 2 + build_ele.depth.value)
        self.handle_list.append( HandleProperties("height", geometry.point(direct1.X, direct1.Y, direct1.Z), geometry.point(direct1.X, direct1.Y,
        direct1.Z - build_ele.height.value), [("height", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append( HandleProperties("width", geometry.point(direct2.X, direct2.Y + build_ele.width.value, direct2.Z), geometry.point(direct2.X,
        direct2.Y, direct2.Z), [("width", HandleDirection.y_dir)], HandleDirection.y_dir, False))
        self.handle_list.append( HandleProperties("length", geometry.point(direct3.X + build_ele.length.value, direct3.Y, direct3.Z), geometry.point(
        direct3.X, direct3.Y, direct3.Z), [("length", HandleDirection.x_dir)], HandleDirection.x_dir, False))
        self.handle_list.append( HandleProperties("Width", geometry.point(direct4.X + build_ele.Width.value, direct4.Y, direct4.Z), 
        geometry.point(direct4.X,direct4.Y,direct4.Z),[("Width", HandleDirection.x_dir)], HandleDirection.x_dir, False))
        self.handle_list.append(HandleProperties("dep", geometry.point(direct5.X, direct5.Y, direct5.Z + build_ele.dep.value),
        geometry.point(direct5.X,direct5.Y,direct5.Z),[("dep", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append( HandleProperties("plheight", geometry.point(direct6.X, direct6.Y, direct6.Z + build_ele.plheight.value),
        geometry.point(direct6.X,direct6.Y,direct6.Z),[("plheight", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append( HandleProperties("depth", geometry.point(direct7.X, direct7.Y, direct7.Z + build_ele.depth.value),
        geometry.point(direct7.X,direct7.Y,direct7.Z),[("depth", HandleDirection.z_dir)], HandleDirection.z_dir, False))
        self.handle_list.append( HandleProperties("centralWidth", geometry.point(direct8.X + build_ele.centralWidth.value, direct8.Y, direct8.Z),
        geometry.point(direct8.X, direct8.Y, direct8.Z), [("centralWidth", HandleDirection.x_dir)], HandleDirection.x_dir, False))
