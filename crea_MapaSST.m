close all; clear all
load Globales

%% Load configuration
configIEOOS

titulo="Temperatura superficial del mar en las demarcaciones Españolas.";


%% Inicio
fprintf('>>>>> %s\n',mfilename)
fid = fopen(FileHtmMapaSST,'w');
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
fprintf(fid,'		.leaflet-container {height: 700px;width: 700px;max-width: 100%;max-height: 100%;}\n');
fprintf(fid,'	</style>\n');
fprintf(fid,'	<style>#map { width: 700px; height: 700px; }\n');
fprintf(fid,'        .info { padding: 6px 8px; font: 14px/16px Arial, Helvetica, sans-serif; background: white; background: rgba(255,255,255,0.8); box-shadow: 0 0 15px rgba(0,0,0,0.2); border-radius: 5px; } .info h4 { margin: 0 0 5px; color: #777; }\n');
fprintf(fid,'        .legend { text-align: left; line-height: 18px; color: #555; } .legend i { width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7; }\n');
fprintf(fid,'    </style>\n');
fprintf(fid,'</head> \n');

fprintf(fid,'<body> \n');

% Titulo
fprintf(fid,'    <div align="center">\n');
fprintf(fid,'        %s<br/>\n',titulo);
fprintf(fid,'         Actualizado el %s .<br/>\n',date);
fprintf(fid,'        <div id="map" style="width: 700px; height: 700px;"></div> \n');
fprintf(fid,'    </div>\n');

fprintf(fid,'<script type="text/javascript">\n');

