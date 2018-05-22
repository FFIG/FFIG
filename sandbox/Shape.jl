module FFIG

export Shape, Circle, Square, area, name, perimeter

mutable struct Shape
    ptr::Ptr{Void}
    Shape(ptr) = new(ptr)
end

function area(s::Shape)
    return ccall(("Shape_AbstractShape_area_noexcept", :libShape_c), Float64, (Ptr{Void},), s.ptr)
end

function perimeter(s::Shape)
    return ccall(("Shape_AbstractShape_perimeter_noexcept", :libShape_c), Float64, (Ptr{Void},), s.ptr)
end

function name(s::Shape)
    cstring = ccall(("Shape_AbstractShape_name_noexcept", :libShape_c), Cstring, (Ptr{Void},), s.ptr)
    return unsafe_string(cstring)
end

function Circle(r::Float64)
    p = Array{Ptr{Void}}(1)
    ccall(("Shape_Circle_create", :libShape_c), Int32, (Float64, Ptr{Ptr{Void}}), r, p)
    return Shape(p[1])
end

function Square(s::Float64)
    p = Array{Ptr{Void}}(1)
    ccall(("Shape_Square_create", :libShape_c), Int32, (Float64, Ptr{Ptr{Void}}), s, p)
    return Shape(p[1])
end

end # Module FFIG