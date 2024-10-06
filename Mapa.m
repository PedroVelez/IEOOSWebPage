clear all; close all; clc;

%Para Batimetria
% Op.lat_min=24.25;
% Op.lat_max=29.50;
% Op.lon_min=340;
% Op.lon_max=352;

lat_min=24;
lat_max=45;
lon_min=-20;
lon_max= 5;

%% Mapa estaciones
figure
m_proj('mercator','lat',[lat_min lat_max], 'long',[lon_min lon_max]);

%Batimetria
BAT=load('EspanhaBat.mat');
[CS,CH]=m_contourf(BAT.batylon,BAT.batylat,BAT.elevations,40,'edgecolor','none');hold on
caxis([min(min(BAT.elevations)) 0])
colormap(m_colmap('blues'));
set(gcf,'color','w');

%Estaciones
Estaciones=load('./Estaciones/HidrograPhicStations.mat');
for ir=1:5
    m_plot(Estaciones.Lons{ir},Estaciones.Lats{ir},'o','markersize',4,'MarkerEdgeColor','k','MarkerFaceColor','k')
end

%Costa
m_usercoast('EspanhaCoast.mat','patch',[.7 .6 .4,],'edgecolor',[.7 .6 .4,]);
m_grid('linestyle',':','fontsize',10)


