# LlapaYachay
#### Quechua translation: All - Know
## Blockchain model for university degree registration and issuance
------------
It is a blockchain model focused on the registration and issuance of university degrees, which can consist of up to five participating nodes, with an additional node dedicated to interaction with the public.
### Version
The current project is version 1.0.0.

### State
The current project is a prototype that includes the basic and essential functionalities of a blockchain system, being an initial version, it is recognised that there are some improvements to be added, however, this first version aims to explore the application of this technology in university degrees.
### Prerequisites
This project has been developed and tested on Linux only, and the environment must meet the following requirements
- Ubuntu 20.04 or 22.04 operating system
- Docker Engine 20.10
- Python >= 3.10.0

### Install

Note: Before proceeding, check that the above requirements are met.

1. Download or clone the repository, and go into the Llapayachay folder, and then into the src subfolder:

        cd LlapaYachay
        cd src

2. In this folder you will find 2 other folders called participants and public, first go to the participants folder:

        cd participantes

3. Run the script image.sh and then the script start.sh

        bash image.sh
        bash start.sh
4. Return to the previous directory and change to the public folder:

        cd ...
        cd public

5. Run the image.sh script and then the start.sh script

        bash image.sh
        bash start.sh
6. Then return to the initial path where the repository was downloaded or cloned, and continue with the startup configuration.

![dockers containers](https://user-images.githubusercontent.com/77517569/226686743-e9e9642c-7cbb-46ac-85a0-07620c177f18.png)

### Initial configuration
The ports of the participating nodes are in the range 5000 - 5004, with each node assigned to a network port in the same order.
1. When logging in to a participating node, if no blockchain network has been configured, the "setup" view will be loaded automatically and only once to fill in the fields:
	- Blockchain network name : In this field, the user defines the name of the blockchain network.
	- Participating nodes : In this field, the user defines the number of participating nodes.
	- Private network domain : In this field, the user defines the IP of the host server or domain, e.g: 99.999.99.9 or domain.test
	- Confirmation field: Use this field to confirm that the fields have been filled in correctly.
![setup](https://user-images.githubusercontent.com/77517569/226686925-e47ec425-e97e-4a52-b3c1-68328b682338.png)
![setup-complete](https://user-images.githubusercontent.com/77517569/226686950-e8d030e6-f062-4be1-92ff-1de60f3c502e.png)

2. Then, if the node is not registered, it will be asked to register once by filling in the following fields:
	- Name : in this field, the participant enters his first name(s).
	- Surname : In this field, the user enters his or her surname.
	- Identity document : In this field, the user enters the number of the identity document.
	- Peer node : In this field the participant's role is selected and should not be registered with a role already in use.
	- Password and confirmation: A password is registered and validated by repeating it, the user must remember the key, as this key must be entered each time he/she signs with his/her private key in the blockchain.
![Registro nodo](https://user-images.githubusercontent.com/77517569/226687060-321a5f59-d24f-4c5c-b3eb-fe359f83b9a8.png)
![registro nodo completo](https://user-images.githubusercontent.com/77517569/226687079-b2c59ef3-afd8-495a-8254-7918d3c386b5.png)


3. Finally, the main panel of the participating nodes is loaded with the sections:
	- Blockchain: This section is available to all nodes, and you can see the hash of each node in relation to the hash of the previous block.
	- Signature: This section is available for the node with the signing role, and you can see the list of records to be signed, and you can only sign once per record.
	- Registration: This section is available to the node with the Create role and you can see the list of registrations made and a button to create more registrations.
![registro setup y credencial completo](https://user-images.githubusercontent.com/77517569/226687180-4b48c694-c9c9-488d-815b-bb191ed80f73.png)

### Ilustrative examples
3.1.	Initial configuration of the blockchain network
Figure 5 shows the deployed system, with six active containers representing the nodes of the blockchain. The containers acting as nodes in the prototype use the image "node" and are labelled "node1" to "node5". In addition, the public node container is labelled 'public'. This clearly illustrates the configuration and organisation of the nodes within the developed blockchain network.

 ![image](https://github.com/horus100/LlapaYachay/assets/77517569/b95c576d-d368-401b-9970-5e0c5df157a1)
 
Figure 5. List of Docker containers

Figure 6 shows the initial blockchain setup for a university issuing professional degrees. The blockchain’s name, number of nodes, and private network domain (e.g. IP address or domain, such as 99.999.999.999.999 or domain.com) are defined. Roles are assigned to participants such as the head of the professional degree area, rector, vice-rector, faculty director, and supervising institution, specifying their names and roles. This illustrates the setup process and highlights the importance of role definition and network structure in professional degree awarding and validation.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/97d56258-6528-485f-888f-fc535c1b976f)

Figure 6. Blockchain network initial configuration interface

3.2.	Adding new participants to the network
Figure 7 shows the node registration form after the blockchain’s initial setup. The user enters their personal details, selects the node type, and sets a password for blockchain authorisation. Additional nodes joining the network must register their data to interact with the blockchain. This illustrates the process of adding new participants and their interaction within the blockchain network.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/68a65d44-6dab-487a-95ed-82e28cdf6158)

Figure 7. User registration interface as a participating node.

3.3.	Visualisation of the blockchain and its details
After the initial configuration and registration of the node, participants can create or sign blocks and view the blockchain as a whole. The blockchain is represented by a table, where each row corresponds to a single block, including its hash and the hash of the previous block (Figure 8). This representation makes it easier to understand and monitor the blockchain, ensuring the transparency and integrity of the information stored.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/6b4733f6-ddae-4649-a7ab-5bb8dae4dda3)

Figure 8. Blockchain interface.

3.4.	Interaction with the public node
The following images (Figures 9 and 10) show the interface of the node that will interact with the interested public. This node offers specific functionalities, such as performing title queries using a hash (Figure 9) and visualising the blockchain in tabular form (Figure 10). These features provide easy and transparent access to the information stored on the blockchain for external users who wish to verify securities or query the blockchain.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/3ed7c02e-3ea3-4fef-a722-8803ece25d79)

Figure 9. Public Node Interface, Part 1.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/128ede1f-268d-4196-8e55-6d22676cfd47)

Figure 10. Public Node Interface, Part 2.

3.5.	Procedure for registering a professional title
This process is carried out by an assigned user on the network, who is responsible for registering the title data. The user must then enter his or her password to sign the block created (Figure 11). If the registration is successful, the system displays a confirmation message (Figure 12). This approach guarantees the authenticity and integrity of the data registered in the blockchain, while giving responsibility to the assigned user.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/7ba742b5-f261-43cc-b739-1ce438459ee0)

Figure 11. Registration form for a professional title.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/2b50e33f-b054-44e2-b637-3702ce1f9cdd)

