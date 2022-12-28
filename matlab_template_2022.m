clear all;
close all;

%% Group details
% Group 21 consisting of
% 1. Hendrik (Nick) Verkaik
% 2. Daan van Turnhout
% 3. Daan Spanbroek
% 4. Dico de Gier


%% Excercise 1c (run function of part b) on the input below)
names = ['A','B','C','D','E'];
V_c = [3,2,1,3,3; 4,5,6,7,8; 5,10,5,10,5];
ASSIGNMENT(names, V_c)


%% Exercise 1e (run function of part d) on the input below)
names = ['A','B','C','D','E']; %Same as in part c), but added again for completeness.
V_e = [3,2,1,7,6; 40,5,6,7,8; 4,9,5.5,10,6];
k = [2,3,1];
KTH_AUCTION(names, V_e, k)


%% Exercise 1h) (run function of part g) on the input below)
G = {makedist('Gamma','a',5), makedist('Gamma','a',4), ...
        makedist('Gamma','a',3)};
n = 10;
r = [3,6,4];


%% Exercise 1i) (experimental verification)


%% Exercise 1k) (running function of part j) on some input)





%% Function of Exercise 1a)
function [winner, prize] = SECOND_PRIZE(bids)
winamount = max(bids);
win = find(bids == winamount);
winner = max(win);
A = sort(bids, 'descend');
prize = A(2);
end


%% Function of Exercise 1b)
function [nameprize] = ASSIGNMENT(names, bids)
% nameprize = ASSIGNMENT(names, bids)

% input
%-------
% names: a list of all names entering the auctions
% bids: a matrix with for every item a prize of what each bider bid
%
% output
% a matching of who won which item and what theyhave to pay
%
j = 1;
sizes = size(bids);
A = cell(sizes(1),2);
while j < sizes(1) + 1
    itemprize = bids(j,:);
    [index, prize] = SECOND_PRIZE(itemprize);
    name = names(index);
    A(j,1) = {name};
    A(j,2) = {prize};
    j = j + 1;
end
nameprize = A;
end

%% Function of Exercise 1d)
function [winner, prize] = KTH_PRIZE(bids,k)
A = sort(bids, 'descend');
winners = A(1:k);
winner = find(ismember(bids, winners));
prize = A(k+1);
end

function [matrix] = KTH_AUCTION(names, bids, copies)
sizes = size(bids);
A = cell(3,3);
for k = 1:length(names)
    A(k,1) = {names(k)};
    A(k,3) = {0};
end
j = 1;
while j < sizes(1) + 1
    itemprize = bids(j,:);
    copy = copies(j)
    [indexes, prize] = KTH_PRIZE(itemprize, copy);

    i = 1;
    len = size(indexes);
    while i < len(2) + 1
        position = indexes(i);
        B = A{position ,2}
        B(end+1) = j
        A{position ,2} = B
        oldprize = A(position, 3);
        newprize = oldprize{1} + prize;
        A(position, 3) = {newprize};
        i = i + 1
    end
    j = j + 1;
end
matrix = A
end



%% Function of Exercise 1f)
function output = DISTRIBUTION(pdo, k, n)
output = @(y) factorial(n)*pdf(pdo,y)*(cdf(pdo,y))^(n-k-1)*(1-cdf(pdo,y))^k/(factorial(k)*factorial(n-k-1));
end


%% Function of Exercise 1g)
function evalue = expected(probobj, k, n)
total = 0;
for i = 1:length(k)
    fun = DISTRIBUTION(probobj{i}, k(i), n);
    p = k(i);
    subtotal = 0;
    for j = 1:20
        subtotal = subtotal + fun(j)* j;    
    end
    total = total + subtotal * p;
end
evalue = total;
end
 
%% Function of Exercise 1j)
function [winner, prize] = SECOND_PRIZE_RESERVE(bids, maxi)
winamount = max(bids);
if winamount >= maxi
    win = find(bids == winamount);
    winner = max(win);
    A = sort(bids, 'descend');
    if A(2) > maxi
        prize = A(2);
    else
        prize = maxi;
    end
else
    prize = 0;
    winner = 0;
end