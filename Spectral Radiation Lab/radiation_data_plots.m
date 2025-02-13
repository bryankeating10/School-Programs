clc
clear
close all

% Load the wavelength matrix and voltage matricies for each of the
% sources
load("radiationVariables.mat")

% Initialize screen sections for visualization purposes
screenSize = get(0,'ScreenSize');
sWid = screenSize(3);
sHie = screenSize(4);
a = sWid/2;
b = sHie/2;
topRight = [a b+10 a b-90];
bottomRight = [a 50 a b-120];
topLeft = [0 b+10 a b-90];
bottomLeft = [0 50 a b-120];
defaultSquare = [a-500 b-350 a+100 b+200];

% Plot intensity vs wavelength for 1600F and 1300F source
figure("Name","Intensity",'Position',defaultSquare)
hold on
plot(wavelength, calcIntensity(1144.261, wavelength), '-', 'Color', [1.000, 0.647, 0.000], ...
    'Marker', '.',LineWidth=2,MarkerSize=24);
plot(wavelength, calcIntensity(977.594, wavelength), '-', 'Color', [0.871, 0.192, 0.388], ...
    'Marker', '.',LineWidth=2,MarkerSize=24);

hold off
xlim([1090 1710])
legend('1600F Source', '1300F Source', 'Location', 'north',Fontsize=16);
title("Intensity of Blackbody Source",FontSize=18)
xlabel("Wavelength (nm)",FontSize=16)
ylabel("Intensity (W/m^3*st)",FontSize=16)
grid on


% Plot calibration factor vs wavelength for 1600F and 1300F source
calib_1300 = calcCalibration(voltage_1300,977.594, wavelength);
calib_1600 = calcCalibration(voltage_1600,1144.261, wavelength);
calib_avg = (calib_1600 + calib_1300)/2;

figure("Name","Calibration Factor",'Position',defaultSquare)
hold on
plot(wavelength, calib_avg, '-', 'Color', [0, 1.000, 0], ...
    'Marker', '.',LineWidth=2,MarkerSize=24);
plot(wavelength, calib_1600, '-', 'Color', [1.000, 0.647, 0], ...
    'Marker', '.',LineWidth=2,MarkerSize=24);
plot(wavelength, calib_1300, '-', 'Color', [0.871, 0.192, 0.388], ...
    'Marker', '.',LineWidth=2,MarkerSize=24);

hold off
xlim([1090 1710])
ylim([0.985 1.61])
legend('Average','1600F Source', '1300F Source', 'Location', 'north',Fontsize=16);
title("Spectral Calibration Factor",FontSize=18)
xlabel("Wavelength (nm)",FontSize=16)
ylabel("Calibration Factor (unitless)",FontSize=16)
grid on
