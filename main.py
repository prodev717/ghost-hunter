from ursina import *
from ursina.prefabs import first_person_controller,health_bar

from random import randint as ran
from random import uniform as uni
import sys

class ghost(Button):
	no=[]
	def __init__(self):
		super().__init__(parent=scene,model="model/ghost.obj",texture="texture/white.png",position=(ran(-490,490),0,ran(-490,490)),
			            collider="box",scale=uni(0.5,1.3),color=color.white,highlight_color=color.blue)
		self.follow=self.add_script(SmoothFollow(target=player,offset=[0,1,0],speed=uni(0.01,0.4)))
		self.alive=True
		ghost.no.append(self)
	def kill(self,regenerate=False):
		self.animate_color(color.white50,1)
		self.texture="texture/black.png"
		self.alive=False
		try:
			self.scripts.remove(self.follow)
			ghost.no.remove(self)
			if regenerate:
				ghost()
		except:
			print("")
	def update(self):
		global player,hb
		if self.alive:
			d=distance(player.position,self.position)
			if d<5:hb.value-=0.1
	def input(self,key):
		global player
		if self.hovered:
			if key=="left mouse up":
				if distance(player.position, self.position)<5:
					ghost.kill(self,regenerate=True)

class Tree(Button):
	def __init__(self):
		super().__init__(parent=scene,model="model/Tree.glb",position=(ran(-490,490),ran(1,4),ran(-490,490)),scale=ran(15,20),
			             collider="box",color=color.white,highlight_color=color.red)
	def input(self,key):
		global player
		if self.hovered:
			if key=="left mouse up":
				if distance(player.position, self.position)<8:
					destroy(self)

def out():
	destroy(sw)
	destroy(ins)
	tex.text="you lost"
	tex.x=-0.11
	fil=Entity(parent=camera,model="cube",texture="radial_gradient",color=color.rgba(200,0,0,0),z=0.9)
	fil.animate_color(color.white10,3)
	invoke(sys.exit,delay=5)

def update():
	if player.intersects(tower).hit and player.y>13:
		hb.value=100		
		tex.x=-0.10
		tex.text="you won"
		s.texture="sky_default"
		for i in ghost.no:
			i.kill()
	if hb.value==0:
		out()
	if held_keys["q"]:
		sys.exit()
	if held_keys["left shift"]:
		player.speed=15
	else:
		player.speed=5
	
def input(key):
	if key=="left mouse down":
		sw.animate_z(1)
	if key=="left mouse up":
		sw.animate_z(0.3)

game=Ursina()
window.exit_button.enabled=False
window.fullscreen=True

s=Sky(texture="sky_sunset")
ground=Entity(model="plane",texture="grass",scale=1000,double_sided=True,collider="mesh")
player=first_person_controller.FirstPersonController(position=(ran(-490,490),0,ran(-490,490)),model="cube",collider="box",color=color.rgba(100,100,100,0))
hb=health_bar.HealthBar(bar_color=color.lime)
tex = Text("find and reach the tower",scale=2,y=-0.45,x=-0.25)
ins = Text("a,w,s,d - movement\nleft shift - sprint\nleft click - attack\nspace - jump\nq - exit",x=-0.8,y=-0.37)
sw=Entity(model="model/sword.obj",texture="texture/s1.png",scale=0.008,parent=camera,rotation=(50,40,10),position=(0.2,-0.1,0.3))
tower=Entity(model="model/tower.obj",texture="texture/towertex.jpg",scale=2.5,collider="mesh",position=(ran(-490,490),-3.05,ran(-490,490)))

for i in range(1000):
	Tree()
for i in range(15):
	ghost()

game.run()