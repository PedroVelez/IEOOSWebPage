% Here are the variables used by the different programs

%% General settings
titulo_webpage="Sistema de observación oceánica del IEO";
domainName='http://www.oceanografia.es/IEOOS';

Verbose=0;
Visible=0;      %Flag to outpun in the screen the figures
SubeFTP=1;      %1 to upload from matlab de figures and web page to the ftp.

%% Input Directories and files
% Directory where the matlab scripts than update the web page are located
PaginaWebDir=strcat(GlobalSU.AnaPath,'/IEOOSWebpage');

dirDemarcaciones=strcat(PaginaWebDir,"/LimiteDemarcaciones/");

Demarcaciones={'CAN',       'NOR',         'SUD',         'ESA',               'LEB';...
               'Canaria',   'Noratlántica','Sudatlántica','Estrecho y Alborán','Levantino-Balear'; ...
                '#bf3eff',  '#d57016',     '#61a347',     '#e28b05',           '#ff9999'};


%% Output Directories and files
%Directory to output the graphic files
DirOutGraph=strcat(PaginaWebDir,'/images');


%Names of the outputs files
FileHtmMapaSST = strcat(PaginaWebDir,'/html/','MapaSST.html');
FileHtmlIEOOSStatus=strcat(PaginaWebDir,'/html/','IEOOSStatusLL.html');


%% Geographical Regions
lat_minIB= 15.00; lat_maxIB=54;
lon_minIB=-45;    lon_maxIB=38;
%Atlantico
lat_min=-65;    lat_max=65;
lon_min=-80;    lon_max=40;

%Map limits
GMCentroArgoIb=[39,-16];
GMZoomArgoIb=4;
GMTamanoArgoIb=[700,650];


%% Ftp
ftp_dir='/html/IEOOS';
ftp_dir_SST='/html/IEOOS/SST';
ftp_dir_status='/html/IEOOS/html_files';

