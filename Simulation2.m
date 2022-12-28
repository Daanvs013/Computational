k = [1];
G = {makedist('halfnormal', 0, 2)};
n = 50;

the_evalue = expected(G,k,n);
pd = makedist('HalfNormal','mu',0,'sigma',2);
storage = zeros(10000, 1);
for t = 1:10000
    v = random(pd, 1, n);
    [winner, prize] = SECOND_PRIZE(v);
    storage(t,1) = prize;
end
simevalue = mean(storage,1);
