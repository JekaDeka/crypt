from django.db import models
from crypt import encode


class Post(models.Model):
    text = models.TextField()
    crypted_type = models.PositiveSmallIntegerField(default=1)
    key = models.TextField(default=None)
    crypted_text = models.TextField(default=None)

    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text

    def crypt(self):
        if self.crypted_type == 1:
            dic = encode.getAlphabet()
            vec = encode.toNumVecX(self.text, dic)
            key = encode.generateKey(vec, dic)
            return encode.encrypt(vec, dic, key), encode.keyToString(key, dic)
        elif self.crypted_type == 2:
            return "Snd crypt type"
        elif self.crypted_type == 3:
            return "Thrd crypt type"
        else:
            return "Another crypt type"

    def save(self, *args, **kwargs):
        self.crypted_text, self.key = self.crypt()
        super(Post, self).save(*args, **kwargs)
