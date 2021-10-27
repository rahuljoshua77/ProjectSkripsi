%load('fisheriris');
filename = 'C:\Users\User\Downloads\INSINAS\PROGRAM\kor_x.xlsx';
x1 = xlsread(filename,'A1:T2046');
filename = 'C:\Users\User\Downloads\INSINAS\PROGRAM\kor_x.xlsx';
t1=xlsread(filename,'A12048:T2048');
x=x1';
t=t1';
CVO = cvpartition(t,'KFold',10);
err = zeros(CVO.NumTestSets,1);
for i = 1:CVO.NumTestSets
    trIdx = CVO.training(i);
    teIdx = CVO.test(i);
    inputtest=x(teIdx,:);
    inputtrain=x(trIdx,:);
    targettest=t(teIdx,:);
    targettrain=t(trIdx,:);
   
    %--------PNN-------------------
%    targettrain=targettrain';
%    O= ind2vec(targettrain); 
%   inputtrain= inputtrain';
%     net=newpnn(inputtrain,O); 
%      outputs1 = net(inputtrain);
%      figure,plotconfusion(outputs1 ,O);
%      inputtest=inputtest';
%      targettest=targettest';
%     outputs = net(inputtest); 
%     O= ind2vec(targettest);
%     figure,plotconfusion(outputs,O);
    
    
     %--------SVM-------------------
   
    svmStruct = fitcecoc(inputtrain,targettrain)

     svmStruct.BinaryLearners{1} 
%           targettest=targettest';
%        O3= full(ind2vec(targettest,6));
%        outputs = predict(svmStruct,inputtest);
%      O2= ind2vec(outputs',6);
%        figure,plotconfusion(O3 ,O2); 
%        targettrain=targettrain' ;
%        output1 = predict(svmStruct,inputtrain);
%          O1= full(ind2vec(output1',6));
%      O= full(ind2vec(targettrain,6)); 
%        figure,plotconfusion(O ,O1);

     
      %--------Decision Tree------------------
%    treee = fitctree(inputtrain,targettrain);
%    outputs = predict(treee,inputtest);
%    O= ind2vec(targettest');
%  O1= ind2vec(outputs');
%  figure,plotconfusion(O1 ,O); 


%--------Naives Bayes------------------
% MDL = fitcnb(inputtrain,targettrain);
% targettest=targettest;  
% outputs = predict(MDL,inputtest)
%    O= ind2vec(targettest');
%  O1= ind2vec(outputs');
%  figure,plotconfusion(O1 ,O);
% 
%    output1 = predict(MDL,inputtrain);
%      O1= ind2vec(output1');
%             targettrain=targettrain;
%              O= ind2vec(targettrain'); 
%      figure,plotconfusion(O1 ,O);
%      err(i) = sum(~strcmp(output1,t(teIdx)));
  end
cvErr = sum(err)/sum(CVO.TestSize);