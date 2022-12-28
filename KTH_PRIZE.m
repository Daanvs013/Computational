function [winner, prize] = KTH_PRIZE(bids,k)
A = sort(bids, 'descend');
winners = A(1:k);
winner = find(ismember(bids, winners));
prize = A(k+1);
end