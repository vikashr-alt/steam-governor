function run_governor()

root = fileparts(fileparts(mfilename('fullpath')));
res = fullfile(root,'results');
figdir = fullfile(root,'figures');

if ~exist(res,'dir'), mkdir(res); end
if ~exist(figdir,'dir'), mkdir(figdir); end

M = 5;
D = 1;
K = 2;
tau = .5;
kp = 2;
ki = .5;
dt = .01;
t = (0:dt:60)';

A = [-D/M,0,K/M;1,0,0;-kp/tau,-ki/tau,-1/tau];
b = [-1/M;0;0];

poles = eig(A);
disp('Closed-loop poles:');
disp(poles);

assert(all(real(poles)<0));
assert((M+tau*D)*(D+K*kp)>tau*M*K*ki);

fid = fopen(fullfile(res,'matlab_metrics.csv'),'w');
fprintf(fid,'load,peak_speed,peak_time,settling_s,throttle_min,throttle_max,max_exact_error\n');

for j = 1:2
    d = .3*(3-2*j);
    labels = {'increase','decrease'};
    label = labels{j};
    y = zeros(length(t),3);

    for n = 2:length(t)
        old = y(n-1,:)';
        a = A*old+b*d;
        c = A*(old+dt*a/2)+b*d;
        e = A*(old+dt*c/2)+b*d;
        g = A*(old+dt*e)+b*d;
        y(n,:) = (old+dt*(a+2*c+2*e+g)/6)';
    end

    yeq = -A\(b*d);
    exact = zeros(size(y));

    for n = 1:length(t)
        exact(n,:) = (yeq-expm(A*t(n))*yeq)';
    end

    err = max(abs(y(:)-exact(:)));
    assert(err<1e-8);

    open = 1-d/D*(1-exp(-D*t/M));
    speed = 1+y(:,1);
    throttle = .6+y(:,3);

    [~,idx] = max(abs(y(:,1)));
    bad = find(abs(y(:,1))>.02*abs(d));
    ts = 0;

    if ~isempty(bad)
        ts = NaN;
        if bad(end)<length(t)
            ts = t(bad(end)+1);
        end
    end

    fprintf(fid,'%.9g,%.12g,%.9g,%.9g,%.12g,%.12g,%.4g\n',...
        1+d,speed(idx),t(idx),ts,min(throttle),max(throttle),err);

    data = [t,speed,throttle,open,.6*ones(size(t)),.01*y(:,2)];

    out = fullfile(res,[label '_matlab.csv']);
    f = fopen(out,'w');
    fprintf(f,'time_s,closed_speed,closed_throttle,open_speed,open_throttle,level_change_m\n');
    fclose(f);
    dlmwrite(out,data,'-append','precision','%.12g');

figure;

    subplot(2,1,1);
    plot(t,speed,'b-',t,open,'r--','linewidth',1.5);
    hold on;
    plot(t,ones(size(t)),'k:');
    ylabel('Normalized speed');
    legend('Closed loop','Open loop','Nominal');
    grid on;
    xlim([0 30]);
    title(sprintf('Load torque 1 to %.1f',1+d));

    subplot(2,1,2);
    plot(t,throttle,'b-',t,.6*ones(size(t)),'r--','linewidth',1.5);
    xlabel('Time (s)');
    ylabel('Throttle fraction');
    grid on;
    xlim([0 30]);

    print(gcf,fullfile(figdir,[label '_matlab.png']),'-dpng','-r180');

    assert(min(throttle)>0 && max(throttle)<1);
end

fclose(fid);

minmargin = Inf;

for mask = 0:63
    factors = .8+.4*bitget(mask,1:6);
    p = [M D K tau kp ki].*factors;
    rr = roots([p(4)*p(1),p(1)+p(4)*p(2),...
        p(2)+p(3)*p(5),p(3)*p(6)]);
    minmargin = min(minmargin,-max(real(rr)));
end

assert(minmargin>0);
fprintf('Worst corner decay margin: %.9g /s\n',minmargin);
fprintf('Completed. Compare results with verified.json; no Python needed for this run.\n');

end