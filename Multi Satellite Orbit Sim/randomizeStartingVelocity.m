% Randomizes the starting velocity of the satellite. The direction of the
% velocity is orthogonal to it's position vector and therefore tangential
% to the gravitational force. It's magnitude is equal to the necessary
% oribital velocity

function [Vx,Vy,Vz] = randomizeStartingVelocity(Rx,Ry,Rz)

v_orbit = orbitVelocity(distFromOrigin([Rx Ry Rz]));        % Necessary orbital speed (m/s)

V_components = cross([Rx Ry Rz],[rand() rand() rand()]);                   % Velocity vector orthogonal to gravity vector

V_ud = V_components/sqrt(dot(V_components,V_components));       % Unit direction of velocity

Vx = V_ud(1)*v_orbit;
Vy = V_ud(2)*v_orbit;
Vz = V_ud(3)*v_orbit;


end