Figure 12. Registration confirmation.

3.6.	Procedure for the signature of the professional title
This process is performed by nodes with block signing ability. The “Signature” section shows records waiting to be signed (Figure 13). Pressing the Sign button opens a form with professional title data and a field for entering the personal key to sign the title (Figure 14). A warning is displayed upon completion indicating success (Figure 15). This approach ensures professional title data authenticity and integrity and provides accountability to signing nodes. 

![image](https://github.com/horus100/LlapaYachay/assets/77517569/a6f13df9-5573-4191-8804-2778ace917e2)

Figure 13. Interface for signing a title.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/13d8528b-28d3-40b8-9989-30611b464e3c)

Figure 14. Form for signing the professional title.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/34aaa0f1-f544-4b3c-b2de-2945deee0627)

Figure 15. confirmation notification.

3.7.	Notification, award and verification of the professional title
When a professional title is registered, an email with the title’s hash for verification is sent (Figure 16). Once signatures are complete, the title’s PDF with a QR code for verification is sent (Figure 17). Scanning the QR code or entering the title’s hash in the public node’s query function displays the title with supporting block hashes (Figure 18). This guarantees the title’s authenticity and makes verification easy.

![mails](https://github.com/horus100/LlapaYachay/assets/77517569/f4ad6b09-a904-4836-9520-b1f361ff783e)


Figure 16. Sent emails.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/90c5b04f-0a5b-4416-a93b-78eef5f4605d)

Figure 17. Model of the professional title to be sent.

![image](https://github.com/horus100/LlapaYachay/assets/77517569/5b0035b6-fbac-4976-9b60-95eed9909b2f)

Figure 18: Verification of a professional title.

In summary, this example shows how the implementation of a university blockchain network can facilitate and secure the issuance and verification of professional degrees. The assignment of specific roles to key stakeholders ensures efficient and secure collaboration (Figure 6). Blockchain technology offers an innovative solution to the challenges of academic document management, improving the reliability, integrity and authenticity of issued professional degrees. This approach can serve as a model for other educational institutions wishing to improve their degree issuance and verification processes using new and secure technologies.
