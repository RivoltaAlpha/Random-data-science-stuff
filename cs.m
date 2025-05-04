% Load the dataset
data = readtable('data1.xlsx', 'Sheet', 'Sheet2');

% Use the corrected column names
regions = data{:, 'Var1'}; % 'Var1' replaces 'Unnamed_0'
latitude = data{:, 'lattitude'};
longitude = data{:, 'longitude'};
water_content = data{:, 'theta'};
critical_value = data{:, 'prefre'};
precipitation = data{:, 'Preci'};
evaporation = data{:, 'Evapor'};

% Ensure regions are treated as strings
if isnumeric(regions)
    regions = string(regions);
elseif iscell(regions)
    regions = string(regions);
end

% Plot soil water content vs. critical value for analysis
figure;
scatter(water_content, critical_value, 'filled');
xlabel('Soil Water Content (\theta)');
ylabel('Critical Value (prefre)');
title('Critical Value vs. Soil Water Content');
grid on;

