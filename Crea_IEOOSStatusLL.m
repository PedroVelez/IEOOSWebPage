close all; clear all
load Globales

%% Load configuration
configIEOOS
titulo="Sistema de observacion oceánica del IEO";
mapTamano=[700,700];
mapCenter=[37, -8];
mapZoom=5;


%% Inicio
fprintf('>>>>> %s\n',mfilename)
fid = fopen(FileHtmlIEOOSStatus,'w');
fprintf('     > Writting leaflet file \n');

fprintf(fid,'<!DOCTYPE html>\n');
fprintf(fid,'<html> \n');
fprintf(fid,'<head> \n');
fprintf(fid,'	<title>%s</title> \n',titulo_webpage);
fprintf(fid,'	<meta charset="utf-8" /> \n');
fprintf(fid,'	<meta name="viewport" content="width=device-width, initial-scale=1.0"> \n');

%Leaflet libraries
fprintf(fid,'   <link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/> \n');
fprintf(fid,'   <script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js" integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew==" crossorigin=""></script>\n');
fprintf(fid,'   <script src=''https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js''></script> \n');
fprintf(fid,'   <link href=''https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css'' rel=''stylesheet'' /> \n');
fprintf(fid,'	<style>\n');
fprintf(fid,'		html, body {height: 100%;margin: 0;}\n');
fprintf(fid,'		.leaflet-container {width: %dpx; height: %dpx;max-width: 100%;max-height: 100%;}\n',mapTamano(1),mapTamano(2));
fprintf(fid,'	</style>\n');
fprintf(fid,'	<style>#map { width: %dpx; height: %dpx; }\n',mapTamano(1),mapTamano(2));
fprintf(fid,'        .info { padding: 6px 6px; font: 14px/16px Arial, Helvetica, sans-serif; background: white; background: rgba(255,255,255,0.8); box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px; } .info h4 { margin: 0 0 5px; color: #777; }\n');
fprintf(fid,'        .legend { text-align: left; line-height: 18px; color: #555; } .legend i { width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7; }\n');
fprintf(fid,'    </style>\n');
fprintf(fid,'</head> \n');

fprintf(fid,'<body> \n');

%% Titulo
fprintf(fid,'    <div align="center">\n');
fprintf(fid,'        Cobertura del sistema de observacion oceanica del <b>IEO</b> el %s <br/>\n',date);
fprintf(fid,'        (24) Estaciones hidrograficas. Último dato recibido el  %s <br/>\n',date);
fprintf(fid,'        <div id="map" style="width: %d px; height: %d px;"></div> \n',mapTamano(1),mapTamano(2));
fprintf(fid,'    </div>\n');

fprintf(fid,'<script type="text/javascript">\n');

%% Poligono con demarcaciones
fprintf(fid,'// Define el poligono de cada demarcacion\n');
fprintf(fid,'const capademarcaciones = L.layerGroup();\n');

