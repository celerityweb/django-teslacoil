================
Django TeslaCoil
================

TeslaCoil is a Django application to expose the functionality of the Django admin app via ReSTful API calls and a rich HTML frontend using the same `ModelAdmin` classes in the stock admin application.

Why?
====

Django admin app is fantastic for launching a web based database content editing and administration interface with minimal code. It provides well structured and rich hooks that allow customization of the backend logic and templating.

However it's greatest limitation is that forms, views, and workflows are necessarily mapped one-to-one with the data model. For more complex or less concrete data models, this can result in convoluted workflows and poor user experience.

We aim to decouple the user interface and experience from the backend, using HTML+CSS+JS for a user-friendly web page application that speaks only to ReST API's. The developers may know how the user experience maps to the data model, but the user need not be burdened with these implementation details. We also aim to have the default, uncustomized operation of TeslaCoil create a basic user experience with functionality on par with and workflow similar to the traditional admin app.

