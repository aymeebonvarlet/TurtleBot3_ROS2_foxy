
import working_on_foxy as wf
import math
import constants as c
import recovery_data_lidar as rdl

def area_barycentre(d_debut,d_fin, theta):
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

def go_to():
    x_pied=rdl.Recovery_data.feet_barrycentre()[0]
    y_pied=rdl.Recovery_data.feet_barrycentre()[1]

    x_centre = area_barycentre()[0]
    y_centre = area_barycentre()[1]

    return [x_pied-x_centre, y_pied-y_centre]

# def calcul_barycentre_object(tab_coor):
#     tab_moy = sum(tab_coor)/len(tab_coor)
#     print(tab_moy)
#     return tab_moy



    

   
    
    
    