%Poligono con demarcaciones
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
    fprintf(fid,'    polygon%3s.bindPopup("<center>Haz click en el vínculo para acceder a: </br> -<a href=\''https://www.oceanografia.es/IEOOS/SST/SST_%3s.html''> Temperatura superfical promedio en la Demarcacion marina %s</a></center>") \n',Demarcaciones{1,iD},Demarcaciones{1,iD},Demarcaciones{2,iD});
    %fprintf(fid,'// Add a click event with a popup\n');
    %fprintf(fid,'    polygon%3s.on(''click'', function(e) {\n',Demarcaciones{1,iD});
    %fprintf(fid,'    var popup = L.popup().setLatLng(e.latlng)\n');
    %fprintf(fid,'        .setContent("<center><a href=\''https://www.oceanografia.es/IEOOS/SST/SST_%3s.html''>Demarcacion marina %s</a></center>") \n',Demarcaciones{1,iD},Demarcaciones{2,iD});
    %fprintf(fid,'        .openOn(demarcaciones);});\n');
end


%% Estaciones
fprintf(fid,'const capaestaciones = L.layerGroup();\n');
fprintf(fid,'    // Define markers (example: three locations)\n');
fprintf(fid,'    var estaciones = [\n');
fprintf(fid,'           [1,''001'',42.22,-8.79,''Radiales'',''14-Jan-2020 00:10:40'',''SurfaceValue'',''BottonValue'',''#bf3eff''], \n');
fprintf(fid,'           [1,''002'',42.21,-8.85,''Radiales'',''14-Jan-2020 00:10:40'',''SurfaceValue'',''BottonValue'',''#bf3eff''], \n');
fprintf(fid,'           [1,''003'',42.14,-8.96,''Radiales'',''14-Jan-2020 00:10:40'',''SurfaceValue'',''BottonValue'',''#bf3eff''], \n');
fprintf(fid,'           [1,''004'',42.13,-9.12,''Radiales'',''14-Jan-2020 00:10:40'',''SurfaceValue'',''BottonValue'',''#bf3eff''], \n');
fprintf(fid,'           [1,''005'',43.36,-8.37,''Radiales'',''14-Jan-2020 00:10:40'',''SurfaceValue'',''BottonValue'',''#bf3eff''], \n');
fprintf(fid,'		];    \n');

fprintf(fid,'let markers = [];\n');
    
fprintf(fid,'    for (var i = 0; i < estaciones.length; i++) {\n');
fprintf(fid,'		  estacion = estaciones[i];\n');
fprintf(fid,'		  if(estacion[0] == 1){\n');
fprintf(fid,'			  markers[i] = L.circleMarker([estacion[2], estacion[3]],\n');
fprintf(fid,'            {radius : 3,\n');
fprintf(fid,'            color  : estacion[8],\n');
fprintf(fid,'            fillColor:estacion[8],\n');
fprintf(fid,'            opacity: 1,\n');
fprintf(fid,'            fillOpacity:.45,\n');
fprintf(fid,'            title: estacion[4]+estacion[1]+'' ''+estacion[5],\n');
fprintf(fid,'            }).addTo(capaestaciones).bindPopup(''<center><p>Estación <b><a href="http://www.oceanografia.es/IEOOS/estaciones/''+estacion[4]+''_''+estacion[1]+''.html" target="_blank">''+estacion[1]+''</a></b><br><b>''+estacion[4]+''</b><br><br><b>Last profile&nbsp;</b>''+estacion[5]+''</p></center>'');\n');
fprintf(fid,'		  }else if (estacion[0] == 0) {\n');
fprintf(fid,'			  markers[i] = L.circleMarker([estacion[2], estacion[3]],\n');
fprintf(fid,'            {radius : 3,\n');
fprintf(fid,'            color  : estacion[8],\n');
fprintf(fid,'            fillColor:estacion[8],\n');
fprintf(fid,'            opacity: 1,\n');
fprintf(fid,'            fillOpacity:.45,\n');
fprintf(fid,'            title: estacion[4]+estacion[1]+'' ''+estacion[5],\n');
fprintf(fid,'            }).addTo(capaestaciones).bindPopup(''<center><p>Estación <b><a href="http://www.oceanografia.es/IEOOS/estaciones/''+estacion[4]+''_''+estacion[1]+''.html" target="_blank">''+estacion[1]+''</a></b><br><b>''+estacion[4]+''</b><br><br><b>Last profile&nbsp;</b>''+estacion[5]+''</p></center>'');\n');
fprintf(fid,'		}\n');
fprintf(fid,'	}\n');


% Initialize the map and set up control
fprintf(fid,'// Initialize the map and set up control\n');
fprintf(fid,'  const map = L.map(''map'',{\n');
fprintf(fid,'                scrollwheelzoom: false, \n');
fprintf(fid,'                center: [37, -8],\n');
fprintf(fid,'                zoom: 5,\n');
fprintf(fid,'                layers: [capademarcaciones],\n');
fprintf(fid,'              });\n');
fprintf(fid,'  map.addControl(new L.Control.Fullscreen());\n');

% Add default map
fprintf(fid,'//Tiles\n');
fprintf(fid,'    const tiles = L.tileLayer(''https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'', {\n');
fprintf(fid,'       attribution: ''Tiles &copy ESRI''}).addTo(map);\n');

%Control de capas
fprintf(fid,'// Layer control\n');
fprintf(fid,'        var overlayLayers = {\n');
fprintf(fid,'          "Demarcaciones": capademarcaciones,\n');
fprintf(fid,'          "Estaciones": capaestaciones,\n');
fprintf(fid,'        };\n');
fprintf(fid,'        L.control.layers(null,overlayLayers,{collapsed:false}).addTo(map);\n');

% Añade la leyenda
fprintf(fid,'//Leyenda\n');
fprintf(fid,'    var legend = L.control({position: ''bottomright''});\n');
fprintf(fid,'    legend.onAdd = function (map) {\n');
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
fprintf(fid,'    legend.addTo(map);\n');

fprintf(fid,'</script> \n');
fprintf(fid,'</body>\n');
fprintf(fid,'</html>\n');

%% Ftp the file
fprintf('     > Uploading  %s \n',FileHtmMapaSST);
ftpobj=FtpOceanografia;
cd(ftpobj,ftp_dir_SST);
mput(ftpobj,FileHtmMapaSST);

%% Writting Informe
%save(FileNameInforme,'Informe','platformes','juldsIB','platdatacentr')
%fprintf('     > %s \n',Informe)

fprintf('%s <<<<<\n',mfilename)