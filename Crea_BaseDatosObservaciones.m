close all
clear all
ir=0;

%% Radiales norte
D=kml2struct('RadialesNorteIEO.kml');
ir=ir+1;
Color{ir}='#bf3eff';
Lons{ir}=[D.Lon];
Lats{ir}=[D.Lat];
Nombre{ir}='Radiales';
plot(Lons{ir},Lats{ir},'b.'); hold on

for i1=1:length(Lons{ir})
    NombreEstaciones{ir}{i1}=sprintf('%03d',i1);
end


D=load('RadProfStations.mat');
ir=ir+1;
Color{ir}='#d57016';
Lons{ir}=D.lon';
Lats{ir}=D.lat';
Nombre{ir}='RadProf';
plot(Lons{ir},Lats{ir},'b.');
for i1=1:length(Lons{ir})
    NombreEstaciones{ir}{i1}=sprintf('%03d',i1);
end


%% STOCA
D=kml2struct('RadialesGolfoCadiz.kml');
ir=ir+1;
Color{ir}='#61a347';
Lons{ir}=[D.Lon];
Lats{ir}=[D.Lat];
Nombre{ir}='STOCA';
plot(Lons{ir},Lats{ir},'b.');
for i1=1:length(Lons{ir})
    NombreEstaciones{ir}{i1}=sprintf('%03d',i1);
end


D=load('RadmedStations.mat');
ir=ir+1;
Color{ir}='#e28b05';
Lons{ir}=[D.lonmalla]';
Lats{ir}=[D.latmalla]';
Nombre{ir}='RadMed';
plot(Lons{ir},Lats{ir},'.');
for i1=1:length(Lons{ir})
    NombreEstaciones{ir}{i1}=sprintf('%03d',i1);
end

%% Raprocan
D=load('RaprocanStations.mat');
ir=ir+1;
Color{ir}='#ff9999';
Lons{ir}=D.PointLon(D.indiceEST);
Lats{ir}=D.PointLat(D.indiceEST);
Nombre{ir}='Raprocan'
for i1=1:length(D.indiceEST)
    NombreEstaciones{ir}{i1}=D.PointName{D.indiceEST(i1)};
end
plot(Lons{ir},Lats{ir},'.');


% %%Boya AGl
% D=kml2struct('BoyaAGL.kml');
% ir=ir+1;
% Color{ir}='#ffffff';
% Lons{ir}=[D.Lon];
% Lats{ir}=[D.Lat];
% Nombre{ir}='BoyaAGL'
% plot(Lons{ir},Lats{ir},'b.');
%
%
% %%Mafeografos
% D=kml2struct('MareografosIEO.kml');
% ir=ir+1;
% Color{ir}='#ffffff';
% Lons{ir}=D.Lon;
% Lats{ir}=D.Lat;
% Nombre{ir}='Mareografos';
% plot(Lons{ir},Lats{ir},'b.');

save('HidrograPhicStations','Lons','Lats','Nombre','NombreEstaciones','Color')
