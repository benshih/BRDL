%% LCR Meter Reader 
clear; close all; clc

% Find a VISA-USB object.
obj1 = instrfind('Type', 'visa-usb', 'RsrcName', 'USB0::0x0957::0x0909::MY54202935::0::INSTR', 'Tag', '');
 
% Create the VISA-USB object if it does not exist
% otherwise use the object that was found.
if isempty(obj1)
    obj1 = visa('AGILENT', 'USB0::0x0957::0x0909::MY54202935::0::INSTR');
else
    fclose(obj1);
    obj1 = obj1(1);
end
 
% Connect to instrument object, obj1.  
fopen(obj1);
 
% Communicating with instrument object, obj1. 
type = query(obj1, ':FUNCtion:IMPedance:TYPE?');
disp('LCR Connected.');
%% Main Data Collection

% Figures Setup
timeStepEnd = 400; % 400 ~= 1 min
out = zeros(timeStepEnd,4);
                 
figure(1)
 
% LCR 1 Plot
subplot(2,1,1)
h1 = animatedline('Color','b','lineWidth',1.5);
ax1 = gca;
ax1.YGrid = 'on';
ylabel('Resistance');

% LCR 2 Plot
subplot(2,1,2)
h2 = animatedline('Color','g','lineWidth',1.5); 
ax2 = gca;
ax2.YGrid = 'on';

%Pause to signal start recording
pause;
disp('Ready. Start recording now')
 
% Start time
startTime = datetime('now');
 
for i = 1:timeStepEnd
    
    % Get current time 
    t(i,1) = datetime('now') - startTime;
   
    data = query(obj1, ':FETCh:IMPedance:FORMatted?');
    splt = strsplit(data,',');
    
    out(i,1) = str2double(splt(1)); % LCR 1 
    out(i,2) = str2double(splt(2)); % LCR 2
    
    figure(1) 
    
    % LCR1 Graph
    subplot(2,1,1)
    addpoints(h1,datenum(t(i,1)),out(i,1));
    ax1.XLim = datenum([t(i,1) - seconds(15) t(i,1)]);
    datetick('x','keeplimits');
    drawnow update
    
    % LCR2 Graph 
    subplot(2,1,2)
    addpoints(h2,datenum(t(i,1)),out(i,2));
    ax2.XLim = datenum([t(i,1) - seconds(15) t(i,1)]);
    datetick('x','keeplimits');
    drawnow update
 
end
 
% Disconnect from instrument object, obj1.
fclose(obj1);
 
%% Make table and save data
variablePrompt = ...
    'Enter the names of the variables measured separated by commas:';
varNames = input(variablePrompt,'s');
varTable = strsplit(varNames,',');
T = table(seconds(t),out(:,1),out(:,2),'VariableNames',varTable);
tablePrompt = 'Enter the name of excel file:';
fileName = input(tablePrompt,'s');
fileName = strcat(fileName, '.xls');
writetable(T,fileName);
fprintf('Results table saved to file %s\n',fileName);

%% Plot Data
figure(2);
yyaxis left; plot(t(:,1),out(:,1),'lineWidth',1.5); hold on;
xlabel('Time (s)'); ylabel(varTable{2}); 
yyaxis right; plot(t(:,1),out(:,2),'lineWidth',1.5)
xlabel('Time (s)');ylabel(varTable{3});
hold off;

%% Add a low pass filter. Watch out for phase gain.
Fs = 1000;
order = 20;
cutoffFreq = 100;
LP = designfilt('lowpassfir','FilterOrder',order,'CutoffFrequency',cutoffFreq, ...
       'DesignMethod','window','Window',{@kaiser,3},'SampleRate',Fs);
y_filtered = filter(LP, out(:,1));
plot(t(:,1),out(:,1),t(:,1),y_filtered(:,1), 'lineWidth', 1.25);


 