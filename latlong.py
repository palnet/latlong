from math import ceil

class Point():
	def __init__( self, lat, lng, num ):
		self.lat = lat
		self.lng = lng
		self.num = num
	
	def __eq__( self, other ):
		return self.num == other.num
	
	def __repr__( self ):
		return "Point( 0x" + str( "{:010x}".format( self.num ) ) + " )"
	def __str__( self ):
		return "Point( lat=" + "{:+07.3f}".format( self.lat ) + ", long=" + "{:+08.3f}".format( self.lng )+" )"

def encodeCoords( pts ):
	# returns encoded decimal value of all points
	
	if type( pts ) is not str:
		raise TypeError( "Parameter must be str" )
	if len( pts.split(" ") ) % 2:
		raise ValueError( "Incomplete point" )
	
	def lat( num ):
		if num < -90 or num > 90:
			raise ValueError( "Invalid latitude: "+str(num) )
		num += 90
		num /= 180
		num *= 2**19 - 1
		return round( num ) << 20 # don't combine to << 39, as rounding has to occur between operations
	
	def lng( num ):
		if num < -180 or num > 180:
			raise ValueError( "Invalid longitude: "+str(num) )
		num += 180
		num /= 360
		num *= 2**20 - 1
		return round( num )
	
	pts = pts.split(" ")
	encoded = 0
	
	for i in range(0, len( pts ), 2):
		lt = lat( float( pts[i] ) )
		lg = lng( float( pts[i+1] ) )
		
		encoded <<= 39 # first point is leftmost bits
		encoded += lt + lg
	
	return encoded

def decodeCoords( bits ):
	if type( bits ) is not int:
		raise TypeError( "Parameter must be int" )
	
	if bits < 0:
		raise ValueError( "Invalid value "+str(bits) )
	
	def lat( num ):
		num /= 2**19 - 1
		num *= 180
		return num-90
	
	def lng( num ):
		num /= 2**20 - 1
		num *= 360
		return num-180
	
	pts = []
	bitPts = []
	
	for i in range( ceil( bits.bit_length()/39 )|1 ): # break into array of points # |1 is for special case of (-90,-180)
		bitPts.insert( 0, (bits>>(39*i))&(2**39-1) ) # right shift 39*i bits, then AND last 39 bits
	
	for pt in bitPts:
		lt = pt >> 20
		lg = pt & (2**20 - 1)
		pts.insert( 0, Point(lat(lt), lng(lg), pt) )
	
	return pts
