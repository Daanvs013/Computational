T = 10000;
p = [0:10];
i = 1;
sim = zeros(11,T);
while i <= T
    r = gamrnd(5,1,1,2);
    for j = 1:11;
        [winner, prize] = SECOND_PRIZE_RESERVE(r,p(j));
        sim(j,i) = prize;
    end
    i = i + 1;
    
end

aver = mean(sim,2);
maxi = max(aver)
place = find(aver == maxi)-1
scatter(p,aver)
