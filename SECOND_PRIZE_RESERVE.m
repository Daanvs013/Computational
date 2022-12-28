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