function B=recompose(A,R,seuil)
B=imresize(A,2,'nearest'); % sur-�chantillonnage
Rseuil = R.*(abs(R)<=seuil); % seuillage
B=B+Rseuil;