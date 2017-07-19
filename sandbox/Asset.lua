local ffi = require("ffi")
ffi.cdef[[
  const char* Asset_error();
  void Asset_clear_error(); 
  int Asset_CDO_create(void** p); 
  int Asset_Asset_value(void* asset, double* v); 
  int Asset_Asset_name(void* asset, const char** v); 
]]

local libAsset = ffi.load("Asset_c")

Asset = {}
Asset.__index = Asset

function Asset_error()
  return ffi.string(libAsset.Asset_error())
end

function Asset:new(o)
  o = o or {}
  setmetatable(o, self)
  self.__index = self
  ptr = ffi.new("void*[1]")
  libAsset.Asset_CDO_create(ptr)
  o.ptr = ptr[0]
  return o
end       

function Asset:value()
  v = ffi.new("double[1]")
  rc = libAsset.Asset_Asset_value(self.ptr, v)
  return v[0]
end

function Asset:name()
  v = ffi.new("const char*[1]")
  rc = libAsset.Asset_Asset_name(self.ptr, v)
  return ffi.string(v[0])
end

