close all; clear all
load Globales

%% Load configuration
configIEOOS
titulo="Sistema de observacion oceánica del IEO";


%CAN_perfiles_T_S_promedio.png
%CAN_SeccionTemporal_T.png
%CAN_temp_promedio_capas_contorno.png

%% Inicio
for iDem=1:1:5;
    FileHtmlClim=strcat(PaginaWebDir,'/html/','Clim_',Demarcaciones{1,iDem},'.html');

    fig1=strcat(Demarcaciones{1,iDem},'_temp_promedio10.png');
    fig2=strcat(Demarcaciones{1,iDem},'_perfiles_T_S_promedio.png');
    fig3=strcat(Demarcaciones{1,iDem},'_SeccionTemporal_T.png');
    fig4=strcat(Demarcaciones{1,iDem},'_temp_promedio_capas_contorno.png');

    fprintf('>>>>> %s\n',mfilename)
    fid = fopen(FileHtmlClim,'w');
    fprintf('     > Writting leaflet file \n');

    fprintf(fid,'<!--A Design by W3layouts\n');
    fprintf(fid,'Author: W3layout\n');
    fprintf(fid,'Author URL: http://w3layouts.com\n');
    fprintf(fid,'License: Creative Commons Attribution 3.0 Unported\n');
    fprintf(fid,'License URL: http://creativecommons.org/licenses/by/3.0/\n');
    fprintf(fid,'-->\n');

    fprintf(fid,'<html>\n');

    fprintf(fid,'<head>\n');
    fprintf(fid,'	<title>IEOOS</title>\n');
    fprintf(fid,'	<link href="css/bootstrap.css" rel="stylesheet" type="text/css" media="all" />\n');
    fprintf(fid,'	<!-- jQuery (necessary for Bootstrap JavaScript plugins) -->\n');
    fprintf(fid,'	<script src="js/jquery.min.js"></script>\n');
    fprintf(fid,'	<!-- Custom Theme files -->\n');
    fprintf(fid,'	<!--theme-style-->\n');
    fprintf(fid,'	<link href="css/style.css" rel="stylesheet" type="text/css" media="all" />\n');
    fprintf(fid,'	<!--//theme-style-->\n');
    fprintf(fid,'	<meta name="viewport" content="width=device-width, initial-scale=1">\n');
    fprintf(fid,'	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n');
    fprintf(fid,'	<meta name="keywords" content="IEOOS" />\n');
    fprintf(fid,'</head>\n');

    fprintf(fid,'<body>\n');

    fprintf(fid,'<!--SST-->\n');
    fprintf(fid,'	<div class="container">\n');
    fprintf(fid,'		<div class="blog">\n');
    fprintf(fid,'			<div class="top-blog">\n');
    fprintf(fid,'				<h2>Temperatura superficial del mar en la Demarcación %s</h2>\n',Demarcaciones{2,iDem});
    fprintf(fid,'			</div>\n');
    fprintf(fid,'			<br>\n');
    fprintf(fid,'			<p>Los datos de ... </a></p>\n');
    fprintf(fid,'			<br>\n');
    fprintf(fid,'			<div class="top-blog"></div>\n');
    fprintf(fid,'			<a href="https://www.oceanografia.es/IEOOS/Clim/images/%s"><img class="img-responsive" \n',fig1);
    fprintf(fid,'                    src="https://www.oceanografia.es/IEOOS/Clim/images/%s" \n',fig1);
    fprintf(fid,'					alt="" /></a><br>\n');
    fprintf(fid,'					<p>...</p>\n');
    fprintf(fid,'			<br>\n');

    fprintf(fid,'<!--Inicios items -->\n');
    fprintf(fid,'			<div class="blog-head">\n');
    fprintf(fid,'<!-------->\n');
    fprintf(fid,'				<div class="col-md-12 blog-bottom">\n');
    fprintf(fid,'					<div class=" blog-top">\n');
    fprintf(fid,'						<a href="https://www.oceanografia.es/IEOOS/Clim/images/%s"><img class="img-responsive"\n',fig2);
    fprintf(fid,'								src="https://www.oceanografia.es/IEOOS/Clim/images/%s" alt="" /></a>\n',fig2);
    fprintf(fid,'						<div class="blog-grid">\n');
    fprintf(fid,'							<h3>... </h3>\n');
    fprintf(fid,'							<p></p>\n');
    fprintf(fid,'						</div>\n');
    fprintf(fid,'					</div>\n');
    fprintf(fid,'				</div>\n');
    fprintf(fid,'<!----\n');

    fprintf(fid,'<!-------->\n');
    fprintf(fid,'				<div class="col-md-12 blog-bottom">\n');
    fprintf(fid,'					<div class=" blog-top">\n');
    fprintf(fid,'						<a href="https://www.oceanografia.es/IEOOS/Clim/images/%s"><img class="img-responsive"\n',fig3);
    fprintf(fid,'								src="https://www.oceanografia.es/IEOOS/Clim/images/%s" alt="" /></a>\n',fig3);
    fprintf(fid,'						<div class="blog-grid">\n');
    fprintf(fid,'							<h3>... </h3>\n');
    fprintf(fid,'							<p></p>\n');
    fprintf(fid,'						</div>\n');
    fprintf(fid,'					</div>\n');
    fprintf(fid,'				</div>\n');
    fprintf(fid,'<!----\n');

    fprintf(fid,'<!-------->\n');
    fprintf(fid,'				<div class="col-md-12 blog-bottom">\n');
    fprintf(fid,'					<div class=" blog-top">\n');
    fprintf(fid,'						<a href="https://www.oceanografia.es/IEOOS/Clim/images/%s"><img class="img-responsive"\n',fig4);
    fprintf(fid,'								src="https://www.oceanografia.es/IEOOS/Clim/images/%s" alt="" /></a>\n',fig4);
    fprintf(fid,'						<div class="blog-grid">\n');
    fprintf(fid,'							<h3>... </h3>\n');
    fprintf(fid,'							<p></p>\n');
    fprintf(fid,'						</div>\n');
    fprintf(fid,'					</div>\n');
    fprintf(fid,'				</div>\n');
    fprintf(fid,'<!----\n');


    fprintf(fid,'<!-------->\n');
    fprintf(fid,'<!--discalimer-->\n');
    fprintf(fid,'				<div class="services">\n');
    fprintf(fid,'					<div class="container">\n');
    fprintf(fid,'						<div class="top-services">\n');
    fprintf(fid,'							<p>Los datos proporcionados en estas páginas son sólamente a título informativo, por lo cual el Instituto Español de Oceanografia declinan toda responsabilidad por su uso.</p>\n');
    fprintf(fid,'						</div>\n');
    fprintf(fid,'					</div>\n');
    fprintf(fid,'				</div>\n');
    fprintf(fid,'<!----\n');

    fprintf(fid,'				<!--Fin items -->\n');
    fprintf(fid,'			</div>\n');
    fprintf(fid,'			<div class="clearfix"> </div>\n');
    fprintf(fid,'		</div>\n');
    fprintf(fid,'	</div>\n');
    fprintf(fid,'</body>\n');
    fprintf(fid,'</html>\n');




    %% Ftp the file
    fprintf('     > Uploading  %s \n',FileHtmlClim);
    ftpobj=FtpOceanografia;
    cd(ftpobj,ftp_dir_clim);
    mput(ftpobj,FileHtmlClim);

end

%% Writting Informe
%save(FileNameInforme,'Informe','platformes','juldsIB','platdatacentr')
%fprintf('     > %s \n',Informe)

fprintf('%s <<<<<\n',mfilename)