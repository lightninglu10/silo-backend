from django.db import models

class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discount')
    code = models.CharField(max_length=200)
    percentage = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    cash = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    num_left = models.IntegerField(blank=True, null=True)
    expires = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self):
        return 'The code: %s gives you %s percent off and %s$ off. Is active: %s' % (str(self.code), str(self.percentage), str(self.cash), str(self.is_active))