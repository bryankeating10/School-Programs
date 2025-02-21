clc
clear
close all

syms y(t)
Dy = diff(y, t);        % Y dot
D2y = diff(y, t, 2);    % Y double dot

% Define the equation
eqn = D2y + 3*Dy + 2*y == 0;

% Solve the equation with initial conditions y(0) = 1, y'(0) = 0
conds = [y(0) == 1, Dy(0) == 2];
sol = dsolve(eqn, conds);

% Convert symbolic solution to function
figure("Name","ChatGPT Example","Position",[100 100 500 500])
fplot(matlabFunction(sol), [0, 10])
xlabel('Time t')
ylabel('y(t)')
title('Solution of the Second-Order ODE')
grid on
hold off


% Trying to visualize a pendulum with a point mass and damper attached to
% its end
syms theta(t)
Dtheta = diff(theta,t);
D2theta = diff(theta,t,2);

g = 9.81;       % Gravity (m/s^2)
l = 2;          % Pendulum length (m)
d = 1;          % Damping coefficient (N*s/m)
m = 2;          % Mass (kg)

eqn_pendulum = D2theta + (3*d/(4*m*l))*Dtheta + (9*g/(2*l))*theta;

% Initial position at 0.01 rad and 0.1 rad/sec
init_conds = [theta(0) == 0.01, Dtheta(0) == 0.1];
sol_pend = dsolve(eqn_pendulum,init_conds);

figure("Name","First pendulum example","Position",[100 100 500 500])
fplot(matlabFunction(sol_pend), [0, 10])
xlabel('Time t')
ylabel('theta(t)')
title('Pendulum motion')
grid on
hold off

% Visualizing the motion of a quarter car system on a bumpy road
% Wheel motion
syms y1(t)          
Dy1 = diff(y1,t);
D2y1 = diff(y1,t,2);

% Quarter car motion
syms y2(t)
Dy2 = diff(y2,t);
D2y2 = diff(y2,t);

% Constants
m_1 = 375;          % Quarter car mass (kg)
m_2 = 20;           % Wheel mass (kg)
ks = 130e3;         % Suspension spring coeff (N/m)
kw = 1e6;           % Car spring coeff (N/m)
b = 9.8e3;          % Damping force (N*s/m)

eqn1 = Dy1;

% Checking accuracy of manual diff eq solution
syms g(t)
Dg = diff(g,t);
D2g = diff(g,t,2);

eqn_acc = D2g + Dg + 3*g == 0;

% Solve the equation with initial conditions g(0) = 0, g'(0) = 2
conds_acc = [g(0) == 0, Dg(0) == 2];
sol_acc = dsolve(eqn_acc, conds_acc);

% Convert symbolic solution to function
figure("Name","Homework Accuracy","Position",[100 100 500 500])
fplot(matlabFunction(sol_acc), [0 10])
xlabel('Time t')
ylabel('g(t)')
title('Homework Accuracy Check')
grid on
hold on

% My solution
y_my = @(t_my) (1/3)*sin(t_my)-(sqrt(3)/6)*sin(sqrt(3)*t_my)-cos(sqrt(3)*t_my);
y_other = @(t_other) (4/sqrt(11))*exp(-(1/2)*t_other)*sin((sqrt(11)/2)*t_other) + 0.1;
fplot(y_my,[0 10])
fplot(y_other,[0 10])

hold off
