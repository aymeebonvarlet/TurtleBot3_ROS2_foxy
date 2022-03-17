
import working_on_foxy as wf
import math
import constants as c

def calcul_barycentre(d_debut,d_fin, theta):
    y_a=-d_debut*math.tan(theta/2)
    y_b=d_debut*math.tan(theta/2)
    y_c=-d_fin*math.tan(theta/2)
    y_d=d_fin*math.tan(theta/2)
    base_basse=y_b-y_a
    base_haute=y_d-y_c
    h=d_fin-d_debut
    barycentre_x= (h/3) * (base_basse+2*base_haute)/(base_haute+base_basse)
    barycentre_y=d_debut + (base_haute-base_basse)/2
    return [barycentre_x, barycentre_y]
    
def calcul_centre_people(x_gauche, x_droit, y_gauche,y_droit):
    x=abs((x_gauche-x_droit)/2)
    y=abs((y_droit-y_gauche)/2)
    return [x,y]

def follow_me():
    t_barycentre=calcul_barycentre(c.d_debut, c.d_fin, c.theta)
    
    
    
    
    
    
    