# Django
### Admin Page at http://127.0.0.1:8000/admin
### To create superuser
```python
python3 manager.py createsuperuser --username admin
```
#### Manually active the user from database
#### set is_active field in database to 1

### To populate the database
#### First comment out signals.py
```python
from djangoTut.utils import crawler
```
#### Remember to uncomment signals.py


### To register
#### touch ./djangoTut/config.py
```python
EMAIL_HOST_USER = 'YOUR OFFICE EMAIL ACCOUNT'
EMAIL_HOST_PASSWORD = 'YOUR EMAIL PASSWORD'
```
#### Make sure email's SMTP and POP is enable

### TODO
#### Application
#### Compare
#### Pagination
#### And more which I can't remember
