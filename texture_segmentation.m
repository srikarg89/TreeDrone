A = imread('drone1.png');
A = imresize(A,0.25);
[BW,maskedRGBImage] = createMask(A);
subplot(1,3,1);imshow(A);title('Original Image');
subplot(1,3,2);imshow(BW);title('Mask');
subplot(1,3,3);imshow(maskedRGBImage);title('Filtered Image');

Agray = rgb2gray(A);
figure
imshow(A)
imageSize = size(A);
numRows = imageSize(1);
numCols = imageSize(2);

wavelengthMin = 4/sqrt(2);
wavelengthMax = hypot(numRows,numCols);
n = floor(log2(wavelengthMax/wavelengthMin));
wavelength = 2.^(0:(n-2)) * wavelengthMin;

deltaTheta = 45;
orientation = 0:deltaTheta:(180-deltaTheta);

g = gabor(wavelength,orientation);
gabormag = imgaborfilt(Agray,g);
for i = 1:length(g)
    sigma = 0.5*g(i).Wavelength;
    K = 3;
    gabormag(:,:,i) = imgaussfilt(gabormag(:,:,i),K*sigma); 
end
X = 1:numCols;
Y = 1:numRows;
[X,Y] = meshgrid(X,Y);
featureSet = cat(3,gabormag,X);
featureSet = cat(3,featureSet,Y);
numPoints = numRows*numCols;
X = reshape(featureSet,numRows*numCols,[]);
X = bsxfun(@minus, X, mean(X));
X = bsxfun(@rdivide,X,std(X));
coeff = pca(X);
% trying to apply the mask to feature2d, but if u look below kmeans is run
% on X, not feature2d, so i actually need to apply mask to x, but dunno how
feature2DImage = reshape(X*coeff(:,1),numRows,numCols);
figure
imshow(feature2DImage,[])
L = kmeans(X,2,'Replicates',5);
L = reshape(L,[numRows numCols]);
figure
imshow(label2rgb(L))
Aseg1 = zeros(size(A),'like',A);
Aseg2 = zeros(size(A),'like',A);
BW2 = L == 2;
BW2 = repmat(BW2,[1 1 3]);
Aseg1(BW2) = A(BW2);
Aseg2(~BW2) = A(~BW2);
figure
imshowpair(Aseg1,Aseg2,'montage');

function [BW,maskedRGBImage] = createMask(RGB) 
    % Convert RGB image to HSV image
    I = rgb2hsv(RGB);
    % Define thresholds for 'Hue'. Modify these values to filter out different range of colors.
    channel1Min = 0.10;
    channel1Max = 0.40;
    % Define thresholds for 'Saturation'
    channel2Min = 0.000;
    channel2Max = 1.000;
    % Define thresholds for 'Value'
    channel3Min = 0.000;
    channel3Max = 1.000;
    % Create mask based on chosen histogram thresholds
    BW = ( (I(:,:,1) >= channel1Min) & (I(:,:,1) <= channel1Max) ) & ...
        (I(:,:,2) >= channel2Min ) & (I(:,:,2) <= channel2Max) & ...
        (I(:,:,3) >= channel3Min ) & (I(:,:,3) <= channel3Max);
    % Initialize output masked image based on input image.
    maskedRGBImage = RGB;
    % Set background pixels where BW is false to zero.
    maskedRGBImage(repmat(~BW,[1 1 3])) = 0;
end