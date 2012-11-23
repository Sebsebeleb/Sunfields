"""
Random map generation

TO CONSIDER:
All the functions that require a world/zone should probably be methods
of the zone/world class instead.
"""

import itertools
import random
random.seed()
snapname = 0

class World():
	def __init__(self, size):

		self.world = []
		for x in range(size[0]):
			self.world.append([])
			for y in range(size[1]):
				self.world[x].append(Tile(self, (x,y)))

class Tile():
	ttype = None
	colour = (0,0,0)


	def __init__(self, parent, pos):
		self.pos = pos
		self.x,self.y = pos
		self.parent = parent
		self.neighboors = []

	def __repr__(self):
		return "%s at %s"%(self.ttype,self.pos)

	def find_neighboors(self):
		self.neighboors = []
		try:
			self.neighboors.append(self.parent.tiles[self.x][self.y+1])
		except IndexError:	pass
		try:
			self.neighboors.append(self.parent.tiles[self.x+1][self.y])
		except IndexError: pass
		if self.y > 0:
			self.neighboors.append(self.parent.tiles[self.x][self.y-1])
		if self.x > 0:
			self.neighboors.append(self.parent.tiles[self.x-1][self.y])

		print "Remaining neighboors: " + str(self.neighboors)

	def find_close(self, distance, allowedtiles = None, start_cost = None, cost_decline = 1):
		visited = []
		totalcost = 0
		start_cost = start_cost or distance
		allowedtiles = allowedtiles or [self]
		print "Startcost: %s"%(start_cost,)

		allowedtiles = type(self)

		current_cost = start_cost
		unvisited = [tuple([t for t in self.neighboors if isinstance(t,allowedtiles)])]
		#totalcost += len(unvisited)*current_cost
		print len(unvisited)

		while len(unvisited) and distance > 0:
			handling = unvisited.pop()
			totalcost += len(handling) * current_cost
			print "len(handling): %s current_cost: %s"%(len(handling), current_cost)
			current_cost -= cost_decline
			distance -= 1
			for tile in handling:
				if distance > 0:
					newtiles = tuple([t for t in tile.neighboors if t not in visited and t in allowedtiles])
					unvisited.append(newtiles)
					visited.append(tile)
		self.populated = totalcost


	def transform_into(self, new):
		global snapname
		self.parent.tiles[self.x][self.y] = new(self.parent, self.pos)
		SavePNG(self.parent, "C:\Users\Sebsebeleb\Desktop\mapgen\steps\\" + str(snapname)+".png")
		snapname += 1


class LandTile(Tile):
	ttype = "land"
	colour = (0, 220, 0)

class WaterTile(Tile):
	ttype = "water"
	colour = (0,0,255)

class Zone():
	tiles = []

	def __init__(self, origin, size, density = 1.0, ):
		self.origin = origin
		self.density = density
		self.tiles = []
		self.size = size
		for x in range(size[0]):
			self.tiles.append([])
			for y in range(size[1]):
				self.tiles[x].append(LandTile(self, (origin[0]+x,origin[1]+y)))

	def find_neighboors(self):
		for x in self.tiles:
			for y in x:
				y.find_neighboors()

	def densify(self, density =  1.0, xscale = 1.0, yscale = 1.0, roundness = "round"):
		"""
		Turns the zone into an island by randomly turning grass tiles to
		water tiles, water tiles father away from the center are more likely to be transformed.

		Density: higher means more water
		xscale and yscale: one higher than the other will make the island longer across that axis
		roundness: Which method will be used for calculating water transformation;
			"round": the island will look smooth and round
			"diamond": The island will resemble a square rotated 45 degrees
		"""

		for a in self.tiles:
			for t in a:
				r = random.random()
				c = self._diamond_dense(t) * density #random treshold
				print "%s lower than %s?"%(r,c)
				if r < c:
					print "Transforming"
					t.transform_into(WaterTile)

	def _round_dense(self, tile):
		pass

	def _diamond_dense(self, tile):
		midx, midy = (self.size[0]/2,self.size[1]/2) #the center of the zone
		return (float((abs(midx-tile.pos[0]) + abs(midy-tile.pos[1]))) / float(midx +midy)) #chance for a tile to be removed

	def remove_lone(self, old, new):
		for a in self.tiles:
			print a
			for t in a:
				#print "Moving on to " + str(t)
				transform = 1
				for n in [i for i in t.neighboors if isinstance(i, old)]:
					print n
					if isinstance(n, old):
						#print "It is!"
						transform = 0
				if transform == 1:
					#print "Transforming %s"%(t)
					t.transform_into(new)

def find_road_path(start, stop):
	x,y = start.pos
	goal = stop.pos

	while (x,y) != goal:
		while x:
			pass

def eliminate_lowpops(zone, oldtile, insta_treshhold, r, factor = 1.0, newtile = WaterTile):
	"""
	Any tile with lower than insta_treshhold is transformed, the others
	have n% chance to be deleted, where n = factor * population / r (times something)
	"""

	#tiles = []
	for i in zone.tiles:
		for t in i:
			t.find_close(r)
			#tiles.append(t)

	for i in zone.tiles:
		for t in i:
			print "t: %s"%(t)
			if not isinstance(t, oldtile):
				continue
			print "%s < %s?"%(t.populated,insta_treshhold)
			if t.populated < insta_treshhold:
				print "it is!"
				t.transform_into(newtile)
				#tiles.remove(t)




def found_cities(self, zone, numberof):
	"""
	To consider:
	Maybe this function shouldnt call find_close
	"""
	for i in zone.tiles:
		for t in i:
			t.find_close(5)

	reversed(sorted(tiles, key = lambda t: t.populated))


def SavePNG(World, f = "C:\Users\Sebsebeleb\Desktop\mapgen\final.png"):
	import png

	p = []
	for n,x in enumerate(World.tiles):
		p.append([])
		for y in World.tiles[n]:
			for c in y.colour:
				p[n].append(c)

	saver = png.from_array(p, "RGB")
	saver.save(f)



def main():
	snapshots = 1	#0 is disabled, only the final state will be saved, 1 is some, 2 is one picture for every modification
	savelocation = "C:\Users\Sebsebeleb\Desktop\mapgen\\"

	z = Zone((0,0),(10,10))
	SavePNG(z, savelocation+"1.png")
	z.densify(1.0)
	SavePNG(z, savelocation+"2.png")
	z.find_neighboors()
	z.remove_lone(LandTile, WaterTile)
	SavePNG(z, savelocation+"3.png")
	z.find_neighboors()
	z.remove_lone(WaterTile, LandTile)
	SavePNG(z, savelocation+"4.png")
	z.find_neighboors()
	print "eliminate!"
	a = raw_input()
	eliminate_lowpops(z, LandTile, 80, 5)
	SavePNG(z, f = savelocation + "final.png")


if __name__ == "__main__":
	main()
