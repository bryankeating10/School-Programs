% Randomizes the starting position of a satellite. The constraints are a
% minimum altitude of 4e^7 meters and a maximum of 7.1e^7 meters

function [Rx,Ry,Rz] = randomizeStartingPosition()
Rx = randi(8e7)-4e7;        % Random x position between +/-4e7 meters
Ry = randi(8e7)-4e7;        % Random y position between +/-4e7 meters

min_alt = 4e7;              % Minimum satellite altitude (m)
max_alt = 7.1e7;            % Minimum satellite altitude (m)

Rzmax = sqrt(max_alt^2-Rx^2-Ry^2); % Minimum z componenet (m)
min_req = min_alt^2-Rx^2-Ry^2;

if (min_req >= 0)
    Rzmin = sqrt(min_req);
else
    Rzmin = -4e7;
end

% First () returns either 1 or -1, second () returns the absolute z value
Rz = (randi([0 1])*2-1)*(randi(floor(Rzmax-Rzmin))+Rzmin);

end
