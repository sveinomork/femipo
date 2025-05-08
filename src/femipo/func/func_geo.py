import numpy as np

from shapely.geometry import Point


from vectormath import Vector3
from scipy.spatial.transform import Rotation as R

def rotate_point_origin_euler(point:Point,seq:str, angels:list,degrees:bool=False)->Point:
    """
    Parameters: 
    point: Point
        Specify the Point Point(X_coor,y_coor,z_corr)
    seqs : string
        Specifies sequence of axes for rotations. Up to 3 characters belonging to the set {str(x), str(y},str(z)} for 
        intrinsic rotations, or {str(x), str(y), str(z)} for extrinsic rotations. 
        Extrinsic and intrinsic rotations cannot be mixed in one function call.

    angles:  array_like 
        Euler angles specified in radians (degrees is False) or degrees (degrees is True). For a single character seq, angles can be:
        array_like with shape (W,) where W is the width of seq, which corresponds to a single rotation with W axes.

    degrees: bool, optional
        If True, then the given angles are assumed to be in degrees. Default is False.

    Returns:
        rotated point :Point
    
    Examples:
        >>> p = Point(1, 0, 0)
        >>> rotate_point_origin_euler(p, seq='z', angles=[90], degrees=True)
        Point(0.000, 1.000, 0.000)

        >>> p = Point(0, 1, 0)
        >>> rotate_point_origin_euler(p, seq='x', angles=[np.pi / 2])
        Point(0.000, 1.000, 0.000)  # stays the same because rotation is about x-axis

        >>> p = Point(1, 0, 0)
        >>> rotate_point_origin_euler(p, seq='zyx', angles=[90, 0, 0], degrees=True)
        Point(0.000, 1.000, 0.000)
    
    """
    # point converted to  np array like
    p=np.array([point.x,point.y,point.z])
    # euler rotation matrix 
    r=R.from_euler(seq,angels,degrees).as_matrix()
    # rotated point as np array like
    rotated_point=np.matmul(r,p.reshape(3,1))
    return Point(rotated_point[0],rotated_point[1],rotated_point[2])

    
def z_rotation_point(point:Point, origin:Point, degrees:float)->Point:
    """Rotates 3-D point around z-axis"""    
    radians = np.deg2rad(degrees)
    x=point.x
    x,y,z = point.x,point.y,point.z
    offset_x, offset_y = origin.x,origin.y
    adjusted_x = (x - offset_x)
    adjusted_y = (y - offset_y)
    cos_rad = np.cos(radians)
    sin_rad = np.sin(radians)
    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
    return Point(qx, qy,z)




def get_planeq(po:Point,normal:Vector3)->np.ndarray:
        
    d=1*po.x*normal.x +normal.y*po.y+normal.z*po.z
    return np.array([normal.x, normal.y, normal.z, d]) # i.e. A = 2, B = -8, C = 5, D = -18

def get_planeq3P(pp1:Point,pp2:Point,pp3:Point)->np.ndarray:
   

    p1 = np.array([pp1.x, pp1.y, pp1.z])
    p2 = np.array([pp2.x, pp2.y, pp2.z])
    p3 = np.array([pp3.x, pp3.y, pp3.z])

    # These two vectors are in the plane
    v1 = p3 - p1
    v2 = p2 - p1

    # the cross product is a vector normal to the plane
    cp = np.cross(v1, v2)
    a, b, c = cp

    # This evaluates a * x3 + b * y3 + c * z3 which equals d
    d = np.dot(cp, p3)
    return np.array([a, b, c, d]) 

def calc_new_point(center: Point, p2: Point, alfa: float) -> Point:
        # Calculate the angle of p2 relative to center
        current_angle = np.atan2(p2.y - center.y, p2.x - center.x)
        
        # Calculate radius from the given point
        r = np.sqrt((p2.x - center.x)**2 + (p2.y - center.y)**2)
        
        # Calculate new angle by adding alfa (converted to radians)
        new_angle = current_angle + np.radians(alfa)
        
        # Calculate new coordinates
        x3 = center.x + r * np.cos(new_angle)
        y3 = center.y + r * np.sin(new_angle)
        
        return Point(x3, y3, p2.z)


def mirror_point(point:Point,po:Point,vector:Vector3)->Point:
    """
    Mirror a point across a plane defined by a point and a vector.
    Args:
        point (Point): The point to be mirrored.
        po (Point): A point on the plane of reflection.
        vector (Vector3): A vector normal to the plane of reflection.
    Returns:
        Point: The mirrored point.
    """
    # Calculate the dot product of the vector and the difference between the point and the plane point
    dot_product = (point.x - po.x) * vector.x + (point.y - po.y) * vector.y + (point.z - po.z) * vector.z
    
    # Calculate the mirrored coordinates
    x_mirror = point.x - 2 * dot_product * vector.x
    y_mirror = point.y - 2 * dot_product * vector.y
    z_mirror = point.z - 2 * dot_product * vector.z
    
    return Point(x_mirror, y_mirror, z_mirror)  


