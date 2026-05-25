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

%showStrings = ones(7);
%showStrings = zeros(7);
showStrings = [0 0 0 0 0 0 1 0];

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
        plot3(N1(i+1, k+1, 1), N1(i+1, k+1, 2), N1(i+1, k+1, 3), 'ko', 'MarkerFaceColor', 'k', 'MarkerSize', 4);
        if i < q
            plot3(N2(i+1, k+1, 1), N2(i+1, k+1, 2), N2(i+1, k+1, 3), 'ro', 'MarkerFaceColor', 'r', 'MarkerSize', 4);
        end
    end
end

% Plot bars and strings
for i = 0:q-1
    for k = 0:p-1
        
        % Base indices handling circular wrap-around
        k_curr = k + 1;
        kp1 = mod(k + 1, p) + 1;
        km1 = mod(k - 1, p) + 1;
        
        % --- Grab all exact neighbor nodes required by Skelton's matrices ---
        n1_ik      = squeeze(N1(i+1, k_curr, :));  % n1(i, k)
        n2_ik      = squeeze(N2(i+1, k_curr, :));  % n2(i, k)
        
        n1_ip1_kp1 = squeeze(N1(i+2, kp1, :));     % n1(i+1, k+1)
        n2_ip1_km1 = squeeze(N2(i+2, km1, :));     % n2(i+1, k-1)
        
        n1_ip1_k   = squeeze(N1(i+2, k_curr, :));  % n1(i+1, k)
        n2_i_km1   = squeeze(N2(i+1, km1, :));     % n2(i, k-1)
        n1_ip1_km1 = squeeze(N1(i+2, km1, :));     % n1(i+1, k-1)
        
        % --- BARS ---
        % b1: Right-Hand Helix (Connects n1(i,k) to n1(i+1, k+1))
        plot3([n1_ik(1), n1_ip1_kp1(1)], [n1_ik(2), n1_ip1_kp1(2)], [n1_ik(3), n1_ip1_kp1(3)], 'b-', 'LineWidth', 2);
          
        if i < q - 1
            % b2: Left-Hand Helix (Connects n2(i,k) to n2(i+1, k-1))
            plot3([n2_ik(1), n2_ip1_km1(1)], [n2_ik(2), n2_ip1_km1(2)], [n2_ik(3), n2_ip1_km1(3)], 'b-', 'LineWidth', 2);
            
            % --- STRINGS ---
            if showStrings(1) == 1 % s1
                plot3([n1_ik(1), n2_ik(1)], [n1_ik(2), n2_ik(2)], [n1_ik(3), n2_ik(3)], 'r--', 'LineWidth', 1);
            end
            if showStrings(2) == 1 % s2
                plot3([n2_ik(1), n1_ip1_k(1)], [n2_ik(2), n1_ip1_k(2)], [n2_ik(3), n1_ip1_k(3)], 'g--', 'LineWidth', 1);
            end
            if showStrings(3) == 1 % s3
                plot3([n1_ip1_k(1), n2_i_km1(1)], [n1_ip1_k(2), n2_i_km1(2)], [n1_ip1_k(3), n2_i_km1(3)], 'm--', 'LineWidth', 1);
            end
            if showStrings(4) == 1 % s4
                plot3([n2_i_km1(1), n1_ik(1)], [n2_i_km1(2), n1_ik(2)], [n2_i_km1(3), n1_ik(3)], 'k--', 'LineWidth', 1);
            end
            if showStrings(5) == 1 % s5
                plot3([n2_i_km1(1), n2_ik(1)], [n2_i_km1(2), n2_ik(2)], [n2_i_km1(3), n2_ik(3)], 'k--', 'LineWidth', 1);
            end
            if showStrings(6) == 1 % s6
                plot3([n1_ik(1), n1_ip1_k(1)], [n1_ik(2), n1_ip1_k(2)], [n1_ik(3), n1_ip1_k(3)], 'r-', 'LineWidth', 1);
            end
            if showStrings(7) == 1 % s7
                plot3([n1_ip1_km1(1), n1_ip1_k(1)], [n1_ip1_km1(2), n1_ip1_k(2)], [n1_ip1_km1(3), n1_ip1_k(3)], 'g-', 'LineWidth', 1);
            end
            if showStrings(8) == 1 % s8
                plot3([n2_i_km1(1), n2_ip1_km1(1)], [n2_i_km1(2), n2_ip1_km1(2)], [n2_i_km1(3), n2_ip1_km1(3)], 'c--', 'LineWidth', 1);
            end
        else
            % Top boundary closure condition (i = q-1)
            % Skelton replaces b2 with an anchor bar to n1(q, k)
            n1_top = squeeze(N1(i+2, k_curr, :)); 
            plot3([n2_ik(1), n1_top(1)], [n2_ik(2), n1_top(2)], [n2_ik(3), n1_top(3)], 'c-', 'LineWidth', 2); 
        end
    end
end
legend('n_1 Nodes', 'n_2 Nodes');
hold off;
% %% 5. Export Coordinates for SolidWorks
% 
% % --- Export N1 Nodes ---
% % Reshape N1 from [q+1, p, 3] into an (TotalPoints x 3) matrix
% N1_flat = reshape(N1, [], 3); 
% 
% % Remove any NaN rows just in case, though N1 shouldn't have them
% N1_flat(any(isnan(N1_flat), 2), :) = []; 
% 
% N1_flat = N1_flat .* 100;
% 
% % Save as space-delimited TXT (SolidWorks prefers space/tab over commas for XYZ curves)
% writematrix(N1_flat, 'N1_coordinates.txt', 'Delimiter', 'space');
% 
% 
% % --- Export N2 Nodes ---
% % Reshape N2 from [q+1, p, 3] into an (TotalPoints x 3) matrix
% N2_flat = reshape(N2, [], 3);
% 
% N2_flat(any(isnan(N2_flat), 2), :) = []; 
% 
% N2_flat = N2_flat .* 100;
% 
% % Save N2 coordinates
% writematrix(N2_flat, 'N2_coordinates.txt', 'Delimiter', 'space');
% 
% disp('SolidWorks coordinate files generated successfully: N1_coordinates.txt and N2_coordinates.txt');