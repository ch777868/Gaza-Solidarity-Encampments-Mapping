import folium
from folium import IFrame
import geopandas
import pandas as pd
import base64
import re
import os

# get_all_values gives a list of rows.
data = pd.read_excel("Gaza Solidarity Encampments/Encampments.xlsx")

# Convert to a DataFrame and render.
encampment_data = pd.DataFrame(data)

encampment_data['Latitude'] = pd.to_numeric(encampment_data['Latitude'], errors='coerce')
encampment_data['Longitude'] = pd.to_numeric(encampment_data['Longitude'], errors='coerce')
# encampment_data['Encampment Start Date'] = pd.to_datetime(encampment_data['Encampment Start Date'], errors='coerce', format='%Y-%m-%d')
# encampment_data['Date of raid/arrests'] = pd.to_datetime(encampment_data['Date of raid/arrests'], errors='coerce', format='%Y-%m-%d')
encampment_data['Location'] = encampment_data['City'].str.strip() + ", " + encampment_data['State'].str.strip()


# # Encampment Images
# path = 'Gaza Solidarity Encampments/Media'
# dir_list = os.listdir(path)
# print("Files and directories in '", path, "' :")
# # prints all files
# print(dir_list)

# encampment_data['Photo File Paths'] = dir_list  

# print(encampment_data)   
# Define USA coordinates
usa_coord = [37.0902, -95.7129] # Latitude, Longitude coord in decimal degrees
nyc_coord = [40.7128, -74.0060]
# Create USA map with folium wrapper around leaflet.js

usa_map = folium.Map(location=usa_coord, zoom_start=4.4)
folium.TileLayer('cartodbpositron').add_to(usa_map)

# Encampment Markers
## Map Icon
pal_flag = "Gaza Solidarity Encampments/673813_map_map marker_national_country_palestinian_pin_flag_palestine.png"
icon = folium.CustomIcon(pal_flag, icon_size=(60, 60))  # Adjust icon size as needed
    
## Map Loop

for index, row in encampment_data.iterrows():
   
    popup_html = f"""
        <!DOCTYPE html>
        <html>
        <h3 align="left" style="font-family:Calibri; color:red"><strong><u>{row['University Name']}</u><strong>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        </h3>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Location:</strong> {row['Location']}
        </h4>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Encampment Start Date:</strong> {row['Encampment Start Date']}
        </h4>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Status:</strong> {row['Status']}
        </h4>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Date of Raid/Arrests:</strong> {row['Date of raid/arrests']}
        </h4>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Number of Arrests:</strong> {row['Number of Arrests']}
        </h4>
        <h4 align="left" style="font-family:Calibri; color:green"> <strong>Source:</strong> <a href={row['Source']}><i>{row['University Name']}</i></a>
        </h4>
        
        """
        
    icon = folium.CustomIcon(pal_flag, icon_size=(60, 60))  # Adjust icon size as needed , icon_size=(50, 50)
    popup  = folium.Popup(popup_html, max_width=300)
    folium.vector_layers.Marker(location=[row['Latitude'],row['Longitude']],
                                popup = popup,
                                icon = icon,
                                tooltip=str(row['University Name'])).add_to(usa_map)

usa_map.save("encampments_map.html")
usa_map 

# for index, row in encampment_data.iterrows():
#         # Write the html code for the popups
#     html = folium.Html(
#             f"""
#             <!DOCTYPE html>
#             <html>
#             <h1 align="center" style="font-family:Calibri; color:red"><strong><u>{row['University Name']}</u><strong>
#             <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
#             <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"/>
#             </h1>
#             <!-- <p class="narrow" style="text-align: left;"> -->
#             <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">

#                 <div class="panel panel-default" style="text-align: left !important; border-color: #ffffff!important;">
#                     <div class="panel-heading" role="tab" id="headingOne" style="background: #ffffff!important;">
#                         <h4 class="panel-title" style="color:green">
#                             <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
#                                 <strong><i class="fa fa-map-marker"></i> Location <span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="float: right;"></span> </strong>
#                             </a>
#                         </h4>
#                     </div>
#                     <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingOne">
#                         <div class="panel-body" align="justify">
#                         {row['Location']}
#                         </div>
#                     </div>
#                 </div>

#                 <div class="panel panel-default" style="text-align: left !important; border-color: #ffffff!important;">
#                     <div class="panel-heading" role="tab" id="headingTwo" style="background: #ffffff!important;">
#                         <h4 class="panel-title" style="color:green">
#                             <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
#                                 <strong><i class="fa-solid fa-tents"></i> Encampment Start Date <span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="float: right;"></span> </strong>
#                             </a>
#                         </h4>
#                     </div>
#                     <div id="collapseThree" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
#                         <div class="panel-body" align="justify">
#                         {row['Encampment Start Date']}
#                     </div>
#                 </div>

#                 <div class="panel panel-default" style="text-align: left !important; border-color: #ffffff!important;">
#                     <div class="panel-heading" role="tab" id="headingThree" style="background: #ffffff!important;">
#                         <h4 class="panel-title" style="color:green">
#                             <a class="collapsed" role="button" data-toggle="collapse" data-parent="#accordion" href="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
#                                 <strong><i class="fa-solid fa-handcuffs"></i> Police/State Violence <span class="glyphicon glyphicon-menu-down" aria-hidden="true" style="float: right;"></span> </strong>
#                             </a>
#                         </h4>
#                     </div>
#                     <div id="collapseFour" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">
#                         <div class="panel-body" align="justify">
#                         {row['Police/State Violence']}
#                         </div>
#                     </div>
#                 </div>
#             </div>

# </html>
#             """,
#             script=True)
#         # Create the popup
#     icon = folium.CustomIcon(pal_flag, icon_size=(60, 60))  # Adjust icon size as needed , icon_size=(50, 50)
#     popup  = folium.Popup(html, max_width=500)
#     folium.vector_layers.Marker(location=[row['Latitude'],row['Longitude']],
#                                 popup = popup,
#                                 icon = icon,
#                                 tooltip=str(row['University Name'])).add_to(usa_map)
#             # <center>
#             #     <img src="{row['University Name']}.gif" width="400" style="border-radius: 50px;"/>
#             # </center>
# usa_map

