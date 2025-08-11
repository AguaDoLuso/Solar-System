# Imports -----------------------------------------------------
import pygame as pg
import math

# Initialize pygame -------------------------------------------
pg.init()
WIDTH, HEIGHT = 900, 900
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Solar_System SimV1")
icon = pg.image.load('solar-system.png')
pg.display.set_icon(icon)

# Colors -----------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

L_BLUE = (100, 149, 237)    # Custom Light Blue
L_RED = (188, 39, 50)       # Custom Light Red

D_GREY = (80, 78, 81)       # Custom Dark Grey

# Astro Class ------------------------------------------------
class Astro:
    AU = 1.49597e8 * 1000     # Astronomical Unit in meters 
    G =  6.67428e-11    # Gravitational Constant
    SCALE = 250 / AU    # 1AU = 200 pixels  Notes: I want to ajust this at will
    TIMESTEP = 3600 * 24    # 1 day         Notes: I want to ajust this at will, also see the current date solar position
    
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius               # Notes: I want to predeterminate the radius in order of the mass (it can manually be inserted later)
        self.color = color                 # Notes: Could make it random if you dont insert
        self.mass = mass                   # Notes: I want to predeterminate the mass in order of the raidus (it can manually be inserted later)
        
        self.orbit = []     # save all the points of the orbit to draw it
        self.sun = False
        self.distance_to_sun = 0        # :(
        
        self.dx = 0     # delta x vel
        self.dy = 0     # delta y vel
        
    def draw(self, window):    # Draws Astro
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:    # needs at least 3 points
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))
            pg.draw.lines(window, self.color, False, updated_points, 2)    # Draw Orbit
        pg.draw.circle(window, self.color, (x,y), self.radius)      # Draw Astro
        
    def remove(self, win):  # Removes Astro
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pg.draw.circle(win, BLACK, (x,y), self.radius)
        
    def attraction(self, other):    # calculates the gravitational force of 2 bodies
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt((distance_x**2) + (distance_y**2))    # Pythagoras Teorem to find the distance
        if other.sun:
            self.distance_to_sun = distance     # Notes: Could be better to save on calculations
            
        gravForce = (Astro.G * self.mass * other.mass) / (distance**2)
        theta = math.atan2(distance_y, distance_x)  # Find the theta angle on the Pythagoras Triangle
        gravForce_x = math.cos(theta) * gravForce   # Trigonometry
        gravForce_y = math.sin(theta) * gravForce   # Trigonometry
        return gravForce_x, gravForce_y
        
    def update_position(self, astral_bodies):
        total_fx = total_fy = 0
        for bodie in astral_bodies:
            if self == bodie:   # needs at least 2 bodies to calculate 
                continue
            fx, fy = self.attraction(bodie)
            total_fx += fx
            total_fy += fy
        
        self.dx += total_fx / self.mass * self.TIMESTEP      # F = m / a  <=> a = F / m, total the aceleration that it gains in 1 day 
        self.dy += total_fy / self.mass * self.TIMESTEP
        self.x += self.dx * self.TIMESTEP
        self.y += self.dy * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def init_solar_system():
    AU = Astro.AU
# Sun -------------------------------
    MASS_SUN = 1.98892e30   # Sun Mass in kg
    sun = Astro(0, 0, 30, YELLOW, MASS_SUN)
    sun.sun = True
# Mercury --------------------------
    MASS_MERCURY = 3.3e23
    mercury = Astro(0.387*AU, 0, 8, D_GREY, MASS_MERCURY)
    mercury.dy = 47.4 * 1000  # mercury velocity in meters
# Venus ----------------------------
    MASS_VENUS = 4.8685e24
    venus = Astro(0.723*AU, 0, 14, WHITE, MASS_VENUS)   # Notes: Want to change the color
    venus.dy = -35.02 * 1000    # venus velocity in meters
# Earth ----------------------------
    MASS_EARTH = 5.9742e24  # Earth Mass in kg
    earth = Astro(AU, 0, 16, L_BLUE, MASS_EARTH)
    earth.dy = 29.783 * 1000    # earth velocity velocity in meters
# Mars -----------------------------
    MASS_MARS = 6.39e23
    mars = Astro(1.524*AU, 0, 12, L_RED, MASS_MARS)
    mars.dy = 24.077 * 1000      # mars velocity in meters
# Jupiter --------------------------
# Saturn ---------------------------
# Uranus ---------------------------
# Neptune --------------------------
    
    Astral_Bodies = [sun, mercury, venus, earth, mars]
    return Astral_Bodies

# Main Loop --------------------------------------------------

def main(): 
    astral_bodies = init_solar_system()
    
    run = True
    clock = pg.time.Clock()
    while run:
        clock.tick(60)  # makes the Simulation run cap on 60 fps
        #WINDOW.fill(BLACK)
        for event in pg.event.get(): 
            if event.type == pg.QUIT:
                run = False
            
        for body in astral_bodies:
            body.remove(WINDOW)
            body.update_position(astral_bodies)     
            body.draw(WINDOW)       # Notes: verify if the Astros are out of the window, if they are dont draw, just keep up with the numbers
            
        pg.display.update()
    pg.quit()
            
main()
