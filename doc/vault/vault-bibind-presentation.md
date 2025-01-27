### **Présentation de Vault**
#### **Qu'est-ce que HashiCorp Vault ?**
HashiCorp Vault est un outil open source conçu pour **gérer les secrets de manière centralisée** et sécurisée. Les secrets peuvent inclure des mots de passe, des clés API, des certificats SSL, et bien plus. Vault offre des fonctionnalités essentielles, comme :
- **Stockage chiffré** des secrets.
- **Gestion fine des accès** grâce à des politiques basées sur les utilisateurs et applications/services.
- **Rotation automatique des secrets**, comme les mots de passe de base de données ou les certificats.
- **Accès programmatique** sécurisé via des APIs.
- **Audit des accès** pour garantir la traçabilité des opérations.

#### **Exemples d'utilisation dans un projet comme Bibind :**
1. Stocker les **mots de passe d'administration** et des bases de données utilisées dans les modules (FastAPI, Odoo).
2. Gérer les **clés API** pour des services tiers (GitHub, OVH, etc.).
3. Stocker et gérer les **certificats SSL/TLS** utilisés par HAProxy ou d'autres fronts d'application.
4. Fournir des accès temporaires aux services en interne de manière sécurisée.

### **Commandes principales pour la gestion des secrets avec Vault**
#### **1. Initialisation et déblocage de Vault**
Vault doit être initialisé et déverrouillé avant d’être utilisé. Voici les commandes clés :
1. **Initialisation** (génère des clés de déblocage et un token root) :
   vault operator init
2. 
- Répétez avec plusieurs clés jusqu'à ce que l’état de Vault soit "unsealed" (par défaut, il en faut 3 sur 5 générées lors de l'initialisation).