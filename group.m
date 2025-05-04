% All units of space are in cm, and time is in seconds
% Initial conditions
z_0 = 0;
theta_0 = 0.4756; % Initial theta value
H_0 = 0;

% Parameters for Case 12
n_value = 1.2654;
C_value = 0.000005;
theta_s_value = 0.4756;
theta_r_value = 0.1662;
K_s_value = 0.000267;
alpha_value = 0.0619;

% Grid size (step size)
delta_z = 0.01;  % For example, each grid cell is 0.01 cm

% Maximum z value
max_z = 1000;  

% Maximum number of iterations
max_iterations = ceil(max_z / delta_z);

% Convergence tolerance
tolerance = 1e-10;

% Initialization
z_values = z_0;
theta_values = theta_0;
H_values = H_0;
H_minus_z_values = []; % Initialize array for H - z
K_values = []; % Initialize array for K values

% Iterative computation
for i = 1:max_iterations
    z_i = z_values(end);
    theta_i = theta_values(end);
    H_i = H_values(end);

    % Compute K(θ_i)
    lambda_val = (theta_i - theta_r_value) / (theta_s_value - theta_r_value);
    K_i = K_s_value * sqrt(lambda_val) * (1 - (1 - lambda_val^(1/(1 - 1/n_value)))^(1 - 1/n_value))^2;

    % Add current K_i to the array
    K_values = [K_values, K_i];
    % If K is below a small threshold, set it to a very small positive value
    if K_i < 1e-10
        K_i = 1e-10;
    end

    % Compute [H(z_{i+1}) - H(z_i)] / Δz
    delta_H_over_delta_z = C_value / K_i; % Negative sign indicates evaporation > precipitation

    % Compute new H(z_{i+1})
    H_i_plus_1 = H_i + delta_H_over_delta_z * delta_z;

    % Update z, θ, and H values
    z_i_plus_1 = z_i + delta_z;
    z_values = [z_values, z_i_plus_1];

    % Compute H - z
    H_minus_z_i_plus_1 = H_i_plus_1 - z_i_plus_1;
    H_minus_z_values = [H_minus_z_values, H_minus_z_i_plus_1];

    % If H - z > 0, set K and θ to saturation values
    if (H_i_plus_1 - z_i_plus_1) > 0
        theta_i_plus_1 = theta_s_value;
        K_i_plus_1 = K_s_value;
    else
        % Compute the corresponding θ value
        theta_i_plus_1 = theta_r_value + ...
            (1 + (alpha_value * abs(H_i_plus_1 - z_i_plus_1))^n_value)^((1/n_value) - 1) * ...
            (theta_s_value - theta_r_value);
        theta_values = [theta_values, theta_i_plus_1];

        % Recalculate K(θ_{i+1})
        lambda_val_plus_1 = (theta_i_plus_1 - theta_r_value) / (theta_s_value - theta_r_value);
        K_i_plus_1 = K_s_value * sqrt(lambda_val_plus_1) * ...
            (1 - (1 - lambda_val_plus_1^(1/(1 - 1/n_value)))^(1 - 1/n_value))^2;
    end

    % Update K_i
    K_i = K_i_plus_1;

    H_values = [H_values, H_i_plus_1];

    % Check for convergence
    if abs(delta_H_over_delta_z) < tolerance
        break;
    end
end

% Create a K_value array of the same size as z_values
K_value = repmat(K_s_value, size(z_values));

% Plot results

% Calculate and plot ψ = H - z
H_minus_z_values = H_values - z_values;

% Log transformation of H - z
log_H_minus_z_values = log(-H_minus_z_values);

% Compute S = θ / θ_s
S_values = theta_values / theta_s_value;


%% Normalization of parameters for consistent scaling
H_normalized = H_values / max(abs(H_values));          % Normalize H values
theta_normalized = theta_values / max(abs(theta_values)); % Normalize θ values
H_minus_z_normalized = H_minus_z_values / max(abs(H_minus_z_values)); % Normalize ψ
log_H_minus_z_normalized = log(-H_minus_z_values) / max(abs(log(-H_minus_z_values))); % Normalize log(ψ)
S_normalized = S_values / max(abs(S_values));         % Normalize S values

% Plot all parameters against z
figure;
hold on; % Enable multiple plots on the same figure
plot(z_values, H_normalized, 'LineWidth', 2, 'DisplayName', 'H (Normalized)');
plot(z_values, theta_normalized, 'LineWidth', 2, 'DisplayName', '\theta (Normalized)');
plot(z_values, H_minus_z_normalized, 'LineWidth', 2, 'DisplayName', '\psi (H - z, Normalized)');
plot(z_values, log_H_minus_z_normalized, 'LineWidth', 2, 'DisplayName', 'log(\psi) (Normalized)');
plot(z_values, S_normalized, 'LineWidth', 2, 'DisplayName', 'S (Normalized)');

% Add labels, legend, and title
xlabel('z');
ylabel('Normalized Values');
title('Group Analysis of H, θ, ψ, log(ψ), and S vs z');
legend('Location', 'best');
grid on;
hold off;

