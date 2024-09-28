% Plots the orbit of satelllites around the Earth. Takes initial position
% and velocity vectors, timestep, and simulation duration as parameters
clc
clear
close all

% CONSTANTS
m = 1;                                      % Mass of satellites (unimportant to simulation)
m_Earth = 5.972e24;                         % Mass of Earth (kg)

N = 2;                                      % Number of satellites
dt = 120;                                   % Timestep (s)
days = 2.2;                                 % Simulation duration (d)
tmax = days*24*60*60;                       % Simulation duration (s)
imax = floor(tmax/dt);                      % Number of iterations
irecord = floor(600/dt);                    % Records data every 10 mins

[redVal,greenVal,blueVal] = colorMatricies(N);  % RGB values for satelite N
viewAngle = linspace(0,360,imax);           % View angle of the plot for each iteration


% INITIALIZATION
R = zeros(N,3);                             % Empty matrix for initial positions
V = zeros(N,3);                             % Empty matrix for initial velocities
r = zeros(N,1);                             % Empty matrix for altitude values
F = zeros(N,3);                             % Empty matrix for force on satellites


for i=1:N
    [R0x,R0y,R0z] = randomizeStartingPosition();  % Random starting position x,y,z (m)
    R(i,:) = [R0x,R0y,R0z];
    [V0x,V0y,V0z] = randomizeStartingVelocity(R0x,R0y,R0z); % Random starting velocity (m/s)
    V(i,:) = [V0x,V0y,V0z];
    r(i) = distFromOrigin(R(i,:));
    disp(dot(R(i,:),V(i,:)))
end

scatter3(0,0,0,'blue','filled','SizeData',300)
title([mat2str(N),' satellites orbiting the Earth'],"FontSize",15)
subtitle(['Timestep: ',num2str(dt),'s Duration: ',num2str(days),' days'],'FontSize',12)
completion = 0;
annotation('textbox', [0.65, 0.15, 0.1, 0.1],'BackgroundColor','w', 'String','Simulation progress: 0%')
% xlabel('X-axis')
% ylabel('Y-axis')
% zlabel('Z-axis')
xlim([-1.5e8,1.5e8])
ylim([-1.5e8,1.5e8])
zlim([-1.5e8,1.5e8])
grid off
axis off
hold on


% SIMULATION LOOP

for i=1:imax
    F(1,:) = -gravityForThreeD(r(1),m,m_Earth)*R(1,:)/r(1);
    for sat=1:N
        R(sat,:) = R(sat,:) + V(sat,:)*dt + F(sat,:)/(2*m)*dt^2;
        r(sat) = sqrt(dot(R(sat,:),R(sat,:)));
        V(sat,:) = V(sat,:) + F(sat,:)/(2*m)*dt;
        F(sat,:) = -gravityForThreeD(r(sat),m,m_Earth)*R(sat,:)/r(sat);
        V(sat,:) = V(sat,:) + F(sat,:)/(2*m)*dt;
        
        if mod(i,irecord)==1
            completion = viewAngle(i)/3.6;
            annotation('textbox', [0.65, 0.15, 0.1, 0.1],'BackgroundColor','w', 'String',['Simulation progress: ',num2str(floor(completion)),'%']);
            plot3(R(sat,1),R(sat,2),R(sat,3),'.','color',[redVal(sat) greenVal(sat) blueVal(sat)])
            drawnow()
            view([viewAngle(i),0])
            
            %disp(R(sat,:))
        end
    end
end
annotation('textbox', [0.65, 0.15, 0.1, 0.1],'BackgroundColor','g', 'String','Simulation progress: 100%')