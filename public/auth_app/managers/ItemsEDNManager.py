from django.db import models

class ItemsEDNManager(models.Manager):

    """
    Manager for the `Item` model.
    
    This manager includes methods to retrieve items based on different criteria.
    """

    # getter return 1 element
    def get_by_id(self, item_id):
        """
        Retrieve an item by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Item: The retrieved item or None if not found.
        """
        return self.get(id=item_id)

    def get_by_numero(self, numero):
        """
        Retrieve items by their numero.

        Args:
            numero (str): The numero of the items to retrieve.

        Returns:
            QuerySet[Item]: A queryset containing items that match the given numero.
        """
        return self.filter(numero=numero)

    # getter return a list

    def get_by_titre(self, titre):
        """
        Retrieve items by their title (case-insensitive).

        Args:
            titre (str): The title of the items to retrieve.

        Returns:
            QuerySet[Item]: A queryset containing items that match the given title.
        """
        return self.filter(titre__icontains=titre)

    def get_by_writing_college(self, writing_college):
        """
        Retrieve items by their writing college (case-insensitive).

        Args:
            writing_college (str): The writing college of the items to retrieve.

        Returns:
            QuerySet[Item]: A queryset containing items that match the given writing college.
        """
        return self.filter(writing_college__icontains=writing_college)

    def get_by_proofreading_college(self, proofreading_college):
        """
        Retrieve items by their proofreading college (case-insensitive).

        Args:
            proofreading_college (str): The proofreading college of the items to retrieve.

        Returns:
            QuerySet[Item]: A queryset containing items that match the given proofreading college.
        """
        return self.filter(proofreading_college__icontains=proofreading_college)

    # dynamic search

    def search(self, numero=None, titre=None, writing_college=None, proofreading_college=None):
        """
        Perform a dynamic search for items based on various criteria.

        Args:
            numero (str, optional): The numero of the item to filter by.
            titre (str, optional): The title of the item to filter by.
            writing_college (str, optional): The writing college of the item to filter by.
            proofreading_college (str, optional): The proofreading college of the item to filter by.

        Returns:
            QuerySet[Item]: A queryset containing items that match any of the given criteria.
        """
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
