#! /bin/zsh
source $HOME/.zshrc
source $HOME/.env

## Settings based on computer
strval=$(uname -a)
if [[ $strval == *EemmMBP* ]];
then
  analisisDir=$HOME/Dropbox/Oceanografia/Analisis/IEOOSWebPAge
  pythonDir=$HOME/miniconda3/envs/ocean/bin/python
fi
if [[ $strval == *rossby* ]];
then
  analisisDir=$HOME/Analisis/IEOOSWebPage
  pythonDir=/opt/conda/envs/ocean/bin/python
fi

/bin/rm $analisisDir/updateSSTGlobal.log
/bin/touch $analisisDir/updateSSTGlobal.log

printf ">>>> Updating IEOOSWeb page \n"
printf "   > $strval\n"

#------------------------------------
#Inicio
#------------------------------------
printf "   > Directorio $analisisDir \n"

printf "   > Download data from current year SSTs \n"
$pythonDir $analisisDir/downloadData.py

printf "   > Update data SSTs \n"
/bin/rm $analisisDir/data/sst*.nc
$pythonDir $analisisDir/analysisData.py

printf "   > Update data SSTs demarcaciones\n"
$pythonDir $analisisDir/analysisDataiDemarcaciones.py

printf "   > Plots SSTs \n"
/bin/rm $analisisDir/images/*.png
$pythonDir $analisisDir/plotsTimeSeries.py

printf "   > Plots Mapa anomalia \n"
$pythonDir $analisisDir/plotsMapAnomalies.py 
$pythonDir $analisisDir/plotsMapAnomaliesDemarcaciones.py 

printf "   > Plots comparacionHS \n"
$pythonDir $analisisDir/plotsComparaHemispheres.py 

printf "   > Upload Plots \n"
$pythonDir $analisisDir/uploadImages.py
