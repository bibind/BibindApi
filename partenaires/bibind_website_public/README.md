# Bibind Website Public

Module Odoo fournissant le site public de Bibind. Il expose des pages
`/`, `/offers`, `/offers/<slug>`, `/docs` et `/jobs`.

## Dépendances

- `website`
- `bibind_core`

## Configuration

Certains paramètres (URL de la documentation, base de l'API op_bootstrap) sont
lus via `ParamStore` du module `bibind_core`.

## Tests

Les tests utilisent la classe `HttpCase` d'Odoo. Ils sont automatiquement
ignorés si Odoo n'est pas disponible.

Exécution :

```bash
pytest partenaires/bibind_website_public/tests
```
