% Load the dataset
data = readtable('data.xlsx', 'Sheet', 'Sheet2');
disp(data.Properties.VariableNames);


% Extract relevant columns
regions = data{:, 'region'};
soil_moisture = data{:, 'theta'};
critical_value = data{:, 'prefre'};
latitude = data{:, 'lattitude'};
longitude = data{:, 'longitude'};

% Define regions
region_names = {'desert', 'grasslands', 'forest', 'wetlands'}; % Modify if needed
region_colors = {'red', 'green', 'blue', 'cyan'}; % Colors for plotting

% Assign region indices based on type
region_indices = cell(length(region_names), 1);
for i = 1:length(region_names)
    region_indices{i} = strcmp(regions, region_names{i}); % Match the type column to region names
end

% Plot soil moisture vs. critical value for each region
figure;
hold on;
for i = 1:length(region_names)
    idx = region_indices{i};
    scatter(soil_moisture(idx), critical_value(idx), 50, region_colors{i}, 'filled');
end
xlabel('Soil Moisture (\theta)');
ylabel('Critical Value (prefre)');
legend(region_names, 'Location', 'Best');
title('Soil Moisture vs. Critical Value by Region');
grid on;

% Critical value for saturation: Find maximum soil moisture for each region
disp('Critical Values for Soil Moisture Saturation by Region:');
for i = 1:length(region_names)
    idx = region_indices{i};
    critical_moisture = max(soil_moisture(idx));
    fprintf('%s: %.4f\n', region_names{i}, critical_moisture);
end

% Vegetation succession analysis
% Steady-state analysis: Use a simple logistic model for illustration
theta_max = max(soil_moisture); % Saturation point
theta_critical = mean(soil_moisture); % Approximation of critical value
theta = linspace(0, theta_max, 100); % Range of soil moisture
succession_rate = (theta ./ theta_max) .* (1 - (theta ./ theta_max)); % Logistic growth

% Plot steady-state solution
figure;
plot(theta, succession_rate, 'LineWidth', 2);
xlabel('Soil Moisture (\theta)');
ylabel('Vegetation Succession Rate');
title('Steady-State Vegetation Succession Analysis');
grid on;

% Regional geographical distribution of critical values
figure;

% Define regions
region_names = {'desert', 'grasslands', 'forest', 'wetlands'}; % Modify if needed
region_colors = {'red', 'green', 'blue', 'cyan'}; % Colors for plotting

% Loop through each region to plot geographical distribution
for i = 1:length(region_names)
    idx = region_indices{i}; % Indices for the current region
    scatter(latitude(idx), longitude(idx), 50, region_colors{i}, 'filled'); % Use region-specific color
    hold on;
end

% Add labels, legend, and title
xlabel('Latitude');
ylabel('Longitude');
legend(region_names, 'Location', 'Best');
title('Geographical Distribution of Critical Values by Region');
grid on;

% Calculate the mean critical values for each region
mean_critical_values = zeros(length(region_names), 1);
for i = 1:length(region_names)
    idx = region_indices{i};
    mean_critical_values(i) = mean(critical_value(idx)); % Calculate mean critical value
end


