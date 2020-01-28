function B=closeHoles(A)
Ac=imcomplement(A);
[m,n]=size(A);
M=zeros(m,n);
M(1,:)=255;
M(m,:)=255;
M(:,1)=255;
M(:,n)=255;
M=reconstruct(Ac,M);
B=imcomplement(M);