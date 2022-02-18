cd
folder=cd('C:\Users\alexi\OneDrive\Documentos\Nueva carpeta ISC\TXT');
if strcmp(folder,cd)==1
else
    folder=cd('C:\Users\alexi\OneDrive\Documentos\Nueva carpeta ISC\TXT');
end
archivos=ls(folder);
for i=1:1:length(archivos)
    texto=(archivos(i+2,:));
    datos=zeros(1000,27);
    datos=load(texto);
    x(i).x=datos(1:1000,1);
    y(i).y=datos(1:1000,2);
    figure,
    plot(x(i).x,y(i).y,'LineWidth',0.1), title('Datos archivo txt');
    grid on;
end