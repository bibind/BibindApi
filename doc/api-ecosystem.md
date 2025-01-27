### **Résumé des endpoints API actuels et recommandations à développer**
#### **Endpoints API déjà existants dans l’infrastructure Bibind**
Ces endpoints sont principalement déployés et intégrés aux services actuels **OpenStack** et **Ceph**, basés sur la configuration et le réseau définis.
##### **1. OpenStack (existant)**
- **Keystone (identity)** :
    - Endpoint public:
`https://public.bibind.com:5000`
    - Endpoint interne:
`https://internal.bibind.com:5000`

- **Nova (compute)** :
    - Endpoint public:
`https://public.bibind.com:8774/v2.1`
    - Endpoint interne:
`https://internal.bibind.com:8774/v2.1`
    - Fonctionnalités associées :
        - Création, mise à jour et suppression d'instances.
        - Gestion des ressources virtuelles.

- **Neutron (network)** :
    - Endpoint public:
`https://public.bibind.com:9696`
    - Endpoint interne:
`https://internal.bibind.com:9696`
    - Fonctionnalités associées :
        - Gestion des réseaux (VLAN, SRIOV, etc.).
        - Attribution d'adresses IP flottantes.

- **Glance (image)** :
    - Endpoint public:
`https://public.bibind.com:9292`
    - Endpoint interne:
`https://internal.bibind.com:9292`
    - Fonctionnalités associées :
        - Gestion des images d'instances.
        - Chargement et export d'images.

- **Cinder (block storage)** :
    - Endpoint public:
`https://public.bibind.com:8776/v3/%(tenant_id)s`
    - Endpoint interne:
`https://internal.bibind.com:8776/v3/%(tenant_id)s`
    - Fonctionnalités associées :
        - Gestion des disques block de stockage.

- **Heat (orchestration)** :
    - Endpoint public:
`https://public.bibind.com:8004/v1/%(tenant_id)s`
    - Endpoint interne:
`https://internal.bibind.com:8004/v1/%(tenant_id)s`
    - Fonctionnalité : gestion des stacks d'infrastructure en tant que code.

- **Heat CloudFormation (API CFN)** :
    - Endpoint public:
`https://public.bibind.com:8000/v1`
    - Endpoint interne:
`https://internal.bibind.com:8000/v1`

- **Placement** :
    - Endpoint public:
`https://public.bibind.com:8780`
    - Endpoint interne :
`https://internal.bibind.com:8780`

- **Designate (DNS)** :
    - Endpoint public :
`https://public.bibind.com:9001`
    - Endpoint interne :
`https://internal.bibind.com:9001`

- **Skyline (interface utilisateur avancée pour dashboard)** :
    - Endpoint public:
`https://public.bibind.com:9998`
    - Endpoint interne:
`https://internal.bibind.com:9998`

##### **2. Ceph (Stockage distribué)**
- **Ceph Dashboard** :
    - Endpoint principal :
`https://ceph.bibind.com`
    - Fonctionnalités associées :
        - Suivi du cluster Ceph.
        - Gestion des pools, RBD, et alertes.

- **Backend actif** : REST API Ceph
Implémentée sur le réseau interne via le port `:8443`. Exemple :
    - `https://10.197.92.9:8443`

##### **3. Applications Dashboard**
1. **Horizon (Dashboard OpenStack)** :
    - Endpoint principal :
`https://horizon.bibind.com`

2. **Skyline (Dashboard avancée)** :
    - Endpoint dynamique :
`https://skyline.bibind.com`
   
##### **1. ApiBibind (proposer une API REST pour tous les services)**
**Base d’URL suggérée pour tous les endpoints** :
`https://apibibind.bibind.com/v1`