% Finds the distance of a position vector from the origin

function [dist] = distFromOrigin(positionVector)
dist = sqrt(dot(positionVector,positionVector)); % (m)
end
