
import working_on_foxy as wf
import math
import constants as c
import recovery_data_lidar as rdl

# def calcul_barycentre(d_debut,d_fin, theta):
#     y_a=-d_debut*math.tan(theta/2)
#     y_b=d_debut*math.tan(theta/2)
#     y_c=-d_fin*math.tan(theta/2)
#     y_d=d_fin*math.tan(theta/2)
#     base_basse=y_b-y_a
#     base_haute=y_d-y_c
#     h=d_fin-d_debut
#     barycentre_x= (h/3) * (base_basse+2*base_haute)/(base_haute+base_basse)
#     barycentre_y=d_debut + (base_haute-base_basse)/2
#     return [barycentre_x, barycentre_y]
    
def calcul_barycentre_object(tab_coor):
    tab_moy = sum(tab_coor)/len(tab_coor)
    print(tab_moy)
    return 0



    

   
    
    
    