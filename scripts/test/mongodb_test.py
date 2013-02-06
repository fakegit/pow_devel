#
# test for the mongoDB modules and classes
# will be removed if everything runs fine.
#
# khz 4.2.2013
#


from pow_mongodb_column import PowColumn as Column
c = Column('example_column', "String(50)", primary_key=True)
print c.to_json()
print dir(c)