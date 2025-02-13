% Caclculates the calibration factor using spectral radiation intensity,
% net voltage, and source temperature

function [eta] = calcCalibration(V,T,lambda)

% Reference values at 1550 nanometers
I_naut = calcIntensity(T,1550);
V_naut = V(10);

% Calculate spectral calibration factor
eta = (calcIntensity(T,lambda)/I_naut).*(V_naut./V);

end