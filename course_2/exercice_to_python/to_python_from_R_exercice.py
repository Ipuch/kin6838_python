"""
Convert this script from Matlab to Python
"""

# import ...
# import ...

fs = [1, 2, 4];
all_time = linspace(start=0, stop=2, num=200);
t = all_time(1:100);

for f = fs
    y = sin(2 * pi * f * t);
    plot(t, y, 'DisplayName', sprintf('%d Hz', f));
end

legend("show");
saveas(gcf, 'basics_matlab.png');