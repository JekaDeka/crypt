from django.db import models
from crypt import encode
import rsa


class Post(models.Model):
    text = models.TextField()
    crypted_type = models.PositiveSmallIntegerField(default=1)
    key = models.TextField(default='')
    privkey = models.TextField(default='')
    crypted_text = models.TextField(default='')

    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text

    def encrypt(self):
        if self.crypted_type == 1:
            dic = encode.getAlphabet()
            vec = encode.toNumVecX(self.text, dic)
            key = encode.generateKey(vec, dic)
            return encode.encrypt(vec, dic, key), encode.keyToString(key, dic)

        elif self.crypted_type == 2:
            msg = (self.text).encode('utf-8')
            (pubkey, privkey) = rsa.newkeys(512)
            self.privkey = privkey
            enc = rsa.encrypt(msg, pubkey)
            return enc.decode('utf-8', 'replace'), hex(pubkey.n)[:-1] + "?" + hex(pubkey.e)[:-1]

        elif self.crypted_type == 3:
            return "Thrd crypt type"
        else:
            return "Another crypt type"

    def decrypt(self):
        if self.crypted_type == 2:
            tmpKey = (self.privkey).split(',')
            privkey = rsa.PrivateKey(int(tmpKey[0].replace("PrivateKey(", "", 1)), int(tmpKey[1]), int(
                tmpKey[2]), int(tmpKey[3]), int(tmpKey[4].replace(")", "", 1)))
            return (rsa.decrypt(self.crypted_text, privkey))

        elif self.crypted_type == 3:
            return "Thrd ctypt type"
        else:
            return "Another ctypt tpye"

    def save(self, *args, **kwargs):
        self.crypted_text, self.key = self.encrypt()
        super(Post, self).save(*args, **kwargs)
