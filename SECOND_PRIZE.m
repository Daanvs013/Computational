function [winner, prize] = SECOND_PRIZE(bids)
winamount = max(bids);
win = find(bids == winamount);
winner = max(win);
A = sort(bids, 'descend');
prize = A(2);
end