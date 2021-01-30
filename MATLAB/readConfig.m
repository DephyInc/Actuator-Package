function ports = readConfig()
% Read the configuration file - one COM port per line

ports = {'', '', '' };
fileID = fopen('com.txt');

tline = fgetl(fileID);
index = 1;
i = 1;
while ischar(tline)
	cell_array = strsplit(tline);
	ports{index} = cell_array{i};
	index = index + 1;
	tline = fgetl(fileID);
end

fclose(fileID);
end
