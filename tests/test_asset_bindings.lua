require("Asset")

assert(Asset_error() == "")

a = Asset:new()

assert(a:name() == "CDO")

assert(a:value() == 0.0)

