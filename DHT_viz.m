clear; clc; close all;

%% 1. Define Structural Parameters
p = 6;          % Number of units around the circumference
q = 6;          % Number of units along the vertical axis
L = 1.0;        % Total length of the structure
a = 1/16;       % Focus of the paraboloid
Ld = 1.001;       % Height of the paraboloid (must be > L)

%% 2. Initialize Node Storage
N1 = zeros(q+1, p, 3); 
N2 = zeros(q+1, p, 3);

%% 3. Calculate Node Coordinates
for i = 0:q
    for k = 0:p-1
        
        % Calculate for l = 1 (Applies to all rows 0 to q)
        l = 1;
        z1 = (2*i + (l-1)) * (L / (2*q));
        theta1 = (2*k + l) * (pi / p);
        r1_val = sqrt(4 * a * (Ld - z1));
        
        N1(i+1, k+1, 1) = r1_val * cos(theta1); 
        N1(i+1, k+1, 2) = r1_val * sin(theta1); 
        N1(i+1, k+1, 3) = z1;                   
        
        % Calculate for l = 2 (Skip for the very top boundary i=q)
        if i < q
            l = 2;
            z2 = (2*i + (l-1)) * (L / (2*q));
            theta2 = (2*k + l) * (pi / p);
            r2_val = sqrt(4 * a * (Ld - z2));
            
            N2(i+1, k+1, 1) = r2_val * cos(theta2); 
            N2(i+1, k+1, 2) = r2_val * sin(theta2); 
            N2(i+1, k+1, 3) = z2;                   
        else
            N2(i+1, k+1, :) = NaN; % n2(q,k) does not exist
        end
        
    end
end

%% 4. Plotting the Structure
figure('Name', 'Double-Helix Paraboloid Tensegrity', 'Color', 'w');
hold on; grid on; axis equal;
view(3);
xlabel('X [m]'); ylabel('Y [m]'); zlabel('Z [m]');
title(sprintf('Paraboloid of Revolution (p=%d, q=%d) with Boundary Closure', p, q));

% Plot nodes
for i = 0:q
    for k = 0:p-1
        % Always plot n1
        plot3(N1(i+1, k+1, 1), N1(i+1, k+1, 2), N1(i+1, k+1, 3), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 4);
        
        if i < q
            plot3(N2(i+1, k+1, 1), N2(i+1, k+1, 2), N2(i+1, k+1, 3), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
        end
    end
end

% Plot bars and strings
for i = 0:q-1
    for k = 0:p-1
        
        n1_current = squeeze(N1(i+1, k+1, :));
        n2_current = squeeze(N2(i+1, k+1, :));
        
        k_plus_1 = mod(k + 1, p);
        k_minus_1 = mod(k - 1, p);
        
        n1_next_kplus = squeeze(N1(i+2, k_plus_1+1, :));
        n1_current_kminus = squeeze(N1(i+1, k_minus_1+1, :));
        n2_next_kplus = squeeze(N2(i+2, k_plus_1+1, :));
        n2_current_kminus = squeeze(N2(i+1, k_minus_1+1, :));
        
        % Draw Bar 1 (Standard for all rows)
        plot3([n1_current(1), n1_next_kplus(1)], ...
              [n1_current(2), n1_next_kplus(2)], ...
              [n1_current(3), n1_next_kplus(3)], 'b-', 'LineWidth', 2);
          
        % Draw Bar 2
        if i < q - 1
            % Internal rows: standard double-helix connection
            n2_next_kminus = squeeze(N2(i+2, k_minus_1+1, :));
            n1_next_kminus = squeeze(N1(i+2, k_minus_1+1, :));

            plot3([n2_current(1), n2_next_kminus(1)], ...
                  [n2_current(2), n2_next_kminus(2)], ...
                  [n2_current(3), n2_next_kminus(3)], 'b-', 'LineWidth', 2)
           
            plot3([n1_current(1), n2_current(1)], ...
                  [n1_current(2), n2_current(2)], ...
                  [n1_current(3), n2_current(3)], 'r--', 'LineWidth', 1) %this is s1

            % plot3([n2_current(1), n2_current_kminus(1)], ...
            %       [n2_current(2), n2_current_kminus(2)], ...
            %       [n2_current(3), n2_current_kminus(3)], 'r--', 'LineWidth', 1) %this is s2
            % 
            % plot3([n1_current_kminus(1), n2_current_kminus(1)], ...
            %       [n1_current_kminus(2), n2_current_kminus(2)], ...
            %       [n1_current_kminus(3), n2_current_kminus(3)], 'r--', 'LineWidth', 1) %this is s3
            % 
            % plot3([n1_current(1), n2_current_kminus(1)], ...
            %       [n1_current(2), n2_current_kminus(2)], ...
            %       [n1_current(3), n2_current_kminus(3)], 'r--', 'LineWidth', 1) %this is s4
            % 
            % plot3([n2_current(1), n2_current_kminus(1)], ...
            %       [n2_current(2), n2_current_kminus(2)], ...
            %       [n2_current(3), n2_current_kminus(3)], 'r--', 'LineWidth', 1) %this is s5
            % 
            % % plot3([n2_current(1), n2_current(1)], ...
            % %       [n2_current(2), n2_current(2)], ...
            % %       [n2_current(3), n2_current(3)], 'r--', 'LineWidth', 1)
            % %       %this is s6
            % 
            % plot3([n1_current(1), n1_next_kminus(1)], ...
            %       [n1_current(2), n1_next_kminus(2)], ...
            %       [n1_current(3), n1_next_kminus(3)], 'r--', 'LineWidth', 1) %this is s7
            % 
            % plot3([n1_current(1), n2_next_kminus(1)], ...
            %       [n1_current(2), n2_next_kminus(2)], ...
            %       [n1_current(3), n2_next_kminus(3)], 'r--', 'LineWidth', 1) %this is s8

        else
            % Top row (i = q-1): standard b2 is removed. 
            % Replaced by \bar{b}_2 connecting to n1(q, k)
            n1_top = squeeze(N1(i+2, k+1, :)); 
            plot3([n2_current(1), n1_top(1)], ...
                  [n2_current(2), n1_top(2)], ...
                  [n2_current(3), n1_top(3)], 'c-', 'LineWidth', 2); % Cyan to highlight boundary bar
        end

    

    end
end

legend('n_1 Nodes', 'n_2 Nodes');
hold off;