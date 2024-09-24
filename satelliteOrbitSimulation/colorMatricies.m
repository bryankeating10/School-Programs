% Color matricies for multi particle displays. Takes a parameter N for how
% many particles will be simulated

function [redMat,greenMat,blueMat] = colorMatricies(N)

redMat = zeros(1,N);
greenMat = zeros(1,N);
blueMat = zeros(1,N);

redStart = linspace(0,1,340341);
greenStart = linspace(0,1,340341);
blueStart = linspace(0,1,340341);
redStart = [redStart zeros(1,170169)];
blueStart = [zeros(1,170169) blueStart];
greenStart = [greenStart(1:170170) zeros(1,170169) greenStart(170171:340341)];

evenSpace = floor(510510/N);

for i=1:N
    redMat(i) = redStart(evenSpace*i);
    greenMat(i) = greenStart(evenSpace*i);
    blueMat(i) = blueStart(evenSpace*i);
end
