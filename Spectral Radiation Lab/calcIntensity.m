% Calculate intensity using temperature, wavelength, and Planck's Law of
% monochromatic blackbody radiation

function [intensity] = calcIntensity(temp,lambda)

% CONSTANTS
h = 6.6261e-34;                 % Plank's constant (J/s)
k = 1.3806e-23;                 % Boltzmann's constant (J/K)
c = 2.9979e8;                   % Speed of light (m/s)
lambda = lambda*1e-9;           % Converts nanometers to meters

% CALCULATIONS
num = 2*h*c^2;
den1 = lambda.^5;
den2a = (h*c/(k*temp))./lambda;
den2b = exp(den2a)-1;
intensity = num./(den1.*den2b);

end