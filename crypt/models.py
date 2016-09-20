from django.db import models

# def extend(string_to_expand, length):
#    return (string_to_expand * ((length/len(string_to_expand))+1))[:length]


# def substitution(text):
# 	splitedText = list(text)
# 	tmp = "ключ"


class Post(models.Model):
    text = models.TextField()
    crypted_text = models.TextField()
    crypted_type = models.PositiveSmallIntegerField(default=1)

    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text

    def crypt(self, case):
        if case == 1:
            return "First crypt type"
        elif case == 2:
            return "Snd crypt type"
        elif case == 3:
            return "Thrd crypt type"
        else:
            return "Another crypt type"

    def save(self, *args, **kwargs):
        self.crypted_text = self.crypt(self.crypted_type)
        super(Post, self).save(*args, **kwargs)
