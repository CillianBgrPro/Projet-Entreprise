from django.db import models

class ItemsEDNManager(models.Manager):

    # getter return 1 element

    def get_by_id(self, item_id):
        return self.get(id=item_id)

    def get_by_numero(self, numero):
        return self.filter(numero=numero)

    # getter return a list

    def get_by_titre(self, titre):
        return self.filter(titre__icontains=titre)

    def get_by_writing_college(self, writing_college):
        return self.filter(writing_college__icontains=writing_college)

    def get_by_proofreading_college(self, proofreading_college):
        return self.filter(proofreading_college__icontains=proofreading_college)

    # dynamic search

    def search(self, numero=None, titre=None, writing_college=None, proofreading_college=None):
        search = self.all()
        if numero:
            search = search.filter(numero=numero)
        if titre:
            search = search.filter(titre__icontains=titre)
        if writing_college:
            search = search.filter(writing_college__icontains=writing_college)
        if proofreading_college:
            search = search.filter(proofreading_college__icontains=proofreading_college)
        return search
