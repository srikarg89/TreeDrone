run('TestImages/Nashville/Frame17.png');
%run('TestImages/WindsorNationalPark/Frame12.png');

function r = run(fname)
    A = imread(fname);
    A = imresize(A,0.1);
%    A = imresize(A,0.25);
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
    
    disp(g(1));

    gabormag = imgaborfilt(Agray,g);

    for i = 1:length(g)
        sigma = 0.5*g(i).Wavelength;
%        disp(sigma);
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
    feature2DImage = reshape(X*coeff(:,1),numRows,numCols);
    figure
    imshow(feature2DImage,[])

    L = kmeans(X,2,'Replicates',5);

    L = reshape(L,[numRows numCols]);
    figure
    imshow(label2rgb(L))
    r = 10;
    
    Aseg1 = zeros(size(A),'like',A);
    Aseg2 = zeros(size(A),'like',A);
    BW = L == 2;
    BW = repmat(BW,[1 1 3]);
    Aseg1(BW) = A(BW);
    Aseg2(~BW) = A(~BW);
    figure
%    imshow(Aseg2)
    imshowpair(Aseg1,Aseg2,'montage');
    
    L2 = kmeans(X,3,'Replicates',5);
    L2 = reshape(L2,[numRows numCols]);
%    [L2,Centers] = imsegkmeans(feature2DImage,3);
    B = labeloverlay(A,L2);
    figure
    imshow(B)




end