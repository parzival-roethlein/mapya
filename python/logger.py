import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
print('name: %s' % __name__)

if __name__ == '__main__':
    print('name: %s' % __name__)