
% Gravitational function

function [F_gravity] = gravityForThreeD(altitude,m1,m2)
G = 6.6743e-11;                     % Gravitational constant
F_gravity = G*m1*m2/altitude^2;     % Force due to gravity

