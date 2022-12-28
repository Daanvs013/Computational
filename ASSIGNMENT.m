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