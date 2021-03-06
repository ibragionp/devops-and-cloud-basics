## Conceitos Amazon Web Services (AWS):

VPC: Serve como uma rede virtual privada onde podem ser executados recursos na AWS. É como uma rede normal de uma empresa, mas é possível definir seu tamanho.

Roles: São funcões que podem ser criadas em uma conta na AWS. Serve para determinar permissões, o que pode e o que não pode ser feito nos recursos da AWS.

NAT: É um dispositivo que encaminha uma requisição de uma subrede privada para internet e depois retorna uma "resposta", porém funciona apenas nesse sentido. A internet não consegue acessar minha subrede. Funciona apenas com endereços ipv4.

Security Gateways: Controla o tráfego de acessos da VPC para internet e da internet para a VPC. O controle é feito através de grupos de segurança, neles contém grupos de rotas que podem ter o acesso.

Routes: São como caminhos na rede, que determinam para onde o tráfego na rede será direcionado.


VPC Peering: VPC Peering é uma conexão de rede entre duas VPCs. Fazendo uma requisição de acesso e alterando as rotas na route table da instância. Devo utilizar quando eu preciso acessar recursos em outra VPC, e claramente, não é possível acessar um IP privado. Utilizando um tráfego público eu conseguiria acessar, mas iria expor as VPCs, o que é errado. Para isso eu utilizo o VPC peering, que além de ser possível acessar outras VPCs na mesma conta na AWS, também é possível acessar de outra conta e até de outra região no mundo.
