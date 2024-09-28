% Returns the orbit velocity of a satellite given its altitude

function [vel] = orbitVelocity(alt)
G = 6.6743e-11;                 % Gravitational constant
m_Earth = 5.972e24;             % Mass of Earth (kg)

vel = sqrt(G*m_Earth/alt);      % Orbit velocity (m)
end
