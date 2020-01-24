A = imread('Frame142.png');
A = imresize(A,0.25);

[BW,maskedA] = createMask(A);
figure
imshow(maskedA)

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
disp(class(X));
[X,Y] = meshgrid(X,Y);
featureSet = cat(3,gabormag,X);
featureSet = cat(3,featureSet,Y);
numPoints = numRows*numCols;
X = reshape(featureSet,numRows*numCols,[]);
X = bsxfun(@minus, X, mean(X));
X = bsxfun(@rdivide,X,std(X));
coeff = pca(X);
feature2DImage = reshape(X*coeff(:,1),numRows,numCols);

disp(class(X));
disp(class(feature2DImage));
figure
imshow(feature2DImage,[])

NUM_KMEANS = 5;

BW_stretched = reshape(BW,numRows*numCols,1);
X(repmat(~BW_stretched,[1 26])) = -100;

L = kmeans(X,NUM_KMEANS,'Replicates',5);
L = reshape(L,[numRows numCols]);
figure
imshow(label2rgb(L))
for i = 1:NUM_KMEANS
    Aseg = zeros(size(A),'like',A);
    BW1 = L == i;
    BW1 = repmat(BW1,[1 1 3]);
    Aseg(BW1) = A(BW1);
    Aseg(repmat(BW, [1 1])) = 0;
    figure
    imshow(Aseg);
end

function [BW,maskedRGBImage] = createMask(RGB)
    HSV = rgb2hsv(RGB);
    % Define thresholds for 'Hue'. Modify these values to filter out different range of colors.
    channel1Min = 0.05;
    channel1Max = 0.45;
    % Define thresholds for 'Saturation'
    channel2Min = 0.000;
    channel2Max = 1.000;
    % Define thresholds for 'Value'
    channel3Min = 0.000;
    channel3Max = 1.000;
    % Create mask based on chosen histogram thresholds
    BW = ( (HSV(:,:,1) >= channel1Min) & (HSV(:,:,1) <= channel1Max) ) & ...
        (HSV(:,:,2) >= channel2Min ) & (HSV(:,:,2) <= channel2Max) & ...
        (HSV(:,:,3) >= channel3Min ) & (HSV(:,:,3) <= channel3Max);
    % Initialize output masked image based on input image.
    maskedRGBImage = RGB;
    % Set background pixels where BW is false to zero.
    maskedRGBImage(repmat(~BW,[1 1 3])) = 0;
    
end