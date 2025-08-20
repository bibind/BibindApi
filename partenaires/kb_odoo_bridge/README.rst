Kill Bill Odoo Bridge
=====================

This module integrates Odoo with the `Kill Bill <https://killbill.io>`_ billing platform.

Installation
------------

* Install Python dependencies:

  .. code-block:: bash

     pip install -r requirements.txt

* Add the module to your ``odoo.conf`` ``addons_path``.

Configuration
-------------

Navigate to :menuselection:`Settings --> Kill Bill` and configure the following
parameters:

* Base URL of Kill Bill
* API key and secret
* Basic authentication credentials
* Webhook secret (optional)

Usage
-----

* On partners, use the **Créer compte Kill Bill** button to create and link an
  account in Kill Bill.
* On sale orders containing subscription products, use **Souscrire (Kill Bill)**
  to create subscriptions.
* A cron job runs every 10 minutes to synchronise invoices and payments.
* Wizards are available to import or publish the catalog from/to Kill Bill.

Tests
-----

Run unit tests with ``pytest``::

   pytest kb_odoo_bridge/tests -q