for iD=1:5
    codeDemarcacion=Demarcaciones{1,iD};
    d=load(strcat(dirDemarcaciones,'/Demarcacion',Demarcaciones{1,iD},'.txt'));
    fprintf(fid,'    var polygon%3s = L.polygon([\n    ',Demarcaciones{1,iD});
    for i1=1:length(d)
        fprintf(fid,'[%4.2f,%5.2f],',d(i1,2),d(i1,1));
    end
    fprintf(fid,'    ]).addTo(capademarcaciones);\n');
    fprintf(fid,'    polygon%3s.setStyle({fillColor: ''%s'',color: ''%s'',fillOpacity: 0.5});  \n',Demarcaciones{1,iD},Demarcaciones{3,iD},Demarcaciones{3,iD});
    fprintf(fid,'    polygon%3s.bindPopup("<center><b>Demarcación marina %s</b></br>Haz click en el vínculo para acceder a: </br> - <a href=\''https://www.oceanografia.es/IEOOS/SST/SST_%s.html'' target=''_blank''>Temperatura superfical promedio</a> </br> - <a href=\''https://www.oceanografia.es/IEOOS/Clim/Clim_%3s.html'' target=''_blank''>Temperatura promedio</a> </center>") \n',Demarcaciones{1,iD},Demarcaciones{2,iD},Demarcaciones{1,iD},Demarcaciones{1,iD});
    %fprintf(fid,'    polygon%3s.bindPopup("<center><b>Demarcación marina %s</b> </br> Haz click en el vínculo para acceder a: </br> - <a href=''https://www.oceanografia.es/IEOOS/SST/SST_%s.html'' target=''_blank''>Temperatura superficial promedio</a> </br> - <a href=''https://www.oceanografia.es/IEOOS/Clim/Clim_%s.html'' target=''_blank''>Temperatura promedio</a> </center>") \n',Demarcaciones{1,iD},Demarcaciones{1,iD},Demarcaciones{2,iD});
end





%% Estaciones
fprintf(fid,'//Datos de las ultimas ocupaciones de las estaciones\n'); 
fprintf(fid,'const capaestaciones = L.layerGroup();\n');
fprintf(fid,'    // Define markers (example: three locations)\n');
fprintf(fid,'    var estaciones = [\n');
Estaciones=load('./Data/HidrograPhicStations.mat');
for ir=1:length(Estaciones.Nombre)
     for ie=1:length(Estaciones.Lons{ir})
         NombreRadial=Estaciones.Nombre{ir};
         NombreEstacion=char(Estaciones.NombreEstaciones{ir}(ie));
         %SurfaceValue=sprintf('%3.0fdbar %4.1fC %4.1f',pres(np,iSV),tems(np,iSV),sals(np,iSV));
         %BottonValue=sprintf('%3.0fdbar %4.1fC %4.1f',pres(np,iBV),tems(np,iBV),sals(np,iBV));
         fprintf(fid,'           [1,''%s'',%4.2f,%4.2f,''%s'',''%s'',''%s'',''%s'',''%s''], \n', NombreEstacion,Estaciones.Lats{ir}(ie),Estaciones.Lons{ir}(ie),NombreRadial,'14-Jan-2020 00:10:40','SurfaceValue','BottonValue',Estaciones.Color{ir});
     end
 end
fprintf(fid,'		];\n');  

fprintf(fid,'let markers = [];\n');   
fprintf(fid,'    for (var i = 0; i < estaciones.length; i++) {\n');
fprintf(fid,'		  estacion = estaciones[i];\n');
fprintf(fid,'		  if(estacion[0] == 0){\n');
fprintf(fid,'			  markers[i] = L.circleMarker([estacion[2], estacion[3]],\n');
fprintf(fid,'            {radius : 3,\n');
fprintf(fid,'            color  : estacion[8],\n');
fprintf(fid,'            fillColor:estacion[8],\n');
fprintf(fid,'            opacity: 1,\n');
fprintf(fid,'            fillOpacity:.45,\n');
fprintf(fid,'            title: estacion[4]+estacion[1]+'' ''+estacion[5],\n');
fprintf(fid,'            }).addTo(capaestaciones).bindPopup(''<center><p>Estación <b><a href="http://www.oceanografia.es/IEOOS/estaciones/''+estacion[4]+''_''+estacion[1]+''.html" target="_blank">''+estacion[1]+''</a></b><br><b>''+estacion[4]+''</b><br><br><b>Last profile&nbsp;</b>''+estacion[5]+''</p></center>'');\n');
fprintf(fid,'		  }else if (estacion[0] == 1) {\n');
fprintf(fid,'			  markers[i] = L.circleMarker([estacion[2], estacion[3]],\n');
fprintf(fid,'            {radius : 3,\n');
fprintf(fid,'            color  : estacion[8],\n');
fprintf(fid,'            fillColor:estacion[8],\n');
fprintf(fid,'            opacity: 1,\n');
fprintf(fid,'            fillOpacity:.45,\n');
fprintf(fid,'            title: estacion[4]+estacion[1]+'' ''+estacion[5],\n');
fprintf(fid,'            }).addTo(capaestaciones).bindPopup(''<center><p>Estación <b><a href="%s/estaciones/''+estacion[4]+''_''+estacion[1]+''.html" target="_blank">''+estacion[1]+''</a></b><br><b>''+estacion[4]+''</b><br><br><b>Last profile&nbsp;</b>''+estacion[5]+''</p></center>'');\n',domainName);
fprintf(fid,'		}\n');
fprintf(fid,'	}\n');

% Añade la leyenda Demarcaciones
fprintf(fid,'//Leyenda demarcaciones\n');
fprintf(fid,'    var legendDem = L.control({position: ''bottomright''});\n');
fprintf(fid,'    legendDem.onAdd = function (map) {\n');
fprintf(fid,'    function getColor(d) {\n');
fprintf(fid,'        return d === "%s" ? "#bf3eff" :\n',Demarcaciones{2,1});
fprintf(fid,'               d === "%s" ? "#d57016" :\n',Demarcaciones{2,2});
fprintf(fid,'               d === "%s" ? "#61a347" :\n',Demarcaciones{2,3});
fprintf(fid,'               d === "%s" ? "#e28b05" :\n',Demarcaciones{2,4});
fprintf(fid,'               d === "%s" ? "#ff9999" :\n',Demarcaciones{2,5});
fprintf(fid,'               "#ff7f00";\n');
fprintf(fid,'    }');
fprintf(fid,'    var div = L.DomUtil.create(''div'', ''info legend'');\n');
fprintf(fid,'    labels = [''<strong>Demarcaciones</strong>''],\n');
fprintf(fid,'    categories = [''%s'',''%s'', ''%s'',''%s'',''%s''];\n',Demarcaciones{2,1},Demarcaciones{2,2},Demarcaciones{2,3},Demarcaciones{2,4},Demarcaciones{2,5});
fprintf(fid,'    for (var i = 0; i < categories.length; i++) {\n');
fprintf(fid,'            div.innerHTML += \n');
fprintf(fid,'            labels.push(\n');
fprintf(fid,'               ''<i class="circle" style="background:'' + getColor(categories[i]) + ''"></i>'' +\n');
fprintf(fid,'            (categories[i] ? categories[i] : ''+''));}\n');
fprintf(fid,'        div.innerHTML = labels.join(''<br>'');\n');
fprintf(fid,'    return div;\n');
fprintf(fid,'    };\n');

fprintf(fid,'//Leyenda\n'); 
fprintf(fid,'    var legendEst = L.control({position: ''bottomright''});\n'); 
fprintf(fid,'    legendEst.onAdd = function (map) {\n'); 
fprintf(fid,'    function getColor(d) {\n'); 
fprintf(fid,'        return d === "Campaña - Radiales" ? "#bf3eff" :\n'); 
fprintf(fid,'               d === "Campaña - RadProf"  ? "#d57016" :\n'); 
fprintf(fid,'               d === "Campaña - STOCA"    ? "#61a347" :\n'); 
fprintf(fid,'               d === "Campaña - RadMed"   ? "#e28b05" :\n'); 
fprintf(fid,'               d === "Campaña - Raprocan" ? "#ff9999" :\n');                
fprintf(fid,'               "#ff7f00";\n'); 
fprintf(fid,'    }\n');
fprintf(fid,'    var div = L.DomUtil.create(''div'', ''info legend'');\n'); 
fprintf(fid,'    labels = [''<strong>Observaciones</strong>''],\n'); 
fprintf(fid,'    categories = [''Campaña - Radiales'',''Campaña - RadProf'', ''Campaña - STOCA'',''Campaña - RadMed'',''Campaña - Raprocan''];\n'); 
fprintf(fid,'    for (var i = 0; i < categories.length; i++) {\n'); 
fprintf(fid,'            div.innerHTML += \n'); 
fprintf(fid,'            labels.push(\n'); 
fprintf(fid,'               ''<i class="circle" style="background:'' + getColor(categories[i]) + ''"></i>'' +\n'); 
fprintf(fid,'            (categories[i] ? categories[i] : ''+''));}\n'); 
fprintf(fid,'        div.innerHTML = labels.join(''<br>'');\n'); 
fprintf(fid,'    return div;\n'); 
fprintf(fid,'    };\n'); 

% Initialize the map and set up control
fprintf(fid,'// Initialize the map and set up control\n');
fprintf(fid,'  const map = L.map(''map'',{\n');
fprintf(fid,'                scrollwheelzoom: false, \n');
fprintf(fid,'                center: [%d, %d],\n',mapCenter(1),mapCenter(2));
fprintf(fid,'                zoom: %d,\n',mapZoom);
fprintf(fid,'                layers: [capademarcaciones],\n');
fprintf(fid,'              });\n');
fprintf(fid,'  map.addControl(new L.Control.Fullscreen());\n');

% Añador leyende por defectos
fprintf(fid,'  legendDem.addTo(map);\n');

% Add default map
fprintf(fid,'//Tiles\n');
fprintf(fid,'    const tiles = L.tileLayer(''https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'', {\n');
fprintf(fid,'       attribution: ''Tiles &copy ESRI''}).addTo(map);\n');

% Funciones para cambiar de leyenda
fprintf(fid,'// Function to update legends when layers change\n');
fprintf(fid,'map.on(''overlayadd'', function (eventLayer) {\n');
fprintf(fid,'    if (eventLayer.name === ''Demarcaciones'') {\n');
fprintf(fid,'        legendDem.addTo(map);\n');
fprintf(fid,'    } else if (eventLayer.name === ''Estaciones'') {\n');
fprintf(fid,'        legendEst.addTo(map);\n');
fprintf(fid,'    }\n');
fprintf(fid,'});\n');

fprintf(fid,'map.on(''overlayremove'', function (eventLayer) {\n');
fprintf(fid,'    if (eventLayer.name === ''Demarcaciones'') {\n');
fprintf(fid,'        map.removeControl(legendDem);\n');
fprintf(fid,'    } else if (eventLayer.name === ''Estaciones'') {\n');
fprintf(fid,'        map.removeControl(legendEst);\n');
fprintf(fid,'    }\n');
fprintf(fid,'});\n');


%Control de capas
fprintf(fid,'// Layer control\n');
fprintf(fid,'        var overlayLayers = {\n');
fprintf(fid,'          "Demarcaciones": capademarcaciones,\n');
fprintf(fid,'          "Estaciones": capaestaciones,\n');
fprintf(fid,'        };\n');
fprintf(fid,'        L.control.layers(null,overlayLayers,{collapsed:false}).addTo(map);\n');

fprintf(fid,'</script> \n');
fprintf(fid,'</body>\n');
fprintf(fid,'</html>\n');

%% Ftp the file
fprintf('     > Uploading  %s \n',FileHtmlIEOOSStatus);
ftpobj=FtpOceanografia;
cd(ftpobj,ftp_dir_status);
mput(ftpobj,FileHtmlIEOOSStatus);

%% Writting Informe
%save(FileNameInforme,'Informe','platformes','juldsIB','platdatacentr')
%fprintf('     > %s \n',Informe)

fprintf('%s <<<<<\n',mfilename)