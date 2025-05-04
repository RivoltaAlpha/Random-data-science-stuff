% Load the dataset
data = readtable('data.xlsx', 'Sheet', 'Sheet2');

% Extract relevant columns
regions = data{:, 'region'};
soil_moisture = data{:, 'theta'};
critical_value = data{:, 'prefre'};

% Define regions
region_names = {'desert', 'grasslands', 'forest', 'wetlands'}; % Modify if needed
region_colors = {'red', 'green', 'blue', 'cyan'}; % Colors for plotting

% Initialize storage for results
critical_values = zeros(length(region_names), 1); % Maximum soil moisture per region
near_saturation_counts = zeros(length(region_names), 1); % Count of near-saturation values

% Define saturation threshold (e.g., within 90% of max soil moisture)
saturation_threshold = 0.9;

% Calculate critical values and near-saturation counts for each region
disp('Critical Values and Near-Saturation Counts by Region:');
for i = 1:length(region_names)
    % Get indices for the current region
    idx = strcmp(regions, region_names{i});
    
    % Extract soil moisture values for the region
    region_soil_moisture = soil_moisture(idx);
    
    % Find the maximum (critical) value for soil moisture in the region
    critical_values(i) = max(region_soil_moisture);
    
    % Count values approaching saturation (within 90% of max value)
    near_saturation_counts(i) = sum(region_soil_moisture >= saturation_threshold * critical_values(i));
    
    % Display results
    fprintf('%s:\n', region_names{i});
    fprintf('  Critical Value (Max Soil Moisture): %.4f\n', critical_values(i));
    fprintf('  Near-Saturation Count: %d\n\n', near_saturation_counts(i));
end
% Define region colors using RGB triplets
region_colors_rgb = [ ...
    1, 0, 0;    % Red for 'desert'
    0, 1, 0;    % Green for 'grasslands'
    0, 0, 1;    % Blue for 'forest'
    0, 1, 1     % Cyan for 'wetlands'
];

% Bar chart: Critical values by region
figure;
b = bar(critical_values, 'FaceColor', 'flat'); % Set 'FaceColor' to 'flat' for custom colors
for i = 1:length(region_names)
    b.CData(i, :) = region_colors_rgb(i, :); % Assign region-specific RGB colors
end
set(gca, 'XTickLabel', region_names, 'XTickLabelRotation', 45);
xlabel('Regions');
ylabel('Critical Value (Max Soil Moisture)');
title('Critical Values by Region');
grid on;

% Bar chart: Near-saturation counts by region
figure;
b = bar(near_saturation_counts, 'FaceColor', 'flat'); % Set 'FaceColor' to 'flat' for custom colors
for i = 1:length(region_names)
    b.CData(i, :) = region_colors_rgb(i, :); % Assign region-specific RGB colors
end
set(gca, 'XTickLabel', region_names, 'XTickLabelRotation', 45);
xlabel('Regions');
ylabel('Near-Saturation Count');
title('Near-Saturation Soil Moisture Counts by Region');
grid on;
