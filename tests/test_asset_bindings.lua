require("Asset")

a = Asset:new()
assert(a.name()=="I'm afraid I can't do that")
assert(a.value()=="I'm afraid I can't do that")

assert(Asset_error() == "")
