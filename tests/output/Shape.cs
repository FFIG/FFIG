// This code was generated by FFIG <http://ffig.org>.
// Manual edits will be lost.
using System;
using System.Runtime.InteropServices;

namespace Shape {

  public class Exception : System.Exception {

    [DllImport("libShape_c.dylib")]    
    private static extern void Shape_clear_error();

    [DllImport("libShape_c.dylib")]    
    private static extern IntPtr Shape_error();
  
    public Exception() : base(Marshal.PtrToStringAnsi(Shape_error())) {
      Shape_clear_error();
    }
  }

  public class AbstractShape {

    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_AbstractShape_dispose(IntPtr c_obj);  
  
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_AbstractShape_area(IntPtr c_obj, out double rv);
  
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_AbstractShape_perimeter(IntPtr c_obj, out double rv);
  
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_AbstractShape_name(IntPtr c_obj, out IntPtr rv);
  
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_AbstractShape_is_equal(IntPtr c_obj, IntPtr s, out int rv);
  
    protected IntPtr c_obj_;
  
    ~AbstractShape() {
      Shape_AbstractShape_dispose(c_obj_);
    }
  
    public double area() {
      double rv;
      int rc = Shape_AbstractShape_area(c_obj_, out rv);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
      return rv;
    }
  
    public double perimeter() {
      double rv;
      int rc = Shape_AbstractShape_perimeter(c_obj_, out rv);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
      return rv;
    }
  
    public string name() {
      IntPtr rv = IntPtr.Zero;
      int rc = Shape_AbstractShape_name(c_obj_, out rv);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
      return Marshal.PtrToStringAnsi(rv);
    }
  
    public int is_equal(AbstractShape s) {
      int rv;
      int rc = Shape_AbstractShape_is_equal(c_obj_, s.c_obj_, out rv);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
      return rv;
    }
  }
  
  public class Circle : Shape.AbstractShape {
    
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_Circle_create(double radius, out IntPtr ptr);
    
    public Circle(double radius) {
      int rc = Shape_Circle_create(radius, out c_obj_);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
    }
  }
  
  public class Square : Shape.AbstractShape {
    
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_Square_create(double side, out IntPtr ptr);
    
    public Square(double side) {
      int rc = Shape_Square_create(side, out c_obj_);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
    }
  }
  
  public class Pentagon : Shape.AbstractShape {
    
    [DllImport("libShape_c.dylib")]    
    private static extern int Shape_Pentagon_create(double side, out IntPtr ptr);
    
    public Pentagon(double side) {
      int rc = Shape_Pentagon_create(side, out c_obj_);
      if(rc != 0) { 
        throw new Shape.Exception();
      }
    }
  }
  
}