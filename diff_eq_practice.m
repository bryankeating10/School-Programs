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
figure("Name","ChatGPT Example")
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

figure("Name","First pendulum example")
fplot(matlabFunction(sol_pend), [0, 10])
xlabel('Time t')
ylabel('theta(t)')
title('Pendulum motion')
grid on

