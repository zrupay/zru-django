# ZRU Django


# Overview

ZRU Django provides integration access to the ZRU API through django framework.

# Requirements

* [Django][django]
* [ZRU Python][zru-python]

# Installation

Install using `pip`...

```bash
pip install zru-django
```

Add `'zru_django'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'zru_django',
    ...
)
```

Set the `ZRU_CONFIG` variable in settings.py using the following format:
```python
ZRU_CONFIG = {
    'PUBLIC_KEY': '<your_public-key>',
    'SECRET_KEY': '<your_secret-key>',
    'CHECK_SIGNATURE_ON_NOTIFICATION': True,
}
```

You can get these values on the [ZRU Panel][zru-developers-key].

This project is implemented with most versions in mind. For modern (and most) versions of Django, you should use:

```python
from django.urls import path, include
urlpatterns = [
    ...
    path("zru/", include('zru_django.urls')),
    ...
]
```

For older versions (django<2.0), you should use the `url` function instead of the `path` one.
 
Note: If you are using an older version of this library, you should set both 'PUBLIC_KEY' and 'PRIVATE_KEY' (set on the Django Admin page) on the settings.py file.

# Migration Guide for Versions Prior to 1.x.x

If you are migrating from a version prior to 1.x.x, you will need to update your import statements to reflect the change from django_mc2p to zru_django. Here is a guide to help you make these changes.

### Updating Import Statements

For any imports that used the django_mc2p module, replace django_mc2p with zru_django.

#### Example:

Before:
```python
from django_mc2p import MC2PClient
```
After:
```python
from zru_django import ZRUClient
```

### Updating Client class

Replace MC2PClient with ZRUClient.

#### Example

Before:

```python
client = MC2PClient(...)
```
After:

```python
client = ZRUClient(...)
```

## Steps to Update Your Code

1.  Search and Replace: Use your IDE or a text editor to search for django_mc2p and replace it with zru_django.
2.  Verify Imports: Ensure all import statements now reference zru_django.
3.  Run Tests: Run your test suite to verify that your code is functioning correctly with the updated imports.

### Summary

By following these steps, you can successfully migrate your project from versions prior to 1.x.x, ensuring compatibility with the new zru_django module naming convention.

# Quick Example

### Basic transaction

```python
# Sending user to pay
from zru_django import ZRUClient

zru = ZRUClient()
transaction = zru.Transaction({
    "currency": "EUR",
    "order_id": "order id",
    "products": [{
        "amount": 1,
        "product": {
            "name": "Product",
            "price": 50
        }
    }],
    "notify_url": "https://www.example.com" + reverse('zru-notify'),
    "return_url": "https://www.example.com/your-return-url/",
    "cancel_return": "https://www.example.com/your-cancel-url/"
})
transaction.save()
transaction.pay_url # Send user to this url to pay
transaction.iframe_url # Show an iframe with this url

# After user pay a notification will be sent to notify_url
from zru_django.signals import notification_received

def check_payment(sender, **kwargs):
    notification_data = sender
    if notification_data.is_transaction and notification_data.is_status_done:
        transaction_id = notification_data.id
        sale_id = notification_data.sale_id
        order_id = notification_data.order_id
        # Use transaction_id, sale_id and order_id to check all the data and confirm the payment in your system
notification_received.connect(check_payment)
```

### Basic subscription

```python
# Sending user to pay a subscription
from zru_django import ZRUClient

zru = ZRUClient()
subscription = zru.Subscription({
    "currency": "EUR",
    "order_id": "order id",
    "plan": {
        "name": "Plan",
        "price": 5,
        "duration": 1,
        "unit": "M",
        "recurring": true
    },
    "notify_url": "https://www.example.com" + reverse('zru-notify'),
    "return_url": "https://www.example.com/your-return-url/",
    "cancel_return": "https://www.example.com/your-cancel-url/"
})
subscription.save()
subscription.pay_url # Send user to this url to pay
subscription.iframe_url # Show an iframe with this url

# After user pay a notification will be sent to notify_url
from zru_django.signals import notification_received

def check_payment(sender, **kwargs):
    notification_data = sender
    if notification_data.is_subscription and notification_data.is_status_done:
        subscription_id = notification_data.id
        sale_id = notification_data.sale_id
        order_id = notification_data.order_id
        # Use subscription_id, sale_id and order_id to check all the data and confirm the payment in your system
notification_received.connect(check_payment)
```

### Basic authorization

```python
# Sending user to pay an authorization
from zru_django import ZRUClient

zru = ZRUClient()
authorization = zru.Authorization({
    "currency": "EUR",
    "order_id": "order id",
    "notify_url": "https://www.example.com" + reverse('zru-notify'),
    "return_url": "https://www.example.com/your-return-url/",
    "cancel_return": "https://www.example.com/your-cancel-url/"
})
authorization.save()
authorization.pay_url # Send user to this url to pay
authorization.iframe_url # Show an iframe with this url

# After user pay a notification will be sent to notify_url
from zru_django.signals import notification_received

def check_payment(sender, **kwargs):
    notification_data = sender
    if notification_data.is_authorization and notification_data.is_status_done:
        authorization_id = notification_data.id
        sale_id = notification_data.sale_id
        order_id = notification_data.order_id
        # Use authorization_id, sale_id and order_id to check all the data and confirm the payment in your system
notification_received.connect(check_payment)
```

[django]: https://www.djangoproject.com/
[zru-python]: https://github.com/zrupay/zru-python
[zru-developers-key]: https://panel.zrupay.com/config/developers/keys
