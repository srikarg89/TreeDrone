function [A,Agray] = matlab_test(fname)
    A = imread(fname);
    A = imresize(A, 0.25);
    Agray = rgb2gray(A);
%    disp(A(1,:,:));
%    Agray = [1 2 3 4; 5 6 7 8; 9 10 11 12];
%    disp(size(Agray));
end